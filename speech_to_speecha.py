import streamlit as st
from streamlit_mic_recorder import mic_recorder
from deep_translator import GoogleTranslator
import speech_recognition as sr
import edge_tts
import asyncio
from io import BytesIO

st.set_page_config(page_title="Rvoice", page_icon="🎙️")

st.title("🎙️ RVOICE - Live Voice to Voice")

# ---------------- LANGUAGE ----------------
lang_map = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Punjabi": "pa",
    "Urdu": "ur"
}

input_lang = st.selectbox("Input Language Select", list(lang_map.keys()))
output_lang = st.selectbox("Output Language Select", list(lang_map.keys()))

# ---------------- MIC RECORD ----------------
st.subheader("🎤 Speak Here (Click to Record)")
audio = mic_recorder(start_prompt="🎙️ Start Recording", stop_prompt="⏹ Stop Recording")

# ---------------- SPEECH TO TEXT ----------------
def speech_to_text(audio_bytes):
    r = sr.Recognizer()
    audio_file = sr.AudioFile(audio_bytes)
    with audio_file as source:
        data = r.record(source)
    return r.recognize_google(data, language=lang_map[input_lang])

# ---------------- TEXT TO VOICE ----------------
async def text_to_voice(text):
    communicate = edge_tts.Communicate(text, "en-US-JennyNeural")
    audio = BytesIO()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio.write(chunk["data"])

    audio.seek(0)
    return audio

# ---------------- PROCESS BUTTON ----------------
if audio:

    st.success("Audio captured!")

    if st.button("▶ Convert & Translate"):

        with st.spinner("Processing..."):

            # Convert voice → text
            text = speech_to_text(audio["bytes"])
            st.subheader("Recognized Text")
            st.write(text)

            # Translate
            translated = GoogleTranslator(
                source=lang_map[input_lang],
                target=lang_map[output_lang]
            ).translate(text)

            st.subheader("Translated Text")
            st.write(translated)

            # Text → Voice
            audio_out = asyncio.run(text_to_voice(translated))

        st.subheader("🔊 Output Voice")
        st.audio(audio_out, format="audio/mp3")

        st.download_button(
            "⬇ Download MP3",
            data=audio_out,
            file_name="rvoice.mp3",
            mime="audio/mp3"
        )

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("**RVOICE - Founder Raj Gupta**")
