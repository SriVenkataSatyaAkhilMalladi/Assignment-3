import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Connect to the SQLite database file
conn = sqlite3.connect('data/register_users.dbo')

# Define the query to fetch user details based on the given username
query = "SELECT role, plan FROM user_data WHERE username = ?"
cursor = conn.cursor()


endpoints_query = "SELECT DISTINCT endpoint FROM activity_log"
endpoints = [row[0] for row in cursor.execute(endpoints_query)]

dates_query = "SELECT DISTINCT date FROM activity_log"
dates = [row[0] for row in cursor.execute(dates_query)]

users_query = "SELECT DISTINCT username FROM activity_log"
users = [row[0] for row in cursor.execute(users_query)]


# Define a function to execute the query and return the user details
def get_user_details(username):
    
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    
    return result


def get_matrix():
    # Define the dropdowns
    endpoint_selected = st.selectbox('Select an endpoint', endpoints)
    date_selected = st.selectbox('Select a date', dates)
    query = f"SELECT time FROM activity_log WHERE endpoint='{endpoint_selected}' AND date='{date_selected}' AND username='{username}'"
    query_total = f"SELECT time FROM activity_log WHERE endpoint='{endpoint_selected}' AND username='{username}'"
    data_compare_success = conn.execute(f"SELECT count(*) FROM activity_log WHERE status_code='200' AND endpoint='{endpoint_selected}' AND username='{username}'").fetchone()[0]
    data_compare_failure = conn.execute(f"SELECT count(*) FROM activity_log WHERE status_code!='200' AND endpoint='{endpoint_selected}' AND username='{username}'").fetchone()[0]
    data = [row[0] for row in cursor.execute(query)]
    data_total=[row[0] for row in cursor.execute(query_total)]
    
    print(data_compare_success)
    # Create the line graph
    fig, ax = plt.subplots()
    ax.plot(data)
    ax.set_xlabel('Time')
    ax.set_ylabel('Endpoint')
    ax.set_title(f'Times {endpoint_selected} API was called on {date_selected}')
    st.pyplot(fig)
    # Create the line graph
    fig1, ax1 = plt.subplots()
    ax1.plot(data_total)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Endpoint')
    ax1.set_title(f'Times {endpoint_selected} API was called in total')
    st.pyplot(fig1)
    #comparison of successfull Api calls and unsuccessful
    st.write(f"There were in total '{data_compare_success}' succesful calls for the selected api and '{data_compare_failure}' unsuccessful calls")


def get_admin_matrix():
    occurrences = []
    endpoint_selected = st.selectbox('Select an endpoint', endpoints)
    date_selected = st.selectbox('Select a date', dates)
    for user in users:
        query = f"SELECT COUNT(*) FROM activity_log WHERE username='{user}' AND endpoint='{endpoint_selected}' AND date='{date_selected}' "
        count = cursor.execute(query).fetchone()[0]
        occurrences.append(count)

    # Create the bar graph
    fig, ax = plt.subplots()
    ax.bar(users, occurrences)
    ax.set_xlabel('Usernames')
    ax.set_ylabel('Occurrences')
    ax.set_title(f'User Activity for the endpoint of {endpoint_selected} on {date_selected}')
    ax.xaxis.set_tick_params(rotation=45) # rotate x-axis tick labels for readability
    st.pyplot(fig)

st.title("User Role and Plan Count")

# Get the username input from the user
username = st.text_input("Enter your username")

# Check if the username is not empty
if username:
    # Call the function to get the user details
    user_details = get_user_details(username)
    
    # Check if the user exists
    if user_details:
        # Get the role and plan of the user
        role, plan = user_details
        
        # Display the role of the user
        if role == "admin":
            st.write(f"Welcome {username}! Your role is {role}")
            get_admin_matrix()
        elif role == "user":
            st.write(f"Welcome {username}! Your role is {role}")
             
            # Display the plan count of the user
            if plan == "free":
                st.write("Your plan count is 10")
                get_matrix()
            elif plan == "gold":
                st.write("Your plan count is 15")
                get_matrix()
            elif plan == "platinum":
                st.write("Your plan count is 20")
                get_matrix()
            else:
                st.write("Invalid plan")
    else:
        st.write("Invalid username")

















