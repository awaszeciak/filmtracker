import os
from dotenv import load_dotenv
from contextlib import closing
import requests
import psycopg

# pobieranie klucza do api z .env
load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

if not (api_key):
    raise ValueError("API key is missing")

# zapytanie do TMDB API
def fetch_movie(movie_id):
    url = "https://api.themoviedb.org/3/movie/" + str(movie_id)

    params = {
        "api_key": api_key,
        "language": "pl-PL",
        "append_to_response": "credits"
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    movie = response.json()

    return movie





# dodawanie filmu do bazy danych
def save_movie(cur, movie):

    release_date = movie.get("release_date")

    if not release_date:
        raise ValueError("Movie release date is missing")

    poster_path = None

    poster_url = "https://image.tmdb.org/t/p/w500"

    if movie.get("poster_path"):
        poster_path = poster_url + movie["poster_path"]

    cur.execute(
        "INSERT INTO filmtracker.film (id_tmdb, rok_produkcji, tytul, data_premiery, opis, czas_trwania, plakat_url) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id_tmdb) DO UPDATE SET tytul = EXCLUDED.tytul, opis = EXCLUDED.opis, czas_trwania=EXCLUDED.czas_trwania, plakat_url = EXCLUDED.plakat_url, rok_produkcji = EXCLUDED.rok_produkcji, data_premiery = EXCLUDED.data_premiery",
        (
            movie["id"],
            int(release_date[:4]),
            movie["title"],
            release_date,
            movie["overview"],
            movie["runtime"],
            poster_path
        )
    )

    cur.execute(
        "SELECT id_filmu FROM filmtracker.film WHERE id_tmdb = %s",
        (movie['id'],)
    )

    result_id = cur.fetchone()
    movie_id = result_id[0]

    return movie_id


def save_genres(cur, movie_id, genres):

    for genre in genres:
        cur.execute(
            "INSERT INTO filmtracker.gatunek (nazwa) VALUES (%s) ON CONFLICT (nazwa) DO NOTHING",
            (
                genre['name'],
            )
        )

        cur.execute(
            "SELECT id_gatunku FROM filmtracker.gatunek WHERE nazwa = %s",
            (genre["name"],)
        )

        result = cur.fetchone()
        genre_id = result[0]

        cur.execute(
            "INSERT INTO filmtracker.film_gatunek (id_filmu, id_gatunku) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (
                movie_id,
                genre_id
            )
        )



def save_actors(cur, movie_id, cast):

    actorurl = "https://api.themoviedb.org/3/person/"

    params={
        "api_key": api_key,
        "language": "pl-PL"
    }

    for actor in cast[:10]:
        actor_id = actor["id"]
        actor_url = actorurl + str(actor_id)



        actor_response = requests.get(actor_url, params=params, timeout=20)
        actor_response.raise_for_status()

        actor_data = actor_response.json()

        cur.execute(
            "INSERT INTO filmtracker.aktor (id_tmdb, nazwa, data_urodzenia, miejsce_urodzenia) VALUES (%s, %s, %s, %s) ON CONFLICT (id_tmdb) DO UPDATE SET nazwa = EXCLUDED.nazwa, data_urodzenia = EXCLUDED.data_urodzenia, miejsce_urodzenia = EXCLUDED.miejsce_urodzenia",
            (
                actor_id,
                actor_data["name"],
                actor_data.get("birthday"),
                actor_data.get("place_of_birth")
            )
        )

        cur.execute(
            "SELECT id_aktora FROM filmtracker.aktor WHERE id_tmdb = %s",
            (actor_id,)
        )

        db_actor_id = cur.fetchone()
        id_actor = db_actor_id[0]

        cur.execute(
            "INSERT INTO filmtracker.film_aktor (id_filmu, id_aktora, postac) VALUES (%s, %s, %s) ON CONFLICT (id_filmu, id_aktora) DO UPDATE SET postac = EXCLUDED.postac", 
            (
                movie_id,
                id_actor,
                actor["character"]
            )
        )

def save_directors(cur, movie_id, crew):

    for person in crew:
        if person["job"] == "Director":
            cur.execute("INSERT INTO filmtracker.rezyser (id_tmdb, nazwa) VALUES (%s, %s) ON CONFLICT (id_tmdb) DO NOTHING", (
                person["id"],
                person["name"]
            ))

            cur.execute(
                "SELECT id_rezysera FROM filmtracker.rezyser WHERE id_tmdb = %s",
                (person["id"],)
            )

            result = cur.fetchone()
            director_id = result[0]

            cur.execute(
                "INSERT INTO filmtracker.film_rezyser (id_filmu, id_rezysera) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (
                    movie_id,
                    director_id
                )
            )

def import_movie(movie_id):
  
    movie = fetch_movie(movie_id)

    

    # laczenie z baza danych
    with closing(psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=5432,
        dbname="filmtracker",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    )) as conn:

        with conn:
            with conn.cursor() as cur:
                db_movie_id = save_movie(cur, movie)
                save_genres(cur, db_movie_id, movie["genres"])
                save_actors(cur, db_movie_id, movie["credits"]["cast"])
                save_directors(cur, db_movie_id, movie["credits"]["crew"])


def import_movies(movie_ids):
    for movie_id in movie_ids:
        try:
            import_movie(movie_id)
            print(f"Imported movie TMDB ID: {movie_id}")
        except (ValueError, requests.RequestException, psycopg.Error) as e:
            print(f"Failed to import movie TMDB ID: {movie_id} : {e}")
        


if __name__ == "__main__":
    import_movies([354912, 77, 37165, 361743, 475557,  106646, 872585, 634649, 424694, 313369, 549559, 453])



