import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

import base64

#image_path = 'acne.jpg'
#image_file = open(image_path, 'rb')
#encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

def encode_image(image_path):
    image_file = open(image_path, 'rb')
    return base64.b64encode(image_file.read()).decode('utf-8')

#Step 1: Analyze image with query

from groq import Groq

model = "llama-3.2-90b-vision-preview"
query = "What is in this image?"

def analyze_image_with_query(model, query, encoded_image):
    client = Groq(api_key=GROQ_API_KEY)
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}"
                    }
                }
            ]
        }
    ]
    chat_completion = client.chat.completions.create(
    model=model,
    messages=messages,
    )

    return chat_completion.choices[0].message.content






















