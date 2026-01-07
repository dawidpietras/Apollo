import streamlit as st
from models.chat_models import Ingredient, ShoppingList
from db import database

st.header("Twoja lista zakupów")

def change_item_bought_status(item_id, bought):
    with database.ShoppingListDatabase() as db:
        db.update_bought_status(item_id, bought)

with database.ShoppingListDatabase() as db:
    items = db.get_items()
    if items:
        for item in items:
            item_id, item_name, quantity, unit, bought = item
            st.checkbox(f"- {item_name}: {quantity} {unit}",
                             value=bought,
                             key=f"item_{item_id}",
                             on_change= change_item_bought_status,
                             args=(item_id, not bought))
    else:
        st.write("Twoja lista zakupów jest pusta.")

# if st.button("Usuń zaznaczone elementy"):
#     with database.ShoppingListDatabase() as db:
        

# if "shopping_list" in st.session_state and st.session_state.shopping_list:
    
#     for i, item in enumerate(st.session_state.shopping_list.ingredients):
#         # st.checkbox(produkt, key=f"produkt_{i}")
#         # print(i, produkt)
#         st.checkbox(f"{item.name} - {item.quantity}{item.unit}", key=f"item_{i}")