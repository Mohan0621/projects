import streamlit as st
import requests

st.title("👑 Admin Dashboard")
if st.session_state.role != "admin":
    st.error("Admin access required.")
    st.stop()
headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
st.subheader("All Users")
res = requests.get("http://localhost:5000/admin/users", headers=headers)
if res.status_code == 200:
    users = res.json()
    for u in users:
        st.write(u)
        if st.button(f"Promote {u['username']}", key="promote"+u["_id"]):
            requests.post(
                f"http://localhost:5000/admin/promote/{u['_id']}",
                headers=headers
            )
            st.success("User promoted!")
            st.rerun()
        if st.button(f"Delete {u['username']}", key="delete"+u["_id"]):
            requests.delete(
                f"http://localhost:5000/admin/delete/{u['_id']}",
                headers=headers
            )
            st.error("User deleted!")
            st.rerun()
st.subheader("📊 System Stats")
stats = requests.get("http://localhost:5000/admin/stats", headers=headers).json()
st.json(stats)
