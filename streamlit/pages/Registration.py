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


API_URL = "http://localhost:8080"
# options = ["Login", "User Registration", "Update Password"]
# selected_option = st.radio("Select an option", options)

# if selected_option == "Login":
#     # st.write("You selected Option 1")
#     st.session_state['access_token']= ''

#     class Login:
#         username:str = Form()
#         password:str = Form()

#     def login():
#         st.title("Login")
#         oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#         username = st.text_input("Username",key="username")
#         password = st.text_input("Password",type="password",key="password")
#         if st.button("Login"):
#             url = str(os.environ.get('URL')) + "token"
#             response = requests.post(url,data={"username": username, "password": password})        
#             if response.status_code == 200:
#                 res = response.json()
#                 access_token = res['access_token']
#                 st.session_state['access_token'] = access_token
#                 st.success("Logged in as {}".format(username))
#                 st.write(type(access_token))
#                 return True # return True after a successful login
#             else:
#                 st.error("Invalid username or password")
#         return False

#     # define the Streamlit main application
#     def show_main_app():
#         # st.title("Main Application")
#         # st.write("Welcome to the main application!")
#         url = "http://localhost:8080/users/me"
#         #token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjc3MTI5MTgwfQ.71FkTnZBGyLT1fbz0E0WQMMVFz2H_0injbiTZLVHBS0"
#         headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
#         response = requests.get(url, headers=headers)

#         # check response
#         if response.status_code == 200:
#             print(response.json())
#         else:
#             print("Request failed with status code:", response.status_code)
#             # add the rest of your application code here




#     def main():
#         if login():
#             print("great")


#     if __name__ == "__main__":
#         main()

# elif selected_option == "Update Password":
#     # st.write("You selected Option 2")
#     if st.button("Change Password"):
#         new_password = st.text_input("Create new password", type="password")
#         confirm_password = st.text_input("Confirm new password", type="password")
#         if st.button("Update"):
#             if new_password != confirm_password:
#                 st.error("Password does not match")
#             else:
                
#                 response = requests.put(f"{API_URL}/users/{username}/password", json={"password": new_password, "confirm new password": confirm_password})

#                 if response.status_code == 200:
#                     st.success("Password updated successfully.")
#                 else:
#                     st.error("Error updating password.")


# else:
#     st.write("Please navigate to User Registration Page")

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


# if st.button("Change Password"):
#     new_password = st.text_input("Create new password", type="password")
#     confirm_password = st.text_input("Confirm new password", type="password")
#     if st.button("Update"):
#         if new_password != confirm_password:
#             st.error("Password does not match")
#         else:
            
#             response = requests.put(f"{API_URL}/users/{username}/password", json={"password": new_password, "confirm new password": confirm_password})

#             if response.status_code == 200:
#                 st.success("Password updated successfully.")
#             else:
#                 st.error("Error updating password.")



    


# #Update password on streamlit not working - field disapeearing on clicking Confirm new password field 
# # if st.button("Update Password"):
# new_password = st.text_input("Create new password", type="password")
# confirm_password = st.text_input("Confirm new password", type="password")
# if st.button("Update"):
#     if new_password != confirm_password:
#         st.error("Password does not match")

#     # elif st.button("Update"):
#         # st.success("Password update successfully!")
#         # update_password(username,password)
#     response = requests.put(f"{API_URL}/users/{username}/password", json={"password": new_password})
#     if response.status_code == 200:
#         st.success("Password updated successfully.")
#     else:
#         st.error("Error updating password.")







