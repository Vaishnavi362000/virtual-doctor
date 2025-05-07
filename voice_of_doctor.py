#step 1: set up text to speech(gtts & levenlabs)
import os
from gtts import gTTS
from dotenv import load_dotenv
import tempfile
from pydub import AudioSegment

# Load environment variables from .env file
load_dotenv()

def text_to_speech_old(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)

input_text = "Hello, how are you?"
output_filepath = "output.mp3"
#text_to_speech_old(input_text, output_filepath)

#Step 2: Convert text to speech using elevenlabs
import elevenlabs
from elevenlabs.client import ElevenLabs

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def text_to_speech_elevenlabs_old(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        voice="Aria",
        text=input_text,
        model="eleven_turbo_v2",
        output_format="mp3_22050_32",
    )
    elevenlabs.save(audio, output_filepath)

input_text = "Hello, how are you?"
output_filepath = "elevenlabs_output.mp3"
#text_to_speech_elevenlabs_old(input_text, output_filepath)

#Step 3

import subprocess
import platform

def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)

    # Convert MP3 to WAV
    wav_filepath = tempfile.mktemp(suffix=".wav")
    audio_segment = AudioSegment.from_mp3(output_filepath)
    audio_segment.export(wav_filepath, format="wav")

    os_name = platform.system()
    try:
        if os_name == "Darwin":
            subprocess.run(("afplay", wav_filepath))
        elif os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(("aplay", wav_filepath))
        else:
            raise OSError("Unsupported OS")
    except Exception as e:
        print(f"Error playing audio: {e}")
            

input_text = "Hello, i am the voice of the virtual doctor. How can i help you today for autopiloting your health?"
output_filepath = "output_autoplay.mp3"
#text_to_speech_with_gtts(input_text, output_filepath)

def text_to_speech_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        voice="Aria",
        text=input_text,
        model="eleven_turbo_v2",
        output_format="mp3_22050_32",
    )
    elevenlabs.save(audio, output_filepath)
    # Convert MP3 to WAV
    # Convert MP3 to WAV
    wav_filepath = tempfile.mktemp(suffix=".wav")
    audio_segment = AudioSegment.from_mp3(output_filepath)
    audio_segment.export(wav_filepath, format="wav")

    os_name = platform.system()
    try:
        if os_name == "Darwin":
            subprocess.run(("afplay", wav_filepath))
        elif os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(("aplay", wav_filepath))
        else:
            raise OSError("Unsupported OS")
    except Exception as e:
        print(f"Error playing audio: {e}")

input_text = "Hello, i am the voice of the virtual doctor. How can i help you today for autopiloting your health?"
output_filepath = "elevenlabs_output_autoplay.mp3"
text_to_speech_elevenlabs(input_text, output_filepath)