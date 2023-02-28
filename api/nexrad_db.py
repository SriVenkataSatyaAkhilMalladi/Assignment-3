import ast
from fastapi import APIRouter
import sqlite3
import pandas as pd
import requests
from pathlib import Path

mod_path = Path(__file__).parent
relative_path_1 = 'data/s3_nexrad.dbo'
db_path = (mod_path / relative_path_1).resolve()

router_nexrad_db = APIRouter()


@router_nexrad_db.get('/retieve_nexrad_months')
def retieve_nexrad_months(year:str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT distinct month FROM folders where year = ?"
    df = pd.read_sql_query(query, conn, params=(year,))
    conn.close()
    return df


@router_nexrad_db.get('/retieve_nexrad_days')
def retieve_nexrad_days(year:str,month:str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT distinct day FROM folders where year = ? and month = ?"
    df = pd.read_sql_query(query, conn,params=(year,month))
    conn.close()
    return df


@router_nexrad_db.get('/retieve_nexrad_stations')
def retieve_nexrad_stations(year:str,month:str,day:str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = 'SELECT nexrad_station FROM folders where year = ? and month = ? and day = ?'
    tdf = pd.read_sql_query(query, conn,params=(year,month,day))
    conn.close()
    df = tdf['nexrad_station'][0]
    df1 = ast.literal_eval(df)

    return df1

