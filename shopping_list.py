import streamlit as st
from models.chat_models import Ingredient, ShoppingList
from db import database

st.header("Twoja lista zakupów")

def change_item_bought_status(item_id, bought):
    with database.ShoppingListDatabase() as db:
        db.update_bought_status(item_id, bought)

with database.ShoppingListDatabase() as db:
    items = db.get_items()
    is_first_unbought_found = False
    if items:
        sorted_items = sorted(items, key=lambda x: x[4])
        divider_drawn = False
        for item in sorted_items:
            if not is_first_unbought_found and item[4]:
                is_first_unbought_found = True
            item_id, item_name, quantity, unit, bought = item
            
            if bought and not divider_drawn:
                st.divider()
                divider_drawn = True
            text = f"- {item_name}: {quantity} {unit}"
            if bought:
                text = f"- ~~{item_name}: {quantity} {unit}~~"
            st.checkbox(
                text,
                value=bought,
                key=f"item_{item_id}",
                on_change= change_item_bought_status,
                args=(item_id, not bought))
    else:
        st.write("Twoja lista zakupów jest pusta.")

st.container(height=20, border=False)

if is_first_unbought_found:
    if st.button("Usuń kupione produkty", width="stretch"):
        with database.ShoppingListDatabase() as db:
            items = db.get_items()
            for item in items:
                item_id, item_name, quantity, unit, bought = item
                if bought:
                    db.delete_item(item_id)
        st.rerun()
