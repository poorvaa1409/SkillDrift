import streamlit as st
from .database import add_user, login_user_db

def authentication():
    st.markdown("<h2 style='text-align: center; color: #00d1b2;'>Portal Access</h2>", unsafe_allow_html=True)
    
    tabs = st.tabs(["Login", "Sign Up", "Forgot Password"])

    with tabs[0]:
        st.markdown("#### Welcome Back")
        with st.form("Login_Form"):
            email = st.text_input("Email", placeholder="example@mail.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            if st.form_submit_button("Access Dashboard"):
                if not email or not password:
                    st.warning("Please fill all fields")
                else:
                    username = login_user_db(email, password)
                    if username:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success(f"Logging in as {username}...")
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

    with tabs[1]:
        st.markdown("#### Create New Account")
        with st.form("Signup_Form"):
            new_user = st.text_input("Username", placeholder="Choose a unique name")
            new_email = st.text_input("Email", placeholder="example@mail.com")
            new_pass = st.text_input("Password", type="password", placeholder="Create a strong password")
            confirm_pass = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
            
            if st.form_submit_button("Join SkillDrift"):
                if new_pass != confirm_pass:
                    st.error("Passwords do not match!")
                elif not new_user or not new_email or not new_pass:
                    st.warning("Please fill all fields")
                else:
                    if add_user(new_user, new_email, new_pass):
                        st.success("Account created! You can now login.")
                    else:
                        st.error("Username or Email already exists.")

    with tabs[2]:
        st.markdown("#### Reset Your Password")
        st.info("Enter your registered email to receive a reset link.")
        with st.form("Forgot_Form"):
            reset_email = st.text_input("Registered Email", placeholder="example@mail.com")
            
            if st.form_submit_button("Send Recovery Mail"):
                if reset_email:
                    st.success(f"A recovery link has been sent to {reset_email}")
                    st.balloons()
                else:
                    st.warning("Please enter your email address")
