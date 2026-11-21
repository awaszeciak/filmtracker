from fastapi import APIRouter
from backend.database import get_connection

router = APIRouter()


@router.get("/films")
def get_films():


    with get_connection() as conn:
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


