import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import os
from faster_whisper import WhisperModel

def record_audio(fs=44100, seconds=5):
    """Records audio from the default microphone."""
    print("Recording...")
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")
    return recording, fs

def save_audio_to_temp_file(recording, fs):
    """Saves the recorded audio to a temporary WAV file."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(temp_file.name, fs, recording)
    return temp_file.name

def transcribe_audio(file_path):
    """Transcribes the audio file using faster-whisper."""
    model = WhisperModel("base.en", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(file_path, beam_size=5, language="en")
    transcribed_text = " ".join([segment.text for segment in segments])
    return transcribed_text

def record_and_transcribe():
    """Records audio, saves it, transcribes it, and cleans up."""
    recording, fs = record_audio()
    temp_file_path = save_audio_to_temp_file(recording, fs)
    
    try:
        transcribed_text = transcribe_audio(temp_file_path)
        print(f"\nTranscribed Text: {transcribed_text}")
        return transcribed_text
    finally:
        os.remove(temp_file_path)
