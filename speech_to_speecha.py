if audio_bytes:

    st.audio(audio_bytes)

    if st.button("▶ Convert & Translate"):

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

            st.subheader("🔊 Output Voice")
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
