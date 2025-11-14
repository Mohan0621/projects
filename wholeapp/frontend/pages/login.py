import streamlit as st
import requests
import jwt

st.title("🔐 Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Login"):
    data = {"username": username, "password": password}
    res = requests.post("http://localhost:5000/auth/login", json=data)
    if res.status_code == 200:
        response = res.json()
        st.session_state.access_token = response["access_token"]
        payload = jwt.decode(
            response["access_token"],
            options={"verify_signature": False}
        )

        st.session_state.role = payload["role"]
        st.session_state.user_id = payload["sub"]

        st.success("Login successful!")
        st.rerun()

    else:
        st.error("Invalid credentials")
