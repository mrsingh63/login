import streamlit as st
from db_admin import verify_admin
import usermanagement  # Import user management module

# Streamlit page setup
st.set_page_config(page_title="Admin Login", page_icon="🔐", layout="centered")

# Add custom CSS to style the button
st.markdown("""
    <style>
    .green-button {
        background-color: green;
        color: white;
        padding: 0.5em;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        width: 100%;
    }
    .green-button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Admin Login")

# Create input fields for username and password
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Detect button click using st.button
login_button = st.button("Login", key="login_button")

# Login logic
if login_button:
    if not username or not password:
        st.warning("Please enter both username and password.")
    else:
        result = verify_admin(username, password)
        if result:
            st.session_state.logged_in = True  # Set login state
            st.success("Logged in successfully!")
        else:
            st.warning("Incorrect username or password. Please try again.")

# Show user management if logged in
if st.session_state.get('logged_in', False):
    usermanagement.display_user_management()  # Call a function in usermanagement.py to show data
