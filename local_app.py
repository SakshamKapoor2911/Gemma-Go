import streamlit as st
import ollama
import tempfile
import os
from faster_whisper import WhisperModel


# --- Application State ---
st.session_state.setdefault("feedback", "Your feedback will appear here.")


# --- Model Loading (Whisper) ---
@st.cache_resource
def load_whisper_model():
    """Loads the faster-whisper model and caches it."""
    try:
        model = WhisperModel("base.en", device="cpu", compute_type="int8")
        return model
    except Exception as e:
        st.error(f"Could not load Whisper model: {e}")
        return None

whisper_model = load_whisper_model()


# --- AI and Audio Logic ---
def transcribe_audio(audio_bytes):
    """Transcribes audio using the pre-loaded faster-whisper model."""
    if whisper_model is None:
        return "Whisper model not loaded. Cannot transcribe."

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_file_path = tmp_file.name
    try:
        segments, _ = whisper_model.transcribe(tmp_file_path, beam_size=5, language="en")
        transcribed_text = " ".join([segment.text for segment in segments])
        return transcribed_text
    except Exception as e:
        return f"Error during transcription: {e}"
    finally:
        os.remove(tmp_file_path)

def get_empathy_feedback(text_to_analyze):
    """Sends transcribed text to the locally running Ollama model."""
    prompt = f"""
    You are an expert empathy and communication coach. Your task is to analyze the following text and provide gentle, constructive feedback.
    Analyze the text from three perspectives:
    1.  **Clarity:** How clear is the user's message?
    2.  **Sentiment:** What is the underlying emotion (e.g., frustrated, nervous, confident)?
    3.  **Empathy:** Does the message consider the other person's feelings?

    After your analysis, provide one single, actionable tip in a "Suggestion:" section to help the user communicate more effectively. Keep the feedback concise and encouraging.

    Text to analyze: "{text_to_analyze}"
    """
    try:
        response = ollama.chat(
            model='gemma3n:e2b',
            messages=[{'role': 'user', 'content': prompt}],
        )
        return response['message']['content']
    except Exception as e:
        st.error("Could not connect to Ollama. Is it running in a separate terminal? (ollama serve)")
        return f"Error communicating with Ollama: {e}"


# --- Main App UI ---
st.set_page_config(layout="wide")
st.title("🎙️ The Offline Empathy Coach (Ollama Edition)")
st.markdown("Practice conversations and get private feedback. **Transcription and AI analysis run 100% locally.**")

# --- Main Columns ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Record Your Message")
    audio_file = st.file_uploader(
        "Upload an audio file (WAV, MP3) or record a new one:", 
        type=["wav", "mp3", "m4a"]
    )
    st.markdown("OR")
    audio_bytes_from_mic = st.audio_input("Click the microphone to record, then click stop when finished.")

    final_audio_bytes = None
    if audio_bytes_from_mic:
        final_audio_bytes = audio_bytes_from_mic.read()
    elif audio_file:
        final_audio_bytes = audio_file.read()

    if final_audio_bytes:
        with st.spinner("Transcribing audio..."):
            transcribed_text = transcribe_audio(final_audio_bytes)

        if "Error" not in transcribed_text:
            st.info(f"**Transcribed Text:** {transcribed_text}")

            with st.spinner("Your coach is thinking..."):
                feedback = get_empathy_feedback(transcribed_text)
                st.session_state.feedback = feedback
        else:
            st.error(transcribed_text)

with col2:
    st.subheader("AI Feedback")
    st.info(st.session_state.get("feedback", "Your feedback will appear here."))

st.markdown("---")
st.info("This app uses `faster-whisper` for local transcription and `Ollama` to run Gemma 2B locally. Your data never leaves your computer.", icon="🔒")
