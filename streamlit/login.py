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


base_url = os.environ.get('URL')
st.session_state['access_token']= ''

class Login:
    username:str = Form()
    password:str = Form()

def login():
    st.title("Login")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    username = st.text_input("Username",key="username")
    password = st.text_input("Password",type="password",key="password")
    if st.button("Login"):
        url = str(base_url) + "token"
        response = requests.post(url,data={"username": username, "password": password})        
        if response.status_code == 200:
            res = response.json()
            access_token = res['access_token']
            st.session_state['access_token'] = access_token
            st.success("Logged in as {}".format(username))
            return True # return True after a successful login
        else:
            st.error("Invalid username or password")
    return False


def main():
    login()


if __name__ == "__main__":
    main()
