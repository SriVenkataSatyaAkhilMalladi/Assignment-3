import requests
import streamlit as st
# from passlib.hash import pbkdf2_sha256
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import requests
from fastapi import Form
import hashlib
import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
import bcrypt
import jwt
from dotenv import load_dotenv
import os
import jwt
load_dotenv()

API_URL = os.environ.get('URL')

def Registration():
    
    url = API_URL + "register"
    response = requests.post(url, json={"username": username, "password": password, "plan": plan})
    if response.status_code == 200:
        st.success("User registered successfully")
    elif response.status_code == 400:
        st.warning("User already registered")
    else:
        st.error("Failed to register user")

st.title("User Registration")

username = st.text_input("Username")
password = st.text_input("Password", type="password")
plan = st.selectbox("Plan", ["free", "gold", "platinum"])
if st.button("Register"):   
    Registration()






