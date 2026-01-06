import streamlit as st
from models.chat_models import Ingredient, ShoppingList
from db import database

st.header("Twoja lista zakupów")

with database.ShoppingListDatabase() as db:
    items = db.get_items()
    if items:
        for item in items:
            item_id, item_name, quantity, unit = item
            st.checkbox(f"- {item_name}: {quantity} {unit}")
    else:
        st.write("Twoja lista zakupów jest pusta.")

# if "shopping_list" in st.session_state and st.session_state.shopping_list:
    
#     for i, item in enumerate(st.session_state.shopping_list.ingredients):
#         # st.checkbox(produkt, key=f"produkt_{i}")
#         # print(i, produkt)
#         st.checkbox(f"{item.name} - {item.quantity}{item.unit}", key=f"item_{i}")