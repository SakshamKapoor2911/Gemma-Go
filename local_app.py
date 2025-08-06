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


def get_learning_feedback_stream(text_to_analyze, language="English"):
    """Streams feedback from Ollama to the frontend as it is generated."""
    prompt = f"""
    You are a supportive teacher helping a student improve their writing and speaking skills.
    The student is learning in '{language}'. Your feedback should be in '{language}'.

    IMPORTANT: Read the text carefully word by word. DO NOT HALLUCINATE ERRORS. DO NOT INVENT ERRORS.

    The text is: "{text_to_analyze}"

    First, perform a "Grammar & Spelling Check" on the text above:
    - Compare each word against standard spelling and grammar
    - If and ONLY if you find ACTUAL errors, list them specifically
    - If NO errors exist, you MUST write exactly: "Grammar and spelling check: No errors found."

    Then, provide a structured, encouraging report under the heading "Teacher's Feedback" focusing on:
    1. **Clarity & Organization:** How clear and well-structured are the ideas?
    2. **Writing Style:** Comment on word choice and expression.
    3. **Impact:** How effective is the writing/speech for its purpose?

    End with a "Suggestion:" section containing one specific, actionable tip to help the student improve.
    Keep your feedback positive and encouraging.
    """
    try:
        response_stream = ollama.chat(
            model='gemma3n:e4b',
            messages=[{'role': 'user', 'content': prompt}],
            stream=True
        )
        for chunk in response_stream:
            if 'message' in chunk and 'content' in chunk['message']:
                yield chunk['message']['content']
    except Exception as e:
        yield f"Error communicating with Ollama: {e}"


# --- Main App UI ---
st.set_page_config(layout="wide")
st.title("📚 The Offline Learning Coach")
st.markdown("For students with limited access to teachers. Practice writing essays or speaking, and get private feedback to improve your skills. **100% free and offline.**")

# --- Main Columns ---

col1, col2 = st.columns(2)

# Create a placeholder in the right column for feedback
with col2:
    st.subheader("Teacher's Feedback")
    feedback_placeholder = st.empty()
    feedback_placeholder.info("Your feedback will appear here after submission.")

with col1:
    st.subheader("Submit Your Speech or Essay")
    # Language Selector
    language = st.selectbox(
        "In which language would you like feedback?",
        ("English", "Spanish", "French", "German", "Hindi", "Mandarin Chinese", "Arabic")
    )
    st.markdown("---")
    # Input Method Tabs
    input_method = st.radio("Choose your input method:", ("Speak", "Write"))
    text_to_process = None
    if input_method == "Speak":
        audio_file = st.file_uploader("Upload an audio file:", type=["wav", "mp3", "m4a"])
        st.markdown("OR")
        audio_bytes_from_mic = st.audio_input("Click the microphone to record your speech:")
        final_audio_bytes = None
        if audio_bytes_from_mic:
            final_audio_bytes = audio_bytes_from_mic.read()
        elif audio_file:
            final_audio_bytes = audio_file.read()
        if final_audio_bytes:
            with st.spinner("Transcribing audio..."):
                text_to_process = transcribe_audio(final_audio_bytes)
    elif input_method == "Write":
        # Use session state to persist text input and ensure correct value is processed
        if "text_input_value" not in st.session_state:
            st.session_state.text_input_value = ""
        text_area_input = st.text_area(
            "Paste or type your essay/speech here:",
            value=st.session_state.text_input_value,
            height=250,
            key="text_area"
        )
        # Update session state with current input
        st.session_state.text_input_value = text_area_input
        # Set the text_to_process variable only when the button is pressed
        text_to_process = text_area_input if text_area_input else None
    # Add a submit button to trigger the analysis
    if st.button("Get Feedback"):
        # Process the text if we have any
        if text_to_process and "Error" not in text_to_process:
            st.info(f"**Submitted Text:** {text_to_process}")
            with st.spinner("Your teacher is reviewing..."):
                feedback_placeholder.empty()
                feedback_placeholder.write_stream(get_learning_feedback_stream(text_to_process, language))
        elif text_to_process and "Error" in text_to_process:
            st.error(text_to_process)
            feedback_placeholder.error(text_to_process)
        elif input_method == "Speak" and not text_to_process:
            warning_msg = "Please record or upload an audio file before getting feedback."
            st.warning(warning_msg)
            feedback_placeholder.warning(warning_msg)
        else:
            warning_msg = "Please enter some text or record audio to get feedback."
            st.warning(warning_msg)
            feedback_placeholder.warning(warning_msg)

st.markdown("---")
st.info("This app uses `faster-whisper` for local transcription and `Ollama` to run Gemma 3n locally. Your data never leaves your computer.", icon="🔒")
