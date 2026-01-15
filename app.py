import streamlit as st

chatbot_page = st.Page("pages//chatbot.py", title="Chatbot", icon="💬")
shopping_list_page = st.Page("pages//shopping_list.py", title="Shopping List", icon="🛒")
record_page = st.Page("pages//recorder_page.py", title="Recorder", icon="🎤")

pg = st.navigation([chatbot_page, shopping_list_page, record_page])
st.set_page_config(page_title="Dietetyk AI", page_icon=":material/edit:")
pg.run()