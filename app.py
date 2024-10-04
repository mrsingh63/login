import streamlit as st
from db import create_connection
import pandas as pd
import hashlib
from after_login import after_login  # Import the after_login function
from db_admin import verify_admin  # Import admin verification function
import usermanagement  # Import user management module
from streamlit_lottie import st_lottie  # Import st_lottie for Lottie animations
import json  # Import JSON for reading local files

# Function to load Lottie animation from a local file
def load_lottie_local(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to register a user
def register_user(name, username, password, contact, gender):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (name, username, password, contact, gender) VALUES (%s, %s, %s, %s, %s)", 
                   (name, username, hash_password(password), contact, gender))
    connection.commit()
    cursor.close()
    connection.close()

# Function to authenticate a user
def authenticate_user(username, password):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
                   (username, hash_password(password)))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user

# Streamlit UI
st.title("Violence Detection System")

menu = ["Login", "Register", "Forget Password", "Admin Login"]  # Added Admin Login
choice = st.sidebar.selectbox("Select Option", menu)

# Check if the user is logged in
if "user" in st.session_state:
    after_login()  # Show after login content if the user is logged in
elif "admin_logged_in" in st.session_state:
    usermanagement.display_user_management()  # Show user management if admin is logged in
else:
    # Login section
    if choice == "Login":
        st.subheader("Login Section")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        
        if st.button("Login"):
            user = authenticate_user(username, password)
            if user:
                st.session_state["user"] = user  # Store user info in session state
                st.success("Logged In as {}".format(user[1]))
                after_login()  # Call the function to display after login content
            else:
                st.warning("Incorrect Username/Password")

        # Load and display Lottie animation from a local file
        lottie_file_path = "loginani.json"  # Change this to your JSON file path
        lottie_json = load_lottie_local(lottie_file_path)
        if lottie_json:
            st_lottie(lottie_json, speed=1, height=300, width=300)  # You can adjust the size as needed
        else:
            st.warning("Failed to load animation.")  # Message if loading fails

    elif choice == "Register":
        st.subheader("Registration Section")
        name = st.text_input("Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        re_password = st.text_input("Re-enter Password", type='password')
        contact = st.text_input("Contact")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        # Initialize a flag to check registration status
        registration_successful = False

        if st.button("Register"):
            if password == re_password:
                register_user(name, username, password, contact, gender)
                st.success("Registered Successfully! Please login.")
                registration_successful = True  # Set registration status to True
            else:
                st.warning("Passwords do not match.")

        # Load and display success animation if registration was successful and not already shown
        if registration_successful:
            # Use session state to check if the animation has already been shown
            if "registration_animation_shown" not in st.session_state:
                st.session_state.registration_animation_shown = True  # Mark animation as shown

                success_animation_file_path = "successani.json"  # Path to your success animation JSON file
                success_lottie_json = load_lottie_local(success_animation_file_path)
                
                # Center the animation using markdown
                st.markdown("<div style='display: flex; justify-content: center;'>" + 
                            "<div style='margin: auto;'>" +
                            "</div></div>", unsafe_allow_html=True)

                if success_lottie_json:
                    st_lottie(success_lottie_json, speed=1, height=300, width=300)  # Adjust size as needed
                else:
                    st.warning("Failed to load success animation.")  # Message if loading fails

    elif choice == "Forget Password":
        st.subheader("Forget Password Section")
        username = st.text_input("Enter your username")
        
        if st.button("Reset Password"):
            # This is a placeholder for the reset password functionality
            st.success("Password reset link sent to your registered email.")
    
    elif choice == "Admin Login":
       

        # Admin login section
        st.subheader("Admin Login Section")
        admin_username = st.text_input("Admin Username")
        admin_password = st.text_input("Admin Password", type='password')
        
        if st.button("Login"):
            result = verify_admin(admin_username, admin_password)
            if result:
                st.session_state.admin_logged_in = True  # Set admin login state
                st.success("Logged in successfully as Admin!")
                usermanagement.display_user_management()  # Show user management on admin login
            else:
                st.warning("Incorrect Admin Username/Password")
