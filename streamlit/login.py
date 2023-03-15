import streamlit as st
import sqlite3
import hashlib
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import requests
from fastapi import Form
# define the Streamlit login page
from pydantic import BaseModel
import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()


# BASE_URL = "http://fastapi.latest:8080/"
BASE_URL = os.environ.get('URL')
options = ["Login", "User Registration", "Update Password"]
selected_option = st.radio("Select an option", options)

if selected_option == "Login":
    # st.write("You selected Option 1")
    st.session_state['access_token']= ''

    class Login:
        username:str = Form()
        password:str = Form()


    username = st.text_input("Username",key="username")
    password = st.text_input("Password",type="password",key="password")
    if st.button("Login"):
        url = BASE_URL + "token"
        response = requests.post(url,data={"username": username, "password": password})        
        if response.status_code == 200:
            res = response.json()
            access_token = res['access_token']
            st.session_state['access_token'] = access_token
            st.success("Logged in as {}".format(username))
        elif response.status_code == 401:
            st.error("Incorrect username or password")


elif selected_option == "Update Password":

        username = st.text_input("Username")
        new_password = st.text_input("Create new password", type="password")
        confirm_password = st.text_input("Confirm new password", type="password")
        role = "user"
        email = "{}@gmail.com".format(username)
        status = "active"
        register_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if st.button("Update"):
            url = BASE_URL + 'update_password'
            response = requests.put(url, json={"username": username, "password": new_password, "confirm_password": confirm_password})

            if response.status_code == 200:
                st.success("Password updated successfully.")
            elif response.status_code == 400:
                st.error("Password and confirm password not the same.")
            else:
                st.error("Password update unsuccessful")



else:
    st.write("Please navigate to User Registration Page")
