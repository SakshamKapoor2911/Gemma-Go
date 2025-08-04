from audio_processor import record_and_transcribe
from gemma_coach import get_empathy_feedback

def run_coaching_session():
    # Step 1: Record and Transcribe
    transcribed_text = record_and_transcribe()

    # Step 2: Get feedback from Gemma
    if transcribed_text:
        print("\n--- Getting Feedback from Your Empathy Coach ---")
        feedback = get_empathy_feedback(transcribed_text)
        print(feedback)
    else:
        print("No text was transcribed. Please try again.")

if __name__ == '__main__':
    run_coaching_session()
