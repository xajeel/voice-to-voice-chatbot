import streamlit as st
import whisper
from groq import Groq
from gtts import gTTS
import os
import tempfile

# Get the Groq API key from Streamlit secrets
GROQ_API = st.secrets["groq"]["api_key"]

# Function for Whisper transcription
def whisper_transcribe(audio_file):
    model = whisper.load_model("base")
    text = model.transcribe(audio_file)
    return text['text']

# Function to generate response using Groq API
def generate_response(prompt):
    client = Groq(client=GROQ_API)
    chat_ = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192"
    )
    return chat_.choices[0].message.content

# Function for text-to-speech conversion using gTTS
def text_to_speech(text, output='response.mp3'):
    tts = gTTS(text=text, lang='en')
    tts.save(output)
    return output

# Main Streamlit app
def main():
    st.title("Voice-to-Voice Chatbot")
    st.write("You can either record your voice or upload an audio file, and the app will transcribe, respond, and convert the response to speech.")

    # Option to record audio or upload a file
    option = st.radio("Choose an option:", ("Record Voice", "Upload MP3 File"))

    audio_file = None
    if option == "Record Voice":
        # Record audio
        st.write("Record your voice:")
        audio_file = st.audio_recorder(format="audio/wav")
    elif option == "Upload MP3 File":
        # Upload audio file
        st.write("Upload an MP3 file:")
        audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

    if audio_file is not None:
        # Save the audio file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_file.close()

            # Transcribe the audio file using Whisper
            st.write("Transcribing audio...")
            transcribed_text = whisper_transcribe(tmp_file.name)
            st.write(f"Transcribed Text: {transcribed_text}")

            # Generate a response using Groq API
            st.write("Generating response...")
            response_text = generate_response(transcribed_text)
            st.write(f"Response: {response_text}")

            # Convert the response to speech
            st.write("Converting response to speech...")
            response_audio_file = text_to_speech(response_text)
            audio_bytes = open(response_audio_file, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")

if __name__ == "__main__":
    main()
