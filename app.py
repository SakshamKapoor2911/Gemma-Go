import streamlit as st
import ollama
import tempfile
from faster_whisper import WhisperModel


# --- Application State ---
st.session_state.setdefault("feedback", "Your feedback will appear here.")
st.session_state.setdefault("transcript_debug", "")

# --- AI and Audio Logic ---

@st.cache_resource
def load_whisper_model():
    """Loads the Whisper model once and caches it."""
    return WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(audio_file):
    model = load_whisper_model()
    # Save audio to temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        temp_audio.write(audio_file.read())
        temp_path = temp_audio.name
    try:
        result = model.transcribe(temp_path, language="en")
        segments = list(result[0])
        text = " ".join([segment.text for segment in segments if segment.text.strip()])
        return text
    except Exception as e:
        st.error(f"Transcription error: {str(e)}")
        return ""


def get_empathy_feedback(text_to_analyze):
    prompt = f"""
    You are an expert empathy and communication coach. Your task is to analyze the following text and provide gentle, constructive feedback.
    Analyze the text from three perspectives: 1. Clarity, 2. Sentiment, 3. Empathy.
    After your analysis, provide one single, actionable tip in a "Suggestion:" section. Keep the feedback concise and encouraging.
    Text to analyze: "{text_to_analyze}"
    """
    try:
        response = ollama.chat(model='gemma:2b', messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        return f"Error communicating with the model: {e}"




# --- Main App UI ---
st.set_page_config(layout="wide")
st.title("🎙️ The Offline Empathy Coach")
st.markdown("Practice difficult conversations and get private, instant feedback powered by Gemma.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Record Yourself")
    st.markdown("Click the microphone to record, then stop when finished.")

    # New audio input widget
    audio_file = st.audio_input("Record your speech", key="speech_input")

    transcript_debug = st.empty()

    if audio_file is not None:
        st.audio(audio_file, format="audio/wav")
        with st.spinner("Transcribing..."):
            text = transcribe_audio(audio_file)
        if text:
            st.success("Transcription complete!")
            transcript_debug.info(f"Transcribed: {text}")
            with st.spinner("Getting feedback..."):
                feedback = get_empathy_feedback(text)
                st.session_state.feedback = feedback
        else:
            transcript_debug.warning("No speech was detected. Please try again and speak clearly.")

    # Manual input option
    st.markdown("### Can't get recording to work?")
    manual_text = st.text_area("Type what you want to analyze here:", 
                            value="", height=100, 
                            placeholder="Type your message here if you can't use the microphone...")

    if st.button("Analyze Text"):
        if manual_text:
            with st.spinner("Your coach is thinking..."):
                feedback = get_empathy_feedback(manual_text)
                st.session_state.feedback = feedback
        else:
            st.warning("Please enter some text to analyze.")

    st.markdown("_Note: Transcription and AI analysis run 100% locally on your machine._")

with col2:
    st.subheader("AI Feedback")
    st.info(st.session_state.feedback)
