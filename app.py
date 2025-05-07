import gradio as gr
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from brain_of_doctor import analyze_image_with_query, encode_image
from voice_of_patient import record_audio, transcribe_with_groq
from voice_of_doctor import text_to_speech_elevenlabs, text_to_speech_with_gtts


system_prompt = """
Understand user queries about health (via text, audio, or image).

Convert voice to clear text and analyze it.

Respond with accurate, safe, and supportive medical guidance.

Never provide a final diagnosis or prescribe medicine.

If symptoms are serious or unclear, advise the user to consult a real doctor or visit a hospital.

You can:

Explain symptoms and possible causes.

Suggest over-the-counter remedies or lifestyle changes.

Help with appointment scheduling, reminders, and general health tips.

Analyze images (if uploaded) like rashes, reports, or scans — but always remind users it's not a replacement for a clinical opinion.

Always respond clearly and kindly, using simple terms the user can understand.
"""

def process_inputs(audio_filepath, image_filepath):
    #transcribe the audio
    speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.getenv("GROQ_API_KEY"), audio_filepath=audio_filepath, stt_model="whisper-large-v3")
    if image_filepath:
        doctor_response = analyze_image_with_query(query=system_prompt + speech_to_text_output, encoded_image=encode_image(image_filepath), model="llama-3.2-11b-vision-preview")
    else:
        doctor_response = "No image provided for analysis"
    
    voice_of_doctor_response = text_to_speech_elevenlabs(input_text=doctor_response, output_filepath="Final_response.mp3")
    return speech_to_text_output, doctor_response, voice_of_doctor_response
#create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath"),
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("Final_response.mp3"),
    ],
    title="Virtual Doctor",
    description="Ask the doctor anything about your health",
)

# Get port from environment variable for Render deployment
port = int(os.environ.get("PORT", 7860))
iface.launch(server_name="0.0.0.0", server_port=port, debug=True)

