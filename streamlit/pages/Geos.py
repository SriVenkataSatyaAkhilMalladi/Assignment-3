import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import os
import sys
sys.path.insert(1, '../../streamlit')
import boto3
import logging
from dotenv import load_dotenv
import io
import requests
from bs4 import BeautifulSoup
import time
import sys
import json


#---------------------------------------------------------------------------------------------------------------
#                            Connection Declarations
#---------------------------------------------------------------------------------------------------------------
#
load_dotenv()

s3client = boto3.client('s3',region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))


#---------------------------------------------------------------------------------------------------------------
#                            Variable Declarations
#---------------------------------------------------------------------------------------------------------------
#

st.header("Explore the GEOS-18 Dataset")

bucket = 'noaa-goes18'
prefix = 'ABI-L1b-RadC/'
USER_BUCKET_NAME = os.environ.get('USER_BUCKET_NAME')

#---------------------------------------------------------------------------------------------------------------
#                            Function Definitions
#---------------------------------------------------------------------------------------------------------------
#

def json_data(js):
    data = json.loads(js)
    return list(data.values())

#---------------------------------------------------------------------------------------------------------------
#                            Streamlit Code
#---------------------------------------------------------------------------------------------------------------
#

col1, col2 = st.columns(2,gap='large')
if st.session_state['access_token'] != '':
    with col1:
        st.header("Search using fields ")
        headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
   

        #Selecting station 
        station_geos = st.text_input(
            'Please select the station', placeholder= 'GEOS 18')

        url = str(os.environ.get('URL')) + 'retrieve_goes_years'
        response = requests.get(url,headers=headers).json()
       #store log responses from api
        #Selecting Year
        year_geos = st.selectbox(
            'Please select the year',
            options=response)
        
        #Retrieving day of year
        url = str(os.environ.get('URL')) + 'retrieve_goes_day_of_year'
        response = requests.get(url,headers=headers,params={"year":year_geos}).json()
       #store log responses from api

        #Day of Year
        day_of_year_geos = st.selectbox('Please select the Day of Year',options=response)
       #store log responses from api

        #Retrieving hours
        url = str(os.environ.get('URL')) + 'retrieve_goes_hours'
        response = requests.get(url,headers=headers,params={"year":year_geos,"day_of_year":day_of_year_geos}).json()

        hour_of_day = st.selectbox('Please select the Hour',options=response)

        #Retrieving Files as dropdown
        prefix = 'ABI-L1b-RadC/{}/{}/{}/'.format(year_geos,day_of_year_geos,hour_of_day)
        url = str(os.environ.get('URL')) + 'list_goes_files_as_dropdown'
        response = requests.get(url,headers=headers,params={"bucket":bucket,"prefix":prefix}).json()

        selected_file = st.selectbox("Select file for download:", options=response)

        #Transfering selected file to S3 bucket 
        if st.button('Submit'):
            with st.spinner('Retrieving details for the file you selected, wait for it....!'):
                time.sleep(5)

                # final_url = 'https://{}.s3.amazonaws.com/index.html#ABI-L1b-RadC/{}/{}/{}/{}'.format(bucket,year_geos,day_of_year_geos,hour_of_day,selected_file)
                name_of_file = {"filename":str(selected_file)}
            
        
                
                try:
                    #Transfer File
                    url = str(os.environ.get('URL')) + 'transfer_file'
                    response = requests.get(url,headers=headers,params=name_of_file)
                    timestamp = time.time()
                    data = response.json()
   

                    if response.status_code ==  200:
                        st.write("S3 Team Bucket link :",data['S3-Personal'])
                        st.write("S3 Public GOES link :",data['S3-Public'])
                        #Log the download if successful
                        url = str(os.environ.get('URL')) + 'log_file_download'
                        response = requests.get(url,headers=headers,params={"file_name":selected_file,"timestamp":timestamp,"dataset":bucket})
                    
                except:
                    st.error("An error occured")
                
                




                

    with col2:
        
        st.header("Search using file name ")
        filename = st.text_input("Enter the filename:")
        json_file_name = {"filename":filename}
        if st.button('Get the Link'):
            try:
                url = os.environ.get('URL') + 'filename_url_gen_goes'
                headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
                response = requests.get(url,headers=headers,params=json_file_name)
            except any:
                st.error("An error occured")
            data = response.json()
            if(response.status_code == 200):
                st.write("S3 Public GOES Bucket Link:",data['url'])
            elif(response.status_code == 400):
                st.warning('Filename does not exist')
            elif(response.status_code == 406):
                st.warning('File name format is invalid')

else:
    st.warning("Login First")



