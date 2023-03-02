from fastapi import APIRouter
import sqlite3
import pandas as pd
import requests
from pathlib import Path
from dotenv import load_dotenv
import boto3
import os




#---------------------------------------------------------------------------------------------------------------
#                            Connection Declarations
#---------------------------------------------------------------------------------------------------------------
#

db_path = 'data/s3_goes.dbo'

router_goes_db = APIRouter()
load_dotenv()

s3client = boto3.client('s3',region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))




#---------------------------------------------------------------------------------------------------------------
#                            API Declarations
#---------------------------------------------------------------------------------------------------------------
#

@router_goes_db.get('/retrieve_goes_years',tags=['GOES'])
def retrieve_goes_years():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT distinct year FROM folders"
    df = pd.read_sql_query(query, conn)
    tdf = df['year'].tolist()
    conn.close()
    return tdf

@router_goes_db.get('/retrieve_goes_day_of_year',tags=['GOES'])
def retrieve_goes_day_of_year(year:str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT distinct day_of_year FROM folders where year = ?"
    df = pd.read_sql_query(query, conn,params=(year,))
    tdf = df['day_of_year'].tolist()
    conn.close()
    return tdf

@router_goes_db.get('/retrieve_goes_hours',tags=['GOES'])
def retrieve_goes_hours(year:str,day_of_year:str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT distinct hour FROM folders where year = ? and day_of_year = ?"
    df = pd.read_sql_query(query, conn,params=(year,day_of_year))
    tdf = df['hour'].tolist()
    conn.close()
    return tdf

@router_goes_db.get('/log_file_download',tags=['GOES'])
def log_file_download(file_name, timestamp,dataset):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS file_logs (file_name text, timestamp text,dataset text)")
    cursor.execute("INSERT INTO file_logs VALUES(?,?,?)",(file_name,timestamp,dataset))    
    conn.commit()
    conn.close()
    return {"Success"}

@router_goes_db.get('/list_goes_files_as_dropdown',tags=['GOES'])
def list_goes_files_as_dropdown(bucket:str, prefix:str):

    result = s3client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter ='/')
    object_list = [x["Key"].split("/")[-1] for x in result["Contents"]]
    return object_list
    