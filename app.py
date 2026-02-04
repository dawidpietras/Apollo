import streamlit as st
from db.model_sql import create_db_and_tables

@st.cache_resource
def init_database():
    create_db_and_tables()

init_database()

chatbot_page = st.Page("pages//chatbot.py", title="Książka kucharksa", icon=":material/chef_hat:")
shopping_list_page = st.Page("pages//shopping_list.py", title="Lista zakupów", icon="🛒")
record_page = st.Page("pages//recorder_page.py", title="Kucharz", icon="🎤")
two_chats_page = st.Page("pages//two_chats.py", title="Two chats", icon="💬")
voice_assistant = st.Page("pages//voice_assistant.py", title="Voice Assistant", icon="💬")

pg = st.navigation([chatbot_page, shopping_list_page, record_page, two_chats_page, voice_assistant])
st.set_page_config(page_title="Dietetyk AI", page_icon=":material/edit:")
pg.run()