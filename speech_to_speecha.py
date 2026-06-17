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

# Select Language

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

    if st.button("▶ Convert & Translate"):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as f:

            f.write(audio_bytes)
            audio_path = f.name

    recognizer = sr.Recognizer()

    try:

        # Speech To Text
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(
            audio_data,
            language=languages[source_lang]
        )

        st.success("✅ Recognized Text")
        st.write(text)

        # Translation
        translated = GoogleTranslator(
            source="auto",
            target=languages[target_lang]
        ).translate(text)

        st.success("🌍 Translated Text")
        st.write(translated)

        # Voice Selection
        if voice_gender == "Female":
            voice = female_voices.get(
                target_lang,
                "en-US-JennyNeural"
            )
        else:
            voice = male_voices.get(
                target_lang,
                "en-US-GuyNeural"
            )

        # Text To Speech
        async def generate_voice():

            output_file = "translated.mp3"

            communicate = edge_tts.Communicate(
                translated,
                voice
            )

            await communicate.save(output_file)

            return output_file

        mp3_file = asyncio.run(
            generate_voice()
        )

        st.subheader("🔊 Output Voice")

        with open(mp3_file, "rb") as audio_file:
            audio_bytes_output = audio_file.read()

        st.audio(audio_bytes_output)

        st.download_button(
            label="⬇ Download MP3",
            data=audio_bytes_output,
            file_name="rvoice_translation.mp3",
            mime="audio/mpeg"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")

    finally:

        if os.path.exists(audio_path):
            os.remove(audio_path)


# -----------------------

# Footer

# -----------------------

st.markdown("---")

st.markdown(
""" <div style='text-align:center'> <h3>🎙️ Rvoice</h3> <p>Founder: Raj Gupta</p> </div>
""",
unsafe_allow_html=True
)
