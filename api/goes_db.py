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
mod_path = Path(__file__).parent
relative_path_2 = 'data/s3_goes.dbo'
db_path = (mod_path / relative_path_2).resolve()

router_goes_db = APIRouter()
load_dotenv()

s3client = boto3.client('s3',region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))




#---------------------------------------------------------------------------------------------------------------
#                            API Declarations
#---------------------------------------------------------------------------------------------------------------
#

@router_goes_db.get('/retrieve_goes_years')
def retrieve_goes_years():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT distinct year FROM folders"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return {"years":df}

@router_goes_db.get('/retrieve_goes_day_of_year')
def retrieve_goes_day_of_year(year:str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT distinct day_of_year FROM folders where year = ?"
    df = pd.read_sql_query(query, conn,params=(year,))
    conn.close()
    return {"day_of_year":df}

@router_goes_db.get('/retrieve_goes_hours')
def retrieve_goes_hours(year:str,day_of_year:str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT distinct hour FROM folders where year = ? and day_of_year = ?"
    df = pd.read_sql_query(query, conn,params=(year,day_of_year))
    conn.close()
    return {"hours":df}

@router_goes_db.get('/log_file_download')
def log_file_download(file_name, timestamp,dataset):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS file_logs (file_name text, timestamp text,dataset text)")
    cursor.execute("INSERT INTO file_logs VALUES(?,?,?)",(file_name,timestamp,dataset))    
    conn.commit()
    conn.close()
    return {"Success"}

@router_goes_db.get('/list_goes_files_as_dropdown')
def list_goes_files_as_dropdown(bucket_name:str, prefix:str):

    result = s3client.list_objects(Bucket=bucket_name, Prefix=prefix, Delimiter ='/')
    object_list = [x["Key"].split("/")[-1] for x in result["Contents"]]
    return {"files":object_list}
    