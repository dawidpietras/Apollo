import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

prompt = "Jesteś pomocnym asystentem, który pomaga zapisaywać listy w odpowiednich kategoriach, jeśli podany tekst nie pasuje nigdzie to nie zmyślaj"
messages = [
    {"role": "system", "content": prompt},
    {"role": "user", "content": "Naprawić kran, złożyć szafkę, kupić mleko, jajka i kilogram mąki i siedem jabłek"}
]

assert os.path.exists("schemas//voice_assistant_schema.json")

client = OpenAI(api_key=api_key)

with open("schemas//voice_assistant_schema.json", "r") as f:
    voice_assistant_schema = json.load(f)

response = client.chat.completions.create(model="gpt-5.2", messages=messages, tools=voice_assistant_schema)

a = response.model_dump_json(indent=4)
print(a)