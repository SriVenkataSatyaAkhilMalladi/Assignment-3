import requests
import streamlit as st
# from passlib.hash import pbkdf2_sha256
from jose import JWTError, jwt
import hashlib
import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
import bcrypt


API_URL = "http://localhost:8080"

def Registration():
    
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    url = "http://localhost:8080/register"
    response = requests.post(url, json={"username": username, "password": hashed_password, "plan": plan})
    if response.status_code == 200:
        st.success("User registered successfully")
    elif response.status_code == 500:
        st.warning("User already registered")
    else:
        st.error("Failed to register user")

st.title("User Registration")

username = st.text_input("Username")
password = st.text_input("Password", type="password")
plan = st.selectbox("Plan", ["Free", "Gold", "Platinum"])
if st.button("Register"):   
    Registration()


if st.button("Change Password"):
    new_password = st.text_input("Create new password", type="password")
    confirm_password = st.text_input("Confirm new password", type="password")
    if st.button("Update"):

        if new_password != confirm_password:
            st.error("Password does not match")
        else:
            
            response = requests.put(f"{API_URL}/users/{username}/password", json={"password": new_password})

            if response.status_code == 200:
                st.success("Password updated successfully.")
            else:
                st.error("Error updating password.")



    


#Update password on streamlit not working - field disapeearing on clicking Confirm new password field 
# if st.button("Update Password"):
new_password = st.text_input("Create new password", type="password")
confirm_password = st.text_input("Confirm new password", type="password")
if new_password != confirm_password:
        st.error("Password does not match")
if st.button("Update"):
    # elif st.button("Update"):
        # st.success("Password update successfully!")
        # update_password(username,password)
    response = requests.put(f"{API_URL}/users/{username}/password", json={"password": new_password})
    if response.status_code == 200:
        st.success("Password updated successfully.")
    else:
        st.error("Error updating password.")







