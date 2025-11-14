import streamlit as st
import requests

if st.session_state.access_token is None:
    st.warning("You must log in first.")
    st.stop()

st.title("👤 User Dashboard")

headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
res = requests.get("http://localhost:5000/user/me", headers=headers)
profile = res.json()
st.subheader("Profile Details")
st.json(profile)
st.subheader("Upload Profile Picture")
file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
if file:
    files = {"file": file.getvalue()}
    upload_res = requests.post(
        "http://localhost:5000/user/upload",
        files={"file": (file.name, file, file.type)},
        headers=headers
    )
    if upload_res.status_code == 200:
        st.success("Image uploaded!")
if profile.get("profile_image"):
    img_url = f"http://localhost:5000/user/image/{profile['profile_image']}"
    st.image(img_url, caption="Profile Photo")
