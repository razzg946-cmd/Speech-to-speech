import streamlit as st
from streamlit_mic_recorder import mic_recorder
from deep_translator import GoogleTranslator
import speech_recognition as sr
import edge_tts
import asyncio
from io import BytesIO
from langdetect import detect

st.set_page_config(page_title="Rvoice PRO", page_icon="🎙️")

st.title("🎙️ RVOICE PRO - AI Voice to Voice")

# ---------------- LANGUAGE ----------------
lang_map = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "bn": "Bengali",
    "mr": "Marathi",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu"
}

# reverse map
rev_map = {v: k for k, v in lang_map.items()}

# ---------------- MIC ----------------
st.subheader("🎤 Speak Now")
audio = mic_recorder(start_prompt="🎙️ Start", stop_prompt="⏹ Stop")

# ---------------- SPEECH TO TEXT ----------------
def speech_to_text(audio_bytes):
    r = sr.Recognizer()
    audio_file = sr.AudioFile(audio_bytes)
    with audio_file as source:
        data = r.record(source)
    return r.recognize_google(data)

# ---------------- TEXT TO VOICE ----------------
async def text_to_voice(text):
    communicate = edge_tts.Communicate(text, "en-US-JennyNeural")
    audio = BytesIO()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio.write(chunk["data"])

    audio.seek(0)
    return audio


# ---------------- MAIN ----------------
if audio:

    st.success("Audio captured 🎧")

    if st.button("▶ Convert & Translate"):

        with st.spinner("AI Processing..."):

            # 1. Speech → Text
            text = speech_to_text(audio["bytes"])
            st.subheader("📝 Recognized Text")
            st.write(text)

            # 2. Auto Detect Language
            detected_lang = detect(text)
            st.info(f"Detected Language: {lang_map.get(detected_lang, detected_lang)}")

            # 3. Select output language
            output_lang = st.selectbox(
                "Select Output Language",
                list(lang_map.values())
            )

            # convert back key
            target_code = list(lang_map.keys())[list(lang_map.values()).index(output_lang)]

            # 4. Translate
            translated = GoogleTranslator(
                source=detected_lang,
                target=target_code
            ).translate(text)

            st.subheader("🔁 Translated Text")
            st.write(translated)

            # 5. Voice Output
            audio_out = asyncio.run(text_to_voice(translated))

        st.subheader("🔊 Output Voice")
        st.audio(audio_out, format="audio/mp3")

        st.download_button(
            "⬇ Download MP3",
            data=audio_out,
            file_name="rvoice_pro.mp3",
            mime="audio/mp3"
        )

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("**RVOICE PRO - Founder Raj Gupta**")
