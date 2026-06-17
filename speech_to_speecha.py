import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from audio_recorder_streamlit import audio_recorder
import edge_tts
import asyncio
import tempfile
import os

# -----------------------

# Page Config

# -----------------------

st.set_page_config(
page_title="Rvoice - Voice Translator",
page_icon="🎙️",
layout="centered"
)

# -----------------------

# Header

# -----------------------

st.title("🎙️ Rvoice")
st.subheader("Voice to Voice Translator")

# -----------------------

# Languages

# -----------------------

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

# -----------------------

# Language Selection

# -----------------------

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

# -----------------------

# Voice Mapping

# -----------------------

female_voices = {
"English": "en-US-JennyNeural",
"Hindi": "hi-IN-SwaraNeural",
"Tamil": "ta-IN-PallaviNeural",
"Telugu": "te-IN-ShrutiNeural"
}

male_voices = {
"English": "en-US-GuyNeural",
"Hindi": "hi-IN-MadhurNeural",
"Tamil": "ta-IN-ValluvarNeural",
"Telugu": "te-IN-MohanNeural"
}

# -----------------------

# Record Audio

# -----------------------

st.markdown("### 🎤 Record Voice")

audio_bytes = audio_recorder(
pause_threshold=2.0,
sample_rate=44100
)

# -----------------------

# Process Audio

# -----------------------

if audio_bytes:

    st.audio(audio_bytes)

    if st.button("▶ Convert"):
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

            voice = "en-US-JennyNeural" if voice_gender == "Female" else "en-US-GuyNeural"

            async def generate():
                file = "translated.mp3"
                tts = edge_tts.Communicate(translated, voice)
                await tts.save(file)
                return file

            mp3 = asyncio.run(generate())

            with open(mp3, "rb") as f:
                st.audio(f.read())

            st.download_button(
                "⬇ Download MP3",
                open(mp3, "rb"),
                file_name="rvoice.mp3",
                mime="audio/mp3"
            )

        except Exception as e:
            st.error(e)

        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)


# -----------------------

# Footer

# -----------------------

st.markdown("---")

st.markdown(
""" <div style='text-align:center'> <h3>🎙️ Rvoice</h3> <p><b>Founder:</b> Raj Gupta</p> </div>
""",
unsafe_allow_html=True
)
