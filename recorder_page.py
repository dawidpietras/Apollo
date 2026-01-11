import streamlit as st
from streamlit_mic_recorder import mic_recorder
import io
from openai import OpenAI
import os
from dotenv import load_dotenv
import instructor
from models.chat_models import ShoppingList

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key)
client = instructor.patch(OpenAI(api_key=api_key))

if not st.session_state.get("transcription"):
    st.session_state["transcription"] = ""

if not st.session_state.get("transcripted_text"):
    st.session_state["transcripted_text"] = ""

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
            st.session_state.transcription = transcription.text
            
        except Exception as e:
            st.error(f"Wystąpił błąd API: {e}")

if st.session_state["transcription"]:
    if st.button("Generuj listę zakupów z ostatniej transkrypcji"):
        with st.spinner("Generowanie listy zakupów..."):
            messages = [
                {"role": "system", "content": "Jesteś pomocnym asystemntem, \
                 który z podanego tekstu, który powinien być słownym opisem \
                 produktów spożywczych które użytkownik posiada w domu wydobywa \
                 listę tych produktów wraz z ilością."},
                {"role": "user", "content": st.session_state.transcription}
            ]
            response = client.chat.completions.create(model="gpt-5.2",
                                           messages=messages,
                                           response_model=ShoppingList)
            for i in response.ingredients:
                st.write(f"{i.canonical_name} - {i.quantity} {i.unit} ")
            st.session_state.transcripted_text = response.model_dump_json()
            print(st.session_state.transcripted_text)

if st.session_state["transcripted_text"]:
    if st.button("Wymyśl przepis z podanych składników"):
        with st.spinner("Generowanie przepisu..."):
            messages = [
                {"role": "system", "content": "Jesteś pomocnym asystemntem, \
                 który z podanej listy składników stara się ułożyć przepis \
                     na danie. Zakładaj, że użytkownik posiada podstawowe \
                         produkty w domu takie jak sól, przyprawy, olej itd."},
                {"role": "user", "content": st.session_state.transcripted_text}
            ]
            response = client.chat.completions.create(model="gpt-5.2",
                                           messages=messages)
            st.write(response.choices[0].message.content)