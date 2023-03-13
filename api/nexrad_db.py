from fastapi import APIRouter
import sqlite3
import pandas as pd
import requests
from pathlib import Path
from dotenv import load_dotenv
import boto3
import os
import ast
import api.jwt as jwt
#---------------------------------------------------------------------------------------------------------------
#                            Connection Declarations
#---------------------------------------------------------------------------------------------------------------
#
db_path = 'data/s3_nexrad.dbo'

router_nexrad_db = APIRouter()
load_dotenv()


s3client = boto3.client('s3',region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))


#---------------------------------------------------------------------------------------------------------------
#                            API Declarations
#---------------------------------------------------------------------------------------------------------------
#


@router_nexrad_db.get('/retieve_nexrad_months',tags = ['NEXRAD'])
def retieve_nexrad_months(year:str,current_user: jwt.User = jwt.Depends(jwt.get_current_active_user)):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT distinct month FROM folders where year = ?"
    df = pd.read_sql_query(query, conn, params=(year,))
    tdf = df['month'].tolist()
    conn.close()
    return tdf

@router_nexrad_db.get('/retieve_nexrad_days',tags = ['NEXRAD'])
def retieve_nexrad_days(year:str,month:str,current_user: jwt.User = jwt.Depends(jwt.get_current_active_user)):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT distinct day FROM folders where year = ? and month = ?"
    df = pd.read_sql_query(query, conn,params=(year,month))
    tdf = df['day'].tolist()
    conn.close()
    return tdf


@router_nexrad_db.get('/retieve_nexrad_stations',tags = ['NEXRAD'])
def retieve_nexrad_stations(year:str,month:str,day:str,current_user: jwt.User = jwt.Depends(jwt.get_current_active_user)):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = 'SELECT nexrad_station FROM folders where year = ? and month = ? and day = ?'
    tdf = pd.read_sql_query(query, conn,params=(year,month,day))
    conn.close()
    df = tdf['nexrad_station'][0]
    df1 = ast.literal_eval(df)

    return df1


@router_nexrad_db.get('/list_nexrad_files_as_dropdown',tags = ['NEXRAD'])
def list_nexrad_files_as_dropdown(bucket_name:str, prefix:str,current_user: jwt.User = jwt.Depends(jwt.get_current_active_user)):

    result = s3client.list_objects(Bucket=bucket_name, Prefix=prefix, Delimiter ='/')
    object_list = [x["Key"].split("/")[-1] for x in result["Contents"]]
    return object_list
    