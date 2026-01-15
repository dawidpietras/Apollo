import streamlit as st
from streamlit_mic_recorder import mic_recorder
import io
from models.chat_models import ShoppingList
from backend.prompts import *
from backend.llm_client import get_sync_client


client = get_sync_client()

if not st.session_state.get("transcription"):
    st.session_state["transcription"] = ""

if not st.session_state.get("transcripted_text"):
    st.session_state["transcripted_text"] = ""

st.header("Powiedź jakie produkty masz w domu")

st.write("Naciśnij przycisk, aby rozpocząć nagrywanie.")

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
                {"role": "system", "content": get_ingredients_from_transcription},
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
                {"role": "system", "content": get_recipe_from_transcripted_ingredients},
                {"role": "user", "content": st.session_state.transcripted_text}
            ]
            def stream_response():
                stream = client.chat.completions.create(
                    model="gpt-5.2",
                    messages=messages,
                    stream=True
                )
                response = ""
                for chunk in stream:
                    chunk_content = chunk.choices[0].delta.content
                    if chunk_content:
                        response += chunk_content
                        yield chunk_content
            col1, col2 = st.columns(2)
            p1 = col1.empty()
            p2 = col2.empty()
            res = ""
            for text in stream_response():
                res += text
                p1.markdown(res)
                p2.markdown(res)