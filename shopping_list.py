import streamlit as st

st.write("Hello, world!")


if "shopping_list" in st.session_state and st.session_state.shopping_list:
    for i, produkt in enumerate(st.session_state.shopping_list.split("\n")):
        st.checkbox(produkt.strip() + "\n", key=f"produkt_{i}")