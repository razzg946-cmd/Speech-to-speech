import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from audio_recorder_streamlit import audio_recorder
import edge_tts
import asyncio
import tempfile
import os

st.set_page_config(
    page_title="Rvoice - Voice Translator",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Rvoice - Voice to Voice Translator")

languages = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml",
    "Kannada": "kn",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Marathi": "mr"
}

source_lang = st.selectbox(
    "Input Language",
    list(languages.keys())
)

target_lang = st.selectbox(
    "Output Language",
    list(languages.keys())
)

voice_gender = st.selectbox(
    "Voice",
    ["Female", "Male"]
)

st.write("### 🎤 Record Voice")

audio_bytes = audio_recorder(
    pause_threshold=2.0,
    sample_rate=44100
)

if audio_bytes:

    st.audio(audio_bytes)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_bytes)
        audio_path = f.name

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(
            audio_data,
            language=languages[source_lang]
        )

        st.success("Recognized Text")
        st.write(text)

        translated = GoogleTranslator(
            source="auto",
            target=languages[target_lang]
        ).translate(text)

        st.success("Translated Text")
        st.write(translated)

        if voice_gender == "Female":
            voice = "en-US-JennyNeural"
        else:
            voice = "en-US-GuyNeural"

        async def generate_voice():
            output_file = "translated.mp3"

            communicate = edge_tts.Communicate(
                translated,
                voice
            )

            await communicate.save(output_file)

            return output_file

        mp3_file = asyncio.run(generate_voice())

        st.audio(mp3_file)

        with open(mp3_file, "rb") as f:
            st.download_button(
                "⬇ Download MP3",
                f,
                file_name="rvoice_translation.mp3",
                mime="audio/mp3"
            )

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)