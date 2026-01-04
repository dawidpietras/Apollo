import streamlit as st
from models.chat_models import Ingredient, ShoppingList

st.header("Twoja lista zakupów")


if "shopping_list" in st.session_state and st.session_state.shopping_list:
    for i, item in enumerate(st.session_state.shopping_list.ingredients):
        # st.checkbox(produkt, key=f"produkt_{i}")
        # print(i, produkt)
        st.checkbox(f"{item.name} - {item.quantity}{item.unit}", key=f"item_{i}")