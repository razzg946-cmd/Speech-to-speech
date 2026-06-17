import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr
import edge_tts
import asyncio
from io import BytesIO

st.set_page_config(page_title="Rvoice", page_icon="🎙️")

st.title("🎙️ RVOICE - Voice to Voice")

# ---------------- LANGUAGE MAP (INDIA + GLOBAL) ----------------
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
    "Urdu": "ur",
    "French": "fr"
}

# ---------------- LANGUAGE SELECT ----------------
input_lang = st.selectbox("Input Language Select", list(lang_map.keys()))
output_lang = st.selectbox("Output Language Select", list(lang_map.keys()))

# ---------------- AUDIO UPLOAD ----------------
audio_file = st.file_uploader("Voice Record (Upload Audio)", type=["wav"])


# ---------------- SPEECH TO TEXT ----------------
def speech_to_text(audio):
    r = sr.Recognizer()
    with sr.AudioFile(audio) as source:
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


# ---------------- PROCESS ----------------
if audio_file is not None:

    if st.button("▶ Convert & Translate"):

        with st.spinner("Processing..."):

            # Speech to Text
            text = speech_to_text(audio_file)
            st.subheader("Recognized Text")
            st.write(text)

            # Translate
            translated = GoogleTranslator(
                source=lang_map[input_lang],
                target=lang_map[output_lang]
            ).translate(text)

            st.subheader("Translated Text")
            st.write(translated)

            # Text to Voice
            audio_out = asyncio.run(text_to_voice(translated))

        st.subheader("Output Voice")
        st.audio(audio_out, format="audio/mp3")

        st.download_button(
            "⬇ Download MP3",
            data=audio_out,
            file_name="rvoice.mp3",
            mime="audio/mp3"
        )

else:
    st.info("⬆ Please upload voice first")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("**RVOICE - Founder Raj Gupta**")
