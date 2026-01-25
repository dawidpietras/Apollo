import streamlit as st
from streamlit_mic_recorder import mic_recorder
from openai import OpenAI
from dotenv import load_dotenv
from backend.prompts import agent_to_do_shopping_list_system_prompt
import os
import json
import io

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

if not st.session_state.get("todo-shopping-list"):
    st.session_state["todo-shopping-list"] = ""
    


assert os.path.exists("schemas//voice_assistant_schema.json")

client = OpenAI(api_key=api_key)

with open("schemas//voice_assistant_schema.json", "r") as f:
    voice_assistant_schema = json.load(f)

audio_results = mic_recorder(
    start_prompt="Naciśnij, aby rozpocząć nagrywanie",
    stop_prompt="Naciśnij, aby zakończyć nagrywanie",
    format="wav",
    key="mic_recorder"
)

if audio_results:
    audio_bytes = audio_results.get('bytes')
    
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
            
            messages = [
                {"role": "system", "content": agent_to_do_shopping_list_system_prompt},
                {"role": "user", "content": transcription.text}
                    ]
            response = client.chat.completions.create(model="gpt-5.2", messages=messages, tools=voice_assistant_schema)

            col1, col2 = st.columns(2)

            
            col2.empty()

            tool_calls = response.choices[0].message.tool_calls
            for call in tool_calls:
                if call.function.name == "add_task":
                    col1.markdown(call.function.arguments)
                elif call.function.name == "update_shopping_list":
                    col2.markdown(call.function.arguments)
        except Exception as e:
            st.error(f"Wystąpił błąd API: {e}")

