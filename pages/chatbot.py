import streamlit as st
import backend.nutritionist as chat
from models.chat_models import IngredientWithBoughtStatus
import db.database as database

USER_AVATAR = "https://img.icons8.com/3d-fluency/94/eggplant.png"
ASSISTANT_AVATAR = "https://img.icons8.com/3d-fluency/94/robot-2.png"

st.title("Dietetyk AI")

### Initialize session state variables
if "nutrionist" not in st.session_state:
    st.session_state.nutrionist = chat.Nutritionist()
    st.session_state.nutrionist.change_persona("Lista zakupów")
    st.session_state.nutrionist.set_model("gpt-5.2")
nutrionist = st.session_state.nutrionist 

if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_snow" not in st.session_state:
    st.session_state.show_snow = True
    st.snow()

#### Chat Interface

for message in st.session_state.messages:
    icon = USER_AVATAR if message["role"] == "user" else ASSISTANT_AVATAR
    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

if prompt := st.chat_input("Co chcesz dziś przekąsić?"):
    st.chat_message("user", avatar=USER_AVATAR).markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        # st.markdown(response)
        response = st.write_stream(st.session_state.nutrionist.send_user_prompt(prompt))
    
    st.session_state.messages.append({"role": "assistant", "content": response})


### Shopping List Management
if st.session_state.messages:
    if st.button("Dodaj do listy zakupów"):
        last_ingredients = st.session_state.nutrionist.get_list_of_ingredients(st.session_state.messages[-1]["content"]).ingredients
        with database.ShoppingListDatabase() as database:
            for ingredient in last_ingredients:
                db_item = IngredientWithBoughtStatus(**ingredient.model_dump())
                database.update_quantity(db_item.canonical_name, db_item.quantity, db_item.unit, db_item.bought)
        st.toast('Pomyślnie dodano produkty do listy zakupów!', icon='✅')
