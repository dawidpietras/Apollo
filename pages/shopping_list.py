import streamlit as st
from db.model_sql import get_all_items, update_shopping_item_bought_status

st.header("Twoja lista zakupów")

def change_item_bought_status(item_id, current_bought_status):
    update_shopping_item_bought_status(item_id, not current_bought_status)

def show_all_db_items():
    items = get_all_items()
    if items:
        divider_drawn = False
        for item in items:
            if item.bought and not divider_drawn:
                st.divider()
                divider_drawn = True
            
            text = f"- {item.name}"
            if item.quantity:
                text += f": {item.quantity}"
            if item.unit:
                text += f" {item.unit}"
            
            if item.bought:
                text = f"~~{text}~~"
            
            st.checkbox(label=text, value=item.bought, key=f"item_{item.id}", on_change=change_item_bought_status, args=(item.id, item.bought))
    else:
        st.write("Twoja lista zakupów jest pusta.")

show_all_db_items()

# def change_item_bought_status(item_id, bought):
#     with database.ShoppingListDatabase() as db:
#         db.update_bought_status(item_id, bought)

# with database.ShoppingListDatabase() as db:
#     items = db.get_items()
#     is_first_unbought_found = False
#     if items:
#         sorted_items = sorted(items, key=lambda x: x[4])
#         divider_drawn = False
#         for item in sorted_items:
#             if not is_first_unbought_found and item[4]:
#                 is_first_unbought_found = True
#             item_id, item_name, quantity, unit, bought = item
            
#             if bought and not divider_drawn:
#                 st.divider()
#                 divider_drawn = True
#             text = f"- {item_name}: {quantity} {unit}"
#             if bought:
#                 text = f"- ~~{item_name}: {quantity} {unit}~~"
#             st.checkbox(
#                 text,
#                 value=bought,
#                 key=f"item_{item_id}",
#                 on_change= change_item_bought_status,
#                 args=(item_id, not bought))
#     else:
#         st.write("Twoja lista zakupów jest pusta.")

# st.container(height=20, border=False)

# if is_first_unbought_found:
#     if st.button("Usuń kupione produkty", width="stretch"):
#         with database.ShoppingListDatabase() as db:
#             items = db.get_items()
#             for item in items:
#                 item_id, item_name, quantity, unit, bought = item
#                 if bought:
#                     db.delete_item(item_id)
#         st.rerun()
