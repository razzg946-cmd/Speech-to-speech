import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr
import edge_tts
import asyncio
from io import BytesIO

st.set_page_config(page_title="Rvoice", page_icon="🎙️")

st.title("🎙️ RVOICE - Voice to Voice")

# ---------------- LANGUAGE ----------------
lang_map = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "French": "fr"
}

input_lang = st.selectbox("Input Language Select", list(lang_map.keys()))
output_lang = st.selectbox("Output Language Select", list(lang_map.keys()))

# ---------------- AUDIO ----------------
audio_file = st.file_uploader("Voice Record (Upload Audio)", type=["wav"])

# ---------------- BUTTON ----------------
if st.button("▶ Convert & Translate"):

# ---------------- SPEECH TO TEXT ----------------
def speech_to_text(audio):
    r = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        data = r.record(source)
    return r.recognize_google(data, language=lang_map[input_lang])

# ---------------- TEXT TO SPEECH ----------------
async def text_to_voice(text):
    communicate = edge_tts.Communicate(text, "en-US-JennyNeural")
    audio = BytesIO()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio.write(chunk["data"])

    audio.seek(0)
    return audio

# ---------------- BUTTON ----------------
if st.button("▶ Convert & Translate"):

    if audio_file is None:
        st.warning("Upload audio first")
    else:
        with st.spinner("Processing..."):

            text = speech_to_text(audio_file)
            st.subheader("Recognized Text")
            st.write(text)

            translated = GoogleTranslator(
                source=lang_map[input_lang],
                target=lang_map[output_lang]
            ).translate(text)

            st.subheader("Translated Text")
            st.write(translated)

            audio_out = asyncio.run(text_to_voice(translated))

        st.subheader("Output Voice")
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
