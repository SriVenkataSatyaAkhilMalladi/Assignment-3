import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import os
import boto3
import logging
from dotenv import load_dotenv
from fastapi import HTTPException
import io
import requests
from bs4 import BeautifulSoup
import time



#---------------------------------------------------------------------------------------------------------------
#                            Connection Declarations
#---------------------------------------------------------------------------------------------------------------
#

load_dotenv()

st.header("Explore the NEXRAD Dataset")

s3client = boto3.client('s3',region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))

#---------------------------------------------------------------------------------------------------------------
#                            Variable Declarations
#---------------------------------------------------------------------------------------------------------------
#
bucket = 'noaa-nexrad-level2'

prefix = 'ABI-L1b-RadC/'
USER_BUCKET_NAME = os.environ.get('USER_BUCKET_NAME')


#---------------------------------------------------------------------------------------------------------------
#                            streamlit code
#---------------------------------------------------------------------------------------------------------------
#
col1, col2 = st.columns(2, gap = 'large')
if st.session_state['access_token'] != '':
    with col1:
        st.header("Search using fields ")
        headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}


        #Selecting Year
        year_nexrad = st.selectbox(
            'Please select the year',
            ('2022', '2023'))
        
        url = str(os.environ.get('URL')) + 'retieve_nexrad_months'
        response = requests.get(url,headers=headers,params={"year":year_nexrad}).json()
        
        #Month of Year
        month_of_year_nexrad = st.selectbox('Please select the Month',options=response)

        url = str(os.environ.get('URL')) + 'retieve_nexrad_days'
        response = requests.get(url,headers=headers,params={"year":year_nexrad,"month":month_of_year_nexrad}).json()
        

        #Day of Month
        day_of_month_nexrad = st.selectbox('Please select the Day of the month',options=response)

        url = str(os.environ.get('URL')) + 'retieve_nexrad_stations'
        response = requests.get(url,headers=headers,params={"year":year_nexrad,"month":month_of_year_nexrad,"day":day_of_month_nexrad}).json()
        

        #Station code selector 
        
        selected_stationcode = st.selectbox('Please select the station',options=response,key='day')



        #MADE CHANGES TO BELOW FUNCTION - ADDED PREFIX_FILE 
        prefix_file = '{}/{}/{}/{}/'.format(year_nexrad,month_of_year_nexrad,day_of_month_nexrad,selected_stationcode)


        url = str(os.environ.get('URL')) + 'list_nexrad_files_as_dropdown'
        response = requests.get(url,headers=headers,params={"bucket_name":bucket,"prefix":prefix_file}).json()


        #Filename selector 
        selected_file = st.selectbox("Select file for download:", options=response,key='file')


        #Transfering selected file to S3 bucket 
        if st.button('Submit'):
            with st.spinner('Retrieving details for the file you selected, wait for it....!'):
                time.sleep(5)
                name_of_file = {"filename":str(selected_file)}
                
                url = str(os.environ.get('URL')) + 'transfer_file_nexrad'
                headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
                response = requests.get(url,headers=headers,params=name_of_file)
                data = response.json()
                st.write("S3 Team Bucket link :",data['S3-Personal'])
                st.write("S3 Public GOES link :",data['S3-Public'])

                timestamp = time.time()
                url = str(os.environ.get('URL')) + 'log_file_download'
                response = requests.get(url,headers=headers,params={"file_name":selected_file,"timestamp":timestamp,"dataset":bucket})
                


    with col2:
        st.header("Search using file name ")
            
        filename = st.text_input("Enter the filename:")
        json_file_name = {"filename":filename}
        if st.button('Get the Link'):
            try:
                url = os.environ.get('URL') + 'filename_url_gen_nexrad'
                headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
                response = requests.get(url,headers=headers,params=json_file_name)
            except:
                print("Failed")
            data = response.json()
            if(response.status_code == 200):
                st.write(data['url'])
            elif(response.status_code == 400):
                st.warning('Filename does not exist')
            elif(response.status_code == 406):
                st.warning('File name format is invalid')

            
else:
    st.warning("Login First")
