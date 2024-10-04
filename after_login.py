import streamlit as st
import subprocess
import sys

def after_login():
    st.title("Welcome to the Violence Detection System")
    st.write(f"Logged in as: {st.session_state['user'][1]}")
    st.write("Here you can access your account information and other features.")

    # Logout button
    if st.button("Logout"):
        # Clear the user session
        del st.session_state["user"]
        st.success("You have been logged out.")
        st.experimental_rerun()  # Rerun the app to refresh the state

