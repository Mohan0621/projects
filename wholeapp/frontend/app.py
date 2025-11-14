import streamlit as st

st.set_page_config(page_title="FlaskShield", page_icon="🛡️")
if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "role" not in st.session_state:
    st.session_state.role = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None

st.title("🛡️ FlaskShield - Secure App")
st.write("Use the sidebar to navigate.")
