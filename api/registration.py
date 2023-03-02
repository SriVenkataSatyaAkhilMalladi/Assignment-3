from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import FastAPI, Request, APIRouter, HTTPException
import hashlib
import api.jwt
from typing import Optional
import bcrypt
import pandas as pd
import os
import requests
import re
import sqlite3
from pathlib import Path
from datetime import datetime


jwt = api.jwt
router_register_user = APIRouter()
router_update_password = APIRouter()
router_get_count = APIRouter()

class User(BaseModel):
    username: str
    password: str
    plan: str

users = {
    'username': [],
    # 'password':[],
    'hashed_password': [],
    'plan':[],
    'registered_time':[],
}


@router_register_user.post("/register")
async def register_user(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    hashed_password = str(hashed_password)
    registered_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    users['username'].append(user.username)   #map all scraped data into the dict
    users['hashed_password'].append(hashed_password)
    users['plan'].append(user.plan)
    users['registered_time'].append(registered_time)

# Define the table schema
    conn = sqlite3.connect('register_users.db')
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='USER_DATA'")
    table_exists = c.fetchone()

    if table_exists:
        print("The users table already exists")
        
        for i in range(len(users['username'])):
            query = "INSERT INTO USER_DATA (username, hashed_password, plan) VALUES (?, ?, ?)"
            c.execute(query, (users['username'][i], users['hashed_password'][i], users['plan'][i]))
            # query = "INSERT INTO USER_DATA (username, hashed_password, plan, registered_time) VALUES (?, ?, ?, ?)"
            # c.execute(query, (users['username'][i], users['hashed_password'][i], users['plan'][i], users['registered_time'][i]))

        print("ran till here")
        if HTTPException(status_code=500, detail="User already regsitered, please navigate to login"):
            print("User already exists")

        else:
            raise HTTPException(status_code=200, detail="User registered successfully")
    
    #Table does not exist
    else:
        print("The users table does not exist")
        c.execute('''CREATE TABLE USER_DATA
                (username TEXT PRIMARY KEY, hashed_password TEXT, plan TEXT)''')

        for i in range(len(users['username'])):
            query = "INSERT INTO USER_DATA (username, hashed_password, plan, registered_time) VALUES (?, ?, ?, ?)"
            c.execute(query, (users['username'][i], users['hashed_password'][i], users['plan'][i], users['registered_time'][i]))
            raise HTTPException(status_code=200, detail="User registered successfully")
        
        print("query executed")
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("added in table")


    


@router_update_password.put("/users/{username}/password")
async def update_password(username: str, password: str):
   
    # Update the user's password in the dictionary
    # if username in users['username']:
    if password != " ":
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        conn = sqlite3.connect('register_users.db')
        c = conn.cursor()
        # for i in range(len(users['username'])):
            # query = "INSERT INTO USER_DATA (username, hashed_password, plan) VALUES (?, ?, ?)"
            # c.execute(query, (users['username'][i], users['hashed_password'][i], users['plan'][i]))
        query = "UPDATE USER_DATA SET hashed_password = ? WHERE username = ?"
        c.execute(query, (hashed_password, username))

        # users[username]["password"] = password 
        #not storing password enetered^ stored hashed password

        # Hash the new password
      
        # users[username]["hashed_password"] = hashed_password
        print("running till here")
        raise HTTPException(status_code=200, detail="Password updated successfully.")
        # return {"message": "Password updated successfully."}
    else:
        raise HTTPException(status_code=500, detail="User not found")
        # return {"error": "User not found."}






