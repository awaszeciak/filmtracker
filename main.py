from fastapi import FastAPI
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.get("/films")
def get_films():
    with psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=5432,
        dbname="filmtracker",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    ) as conn:


        with conn.cursor() as cur:
            cur.execute("SELECT id_filmu, tytul, rok_produkcji, plakat_url FROM filmtracker.film ORDER BY tytul")

            rows = cur.fetchall()

    films = []

    for row in rows:
        film = {
            "id": row[0],
            "title": row[1],
            "year": row[2],
            "poster_url": row[3]
        }

        films.append(film)

    return films

