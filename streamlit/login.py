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

API_URL = "http://localhost:8080"
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
        url = 'http://localhost:8080/' + "token"
        response = requests.post(url,data={"username": username, "password": password})        
        if response.status_code == 200:
            res = response.json()
            access_token = res['access_token']
            st.session_state['access_token'] = access_token
            st.success("Logged in as {}".format(username))
            # return True # return True after a successful login

    # def login():
    #     st.title("Login")
    #     oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    #     username = st.text_input("Username",key="username")
    #     password = st.text_input("Password",type="password",key="password")
    #     if st.button("Login"):
    #         url = str(os.environ.get('URL')) + "token"
    #         response = requests.post(url,data={"username": username, "password": password})        
    #         if response.status_code == 200:
    #             res = response.json()
    #             access_token = res['access_token']
    #             st.session_state['access_token'] = access_token
    #             st.success("Logged in as {}".format(username))
    #             st.write(type(access_token))
    #             return True # return True after a successful login
    #         else:
    #             st.error("Invalid username or password")
    #     return False

    # # define the Streamlit main application
    # def show_main_app():

    #     url = "http://localhost:8080/users/me"
    #     #token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjc3MTI5MTgwfQ.71FkTnZBGyLT1fbz0E0WQMMVFz2H_0injbiTZLVHBS0"
    #     headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
    #     response = requests.get(url, headers=headers)

    #     # check response
    #     if response.status_code == 200:
    #         print(response.json())

    #     else:
    #         print("Request failed with status code:", response.status_code)


    # def main():
    #     if login():
    #         print("great")


    # if __name__ == "__main__":
    #     main()

elif selected_option == "Update Password":

        username = st.text_input("Username")
        new_password = st.text_input("Create new password", type="password")
        confirm_password = st.text_input("Confirm new password", type="password")
        role = "user"
        email = "{}@gmail.com".format(username)
        status = "active"
        register_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if st.button("Update"):
            if new_password != confirm_password:
                st.error("Password does not match")
            else:
                
                response = requests.put(f"{API_URL}/update_password", json={"username": username, "password": new_password, "confirm_password": confirm_password})

                if response.status_code == 200:
                    st.success("Password updated successfully.")
                else:
                    st.error("Password updated successfully.")



else:
    st.write("Please navigate to User Registration Page")