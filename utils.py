import os
import mimetypes
import base64
from google import genai
from google.genai import types

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.Client(api_key=GOOGLE_API_KEY)
model = "gemini-2.0-flash-preview-image-generation"

def get_file_part(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    return types.Part.from_bytes(mime_type=mimetypes.guess_type(file_path)[0], data=data)

def generate_image(image_path, prompt):
    contents = [
        types.Content(
            role="user",
            parts=[
                get_file_part(image_path),
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    config = types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
        response_mime_type="text/plain",
    )

    client = genai.Client()
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        if (
            chunk.candidates and
            chunk.candidates[0].content and
            chunk.candidates[0].content.parts and
            chunk.candidates[0].content.parts[0].inline_data
        ):
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            return inline_data.data, inline_data.mime_type
    return None, None

def apply_custom_css():
    import streamlit as st
    with open("style.css", "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
