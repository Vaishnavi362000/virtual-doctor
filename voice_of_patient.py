#Step 1: Record audio
import logging
import speech_recognition as sr
from pyaudio import PyAudio
from pydub import AudioSegment
from io import BytesIO


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    logging.info("Recording audio...")
    """
    Simplified audio recording function
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone(sample_rate=16000) as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete...")

            wav_data = BytesIO(audio_data.get_wav_data())
            audio_segment = AudioSegment.from_wav(wav_data)
            audio_segment.export(file_path, format="mp3", bitrate="192k")
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"Error recording audio: {e}")
            
audio_filepath = "patient_audio.mp3"
#record_audio(file_path=audio_filepath)
        

#Step 2: Convert audio to text
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    client = Groq(api_key=GROQ_API_KEY)

    audio_file = open(audio_filepath, "rb")
    transcription = client.audio.transcriptions.create(
        model=stt_model,    
        file=audio_file,
        language="en",
    )

    return transcription.text
            
