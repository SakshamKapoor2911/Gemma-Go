# The Offline Learning Coach

This project is a privacy-first Learning Coach designed to help students in low-income or underdeveloped areas improve their writing and speaking skills. Once downloaded, it runs 100% offline, providing free access to AI-powered educational feedback without needing an internet connection.

## Core Mission & Features

The goal is to increase accessibility to learning for students who lack regular access to teachers.

-   **100% Local, Private, and Free**: After initial setup, the app runs entirely on the user's device. No internet required, no data shared.
-   **Supportive Educational Feedback**: Uses a local Gemma model via Ollama to provide structured feedback on essays and speeches.
-   **Multi-Language Support**: Gemma 3n supports over 140 languages, allowing students to get feedback in their native or learning language.
-   **Speech & Text Input**: Users can either record their speech (which is transcribed locally) or type/paste their essays directly.
-   **Cross-Platform Potential**: Can be packaged to run on low-cost computers or even mobile devices, making it highly accessible.

## Project Structure & How to Run

This repository contains multiple ways to run the Learning Coach. **`local_app.py` is the main, recommended version for submission.**

The other files (`app.py`, `main.py`) were developed for a different feature focused on analyzing audio characteristics like pitch, pauses, and confidence to help users improve their oratory skills. However, we encountered a technical challenge, as sending raw audio directly to Gemma 3n via Ollama is not yet supported.

Our plan is to find a workaround for this limitation and integrate these advanced oratory-coaching features in a future release.

### 1. `local_app.py` (Recommended Web App)

This is the main Streamlit application. It provides a user-friendly interface for submitting text or audio and selecting a language for feedback.

**To run:**
1.  Make sure Ollama is running in a separate terminal (`ollama serve`).
2.  Run the Streamlit app:
    ```bash
    streamlit run local_app.py
    ```

### 2. `app.py` & `main.py` (Alternative Interfaces)

These files provide alternative UIs. `app.py` is another Streamlit version, and `main.py` is a simple command-line tool.

**To run:**
```bash
# For the alternative web app
streamlit run app.py

# For the command-line version
python main.py
```

## Setup and Requirements

To ensure the project runs correctly, please follow these steps. It is recommended to use **Python 3.9 or newer**.

1.  **Create a Virtual Environment**: It's best practice to create a dedicated environment for the project.
    ```bash
    # Create the environment
    python -m venv venv

    # Activate it (Windows)
    .\\venv\\Scripts\\activate

    # Activate it (macOS/Linux)
    source venv/bin/activate
    ```

2.  **Install Ollama**: Make sure you have [Ollama](https://ollama.com/) installed and running on your system.

3.  **Download the AI Model**: Pull the Gemma model required for the application. This only needs to be done once.
    ```bash
    ollama pull gemma3n:e4b
    ```
    *Note: The recommended `local_app.py` uses `gemma3n:e4b` for general learning feedback. The alternative interfaces use a different model for empathy-focused analysis.*

4.  **Start the Ollama Server**: Open a separate terminal and run the following command. Leave this running in the background whenever you use the app.
    ```bash
    ollama serve
    ```

5.  **Install Python Dependencies**: Install the required Python packages using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```
    *Note: `faster-whisper` requires PyTorch. If the installation fails, you may need to install `torch` and `torchaudio` separately by following the official instructions at [pytorch.org](https://pytorch.org/).*

## Design Decisions & Future Work

A core challenge was processing audio reliably.

-   **The Challenge**: While Gemma 3n can natively process audio, creating a stable pipeline to get raw audio from a web browser to the local model via Ollama is complex and not yet supported. This prevented us from implementing our desired oratory-coaching features (analyzing pitch, tone, etc.).
-   **The Solution**: To ensure the app is robust and immediately useful, we adopted a two-step process for the main application:
    1.  **Transcribe**: Use `faster-whisper` to reliably convert speech into text. This is excellent for analyzing the *content* of a speech.
    2.  **Analyze**: Send the clean text to Gemma for educational analysis.
-   **Future Work**: Our priority is to find a workaround for the direct audio pipeline. This would unlock feedback on pronunciation, tone, and pacing, which would be a powerful addition to the current features.

This project uses the text-based approach for stability, making it a powerful tool for improving writing and speech composition skills right now.
