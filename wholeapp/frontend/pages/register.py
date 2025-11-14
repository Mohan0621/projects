import streamlit as st
import requests

st.title("📝 Register")
username = st.text_input("Choose a Username")
password = st.text_input("Choose a Password", type="password")
if st.button("Register"):
    res = requests.post("http://localhost:5000/auth/register", json={
        "username": username,
        "password": password
    })
    if res.status_code == 201:
        st.success("User registered! Now login.")
    else:
        st.error(res.json().get("message", "Registration failed"))
