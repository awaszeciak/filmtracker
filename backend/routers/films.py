from fastapi import APIRouter, HTTPException
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


@router.get("/films/{id}")
def get_film(id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id_filmu, tytul, rok_produkcji, plakat_url,  data_premiery, opis, czas_trwania FROM filmtracker.film WHERE id_filmu = %s", (id,))
            row = cur.fetchone()

            if (row is None):
                raise HTTPException(404, "Nie znaleziono filmu")

            cur.execute("SELECT g.nazwa FROM filmtracker.film_gatunek fg JOIN filmtracker.gatunek g ON fg.id_gatunku=g.id_gatunku WHERE fg.id_filmu = %s", (id,))
            genres_rows = cur.fetchall()

            genres = []

            for genre_row in genres_rows:
                genres.append(genre_row[0])

            cur.execute("SELECT a.id_aktora, a.nazwa FROM filmtracker.film_aktor fa JOIN filmtracker.aktor a ON fa.id_aktora=a.id_aktora WHERE fa.id_filmu = %s", (id,))
            actors_rows = cur.fetchall()

            actors = []

            for actors_row in actors_rows:
                actor = {"id": actors_row[0], "name": actors_row[1]}
                actors.append(actor)

            cur.execute("SELECT count(*), avg(o.wartosc) FROM filmtracker.ocena o WHERE o.id_filmu = %s", (id,))
            rating_row = cur.fetchone()


    film = {
        "id": row[0],
        "title": row[1],
        "year": row[2],
        "poster_url": row[3],
        "release_date": row[4],
        "description": row[5],
        "runtime": row[6],
        "genres": genres,
        "cast":actors,
        "rating_count":rating_row[0],
        "average_rating":rating_row[1]
    }

    return film