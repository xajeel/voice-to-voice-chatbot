import streamlit as st
import whisper
from groq import Groq
from gtts import gTTS

# Initialize the Groq API key
GROQ_API = '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'

# Define function for Whisper transcription
def whisper_transcribe(audio_file):
    model = whisper.load_model("base")
    text = model.transcribe(audio_file)
    return text['text']

# Define function to generate response using Groq API
def generate_response(prompt):
    client = Groq(client=GROQ_API)
    chat_ = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192"
    )
    return chat_.choices[0].message.content

# Define function for text-to-speech conversion using gTTS
def text_to_speech(text, output='response.mp3'):
    tts = gTTS(text=text, lang='en')
    tts.save(output)
    return output

# Main function for Streamlit app
def main():
    st.title("Voice-to-Voice Chatbot")
    st.write("Upload an audio file, and the app will transcribe, respond, and convert the response to speech.")

    # File uploader for audio input
    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

    if audio_file is not None:
        st.write("Transcribing audio...")
        # Transcribe audio using Whisper
        transcribed_text = whisper_transcribe(audio_file)
        st.write(f"Transcribed Text: {transcribed_text}")

        st.write("Generating response...")
        # Generate response using Groq API
        response_text = generate_response(transcribed_text)
        st.write(f"Response: {response_text}")

        st.write("Converting response to speech...")
        # Convert the response text to speech using gTTS
        speech_file = text_to_speech(response_text)
        
        # Play the audio file in Streamlit
        audio_bytes = open(speech_file, "rb").read()
        st.audio(audio_bytes, format="audio/mp3")

# Run the app
if __name__ == "__main__":
    main()
