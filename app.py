import streamlit as st
import whisper
from groq import Groq
from gtts import gTTS
import os
from streamlit_mic_recorder import mic_recorder

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
    st.write("Record your voice or upload an audio file to interact with the chatbot.")

    # Option to record audio or upload a file
    option = st.radio("Choose an option:", ("Record Audio", "Upload Audio File"))

    audio_file = None

    if option == "Record Audio":
        # Use streamlit-mic-recorder to record audio
        audio = mic_recorder(
            start_prompt="Start recording",
            stop_prompt="Stop recording",
            just_once=False,
            use_container_width=False
        )

        if audio and 'audio' in audio and audio['audio'] is not None:
            audio_file = audio['audio']
            with open("recorded_audio.wav", "wb") as f:
                f.write(audio['audio'])  # Ensure we're writing the bytes
            st.success("Audio recorded successfully!")

        elif audio and 'audio' not in audio:
            st.warning("Recording not completed yet. Please try again.")

    elif option == "Upload Audio File":
        # Use file uploader to upload an audio file
        uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])
        if uploaded_file is not None:
            audio_file = uploaded_file
            st.success("Audio file uploaded successfully!")

    if audio_file is not None:
        st.write("Transcribing audio...")
        transcribed_text = whisper_transcribe(audio_file)
        st.write(f"Transcribed Text: {transcribed_text}")

        st.write("Generating response...")
        response_text = generate_response(transcribed_text)
        st.write("Response from the chatbot:")
        st.text_area("LLM Output", response_text, height=150)

        st.write("Converting response to speech...")
        speech_file = text_to_speech(response_text)
        audio_bytes_response = open(speech_file, "rb").read()
        st.audio(audio_bytes_response, format="audio/mp3")

if __name__ == "__main__":
    main()
