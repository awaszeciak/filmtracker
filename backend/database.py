import psycopg
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=5432,
        dbname="filmtracker",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    ) 

    return conn