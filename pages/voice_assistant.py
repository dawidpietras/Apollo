import streamlit as st
from streamlit_mic_recorder import mic_recorder
from openai import OpenAI
from dotenv import load_dotenv
from backend.prompts import agent_to_do_shopping_list_system_prompt
import os
import json
import io
from typing import Dict, Type
from sqlmodel import SQLModel
from db.model_sql import insert_shopping_list_item
from models.models import ShoppingItem, ToDoTask
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

if not st.session_state.get("todo-shopping-list"):
    st.session_state["todo-shopping-list"] = ""

if not st.session_state.get("tool-call-transcription"):
    st.session_state["tool-call-transcription"] = ""

if not st.session_state.get("tool-call-pairs"):
    st.session_state["tool-call-pairs"] = []


client = OpenAI(api_key=api_key)

# Mapping for function to be returned by LLM and db model
TOOLS_MAPPING: Dict[str, Type[SQLModel]] = {
    "update_shopping_list": ShoppingItem,
    "add_task": ToDoTask
}

def get_openai_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": name,
                "description": f"Wywołaj gdy chcesz: {name}",
                "parameters": model.model_json_schema()
            }
        } for name, model in TOOLS_MAPPING.items()
    ]

def get_speech_to_text():
    
    audio_results = mic_recorder(
        start_prompt="Naciśnij, aby rozpocząć nagrywanie",
        stop_prompt="Naciśnij, aby zakończyć nagrywanie",
        format="wav",
        key="mic_recorder"
    )

    if audio_results:
        audio_bytes = audio_results.get('bytes')
        
        with st.spinner("Transkrypcja nagrania przez OpenAI..."):
            
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
                st.session_state["tool-call-transcription"] = transcription.text
                
def extract_tool_calls_from_transcript():
    
    if st.session_state["tool-call-transcription"]:
        messages = [
            {"role": "system", "content": agent_to_do_shopping_list_system_prompt},
            {"role": "user", "content": st.session_state["tool-call-transcription"]}
                ]
        response = client.chat.completions.create(model="gpt-5.2", messages=messages, tools=get_openai_tools())
        
        if response.choices[0].finish_reason == 'tool_calls':
            response_functions = response.choices[0].message.tool_calls
            tool_calls = []
            for calls in response_functions:
                tool_calls.append(TOOLS_MAPPING[calls.function.name](**(json.loads(calls.function.arguments))))
            st.session_state["tool-call-pairs"] = tool_calls

def change_bought_status(item: ShoppingItem):
    item.bought = not item.bought
    return item

@st.fragment
def create_checkboxes():
    if st.session_state["tool-call-pairs"]:
        col1, col2 = st.columns(2)
        col1.empty()
        col2.empty()
        tool_calls = st.session_state["tool-call-pairs"]
        for calls in tool_calls:
            if isinstance(calls, ToDoTask):
                col1.checkbox(label=calls.title, value=True)
            elif isinstance(calls, ShoppingItem):
                text = calls.name.capitalize()
                if calls.quantity:
                    text += ' - ' + str(calls.quantity)
                if calls.unit:
                    text += ' ' + calls.unit
                col2.checkbox(label=text, value=not calls.bought, on_change=change_bought_status, args=(calls,))

def save_ingredients_to_shopping_list():
    if st.session_state["tool-call-pairs"]:
        if st.button(label="Wyślij do listy zakupów"):
            for item in st.session_state["tool-call-pairs"]:
                if isinstance(item, ShoppingItem):
                    insert_shopping_list_item(item)
            else:
                st.session_state["tool-call-pairs"] = []

get_speech_to_text()
extract_tool_calls_from_transcript()
create_checkboxes()
save_ingredients_to_shopping_list()