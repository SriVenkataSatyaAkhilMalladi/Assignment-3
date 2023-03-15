# Assignment-3
#Hosted on AWS EC2

Streamlit - http://ec2-52-45-166-0.compute-1.amazonaws.com:8501/

FastAPI Docs - http://ec2-52-45-166-0.compute-1.amazonaws.com:8080/docs#/

AWS Report - https://greatexpectationsteam01.s3.amazonaws.com/index.html

Refrence:

## api folder /api
This folder contains all the api method functions and their respective functional dependencies. They are named as per the functionality - for example: api/metadata_geos.py - contains the api methods for extracting metadata from the Public aws geos bucket to a database.

## data folder /data
This contains all the database file and csv files.

## cli folder /cli
This contains files related to the CLI

## sql folder /sql
This folder contains all the sql scripts that are being used in this application.

## streamlit /streamlit
This contains all the streamlit pages and use the api calls from /api folder to do any task.

# How to Run
1. Open terminal
2. Browse the location where you want to clone the repository
3. Write the following command and press enter 
````
  git clone https://github.com/BigDataIA-Spring2023-Team-01/Assignment-3.git
 ````
 4. Create a virtual environment using the following command
 ````
  python -m venv <Virtual_environment_name>
 ````
 5. Activate the virtual environment and download the requirements.txt using
 ````
  pip install -r /path/to/requirements.txt
 ````
6. Create a .env file inside the main directory /Assignment-3 and ppoulate the below fields
 ````
  AIRFLOW_UID= <The UID of the server of airflow>
  AIRFLOW_PROJ_DIR=<Base Directory of Airflow. For example ./airflow>
  AWS_ACCESS_KEY = <Your AWS_ACCESS_KEY>
  AWS_SECRET_KEY = <Your AWS_SECRET_KEY>
  USER_BUCKET_NAME = team01
  URL = <URL of the FASTAPI application>
  SECRET_KEY = <SECRET_KEY used to hash the token>

 ````
7. User docker compose to run both FastAPI and Streamlit containers.
````
docker compose up -d --build
````


# How to Run CLI commands
1. Open terminal
2. Go to the directory of /cli
3. Write the following command and press enter 
 ````
  pip install .
 ````
4. This will install the CLI package in local and you can now run cli commands using 'goesNexrad'.
5. The following commands are available through this




 link to documentation: https://codelabs-preview.appspot.com/?file_id=1WeY9z0c7sudPQ1AYpLt4cTWWUyIIraKTsfUFj3M1DmY#0
 ## Declaration 
 Contribution 
 
 1. Anandita Deb : 25%
 2. Cheril Yogi :25%
 3. Shamin Chokshi :25%
 4. Thejas Bharadwaj :25%
 
 WE ATTEST THAT WE HAVEN'T USED ANY OTHER STUDENT'S WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK.
