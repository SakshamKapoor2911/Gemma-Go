# Empathy Coach

This project is a privacy-first Empathy Coach that provides feedback on your speech using local AI models. It helps you practice conversations by analyzing your communication for clarity, sentiment, and empathy, running 100% on your own machine.

## Core Features

-   **100% Local & Private**: Your voice data and conversations never leave your computer.
-   **Fast, Accurate Transcription**: Uses `faster-whisper` to transcribe your speech locally.
-   **Advanced Empathy Analysis**: Leverages a local Gemma model via Ollama to provide nuanced feedback.
-   **Multiple Interfaces**: Choose between an interactive Streamlit web app or a command-line interface.

## Project Structure & How to Run

This repository contains three different ways to run the Empathy Coach.

### 1. `local_app.py` (Recommended Web App)

This is the main Streamlit application. It provides a user-friendly interface for either uploading an audio file or recording directly from your microphone.

**To run:**
1.  Make sure Ollama is running in a separate terminal (`ollama serve`).
2.  Run the Streamlit app:
    ```bash
    streamlit run local_app.py
    ```

### 2. `app.py` (Alternative Web App)

This is another version of the Streamlit application. It offers a slightly different UI, with a dedicated microphone input and a separate text area for manual entry.

**To run:**
1.  Make sure Ollama is running.
2.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

### 3. `main.py` (Command-Line Version)

For users who prefer the terminal, `main.py` provides a simple, command-line-based coaching session. It will record audio from your default microphone, transcribe it, and print the AI feedback directly to the console.

**To run:**
1.  Make sure Ollama is running.
2.  Run the Python script:
    ```bash
    python main.py
    ```

## Setup and Requirements

1.  **Install Ollama**: Make sure you have [Ollama](https://ollama.com/) installed and have pulled the model used in the scripts (e.g., `gemma:2b`).

2.  **Start the Ollama Server**: Open a terminal and run the following command. Leave it running in the background.
    ```bash
    ollama serve
    ```

3.  **Install Python Dependencies**: Install the required Python packages from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```
    *Note: `faster-whisper` may require you to install a compatible version of PyTorch (`torch`).*

## Troubleshooting

If you see errors like "llama runner process has terminated" or "Could not connect to Ollama," it usually means one of the following:

1.  **Ollama is not running**: Ensure `ollama serve` is active in a separate terminal.
2.  **Model not pulled**: Make sure you have the correct model installed (e.g., `ollama pull gemma:2b`). Check the model name inside the script you are running.
3.  **System Resources**: Your computer may not have enough RAM to run the model. Try using a smaller model by changing the `model` parameter in the script's `ollama.chat` call.
4.  **Corrupted Model**: Try removing and re-pulling the model: `ollama rm gemma:2b` then `ollama pull gemma:2b`.
