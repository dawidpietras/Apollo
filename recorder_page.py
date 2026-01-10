import streamlit as st
from streamlit_mic_recorder import mic_recorder
import io
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.header("Nagraj swój głos")

st.write("Naciśnij przycisk, aby rozpocząć nagrywanie.")

# 2. Rejestrator dźwięku
audio_results = mic_recorder(
    start_prompt="Naciśnij, aby rozpocząć nagrywanie",
    stop_prompt="Naciśnij, aby zakończyć nagrywanie",
    format="wav",
    key="mic_recorder"
)

if audio_results:
    audio_bytes = audio_results.get('bytes')
    
    st.audio(audio_bytes, format="audio/wav")
    
    with st.spinner("Transkrypcja nagrania przez OpenAI..."):
        try:
            audio_buffer = io.BytesIO(audio_bytes)
            audio_buffer.name = "audio.wav"
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_buffer,
                language="pl"
            )
            
            st.success("Transkrypcja zakończona!")
            st.subheader("Rozpoznany tekst:")
            st.write(transcription.text)
            
        except Exception as e:
            st.error(f"Wystąpił błąd API: {e}")