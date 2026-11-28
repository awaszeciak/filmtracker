from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from backend.database import get_db
from backend.models import Film, Rating
from backend.schemas.film import FilmListItem, FilmDetail

router = APIRouter()


@router.get("/films", response_model=list[FilmListItem])
def get_films(db: Session = Depends(get_db)):
    stmt = select(Film)
    all_films = db.scalars(stmt)
    films = all_films.all()

    return films


@router.get("/films/{id}", response_model=FilmDetail)
def get_film(id: int, db: Session = Depends(get_db)):
    stmt = select(Film).where(Film.id_filmu == id)
    film = db.scalars(stmt).first()

    if film is None:
        raise HTTPException(404, "Nie znaleziono filmu")

    rating_stmt = select(func.avg(Rating.wartosc), func.count(Rating.id_oceny)).where(Rating.id_filmu == id)
    rating = db.execute(rating_stmt)
    average_rating, rating_count = rating.one()

    film_data = {
        "id_filmu": film.id_filmu,
        "tytul": film.tytul,
        "rok_produkcji": film.rok_produkcji,
        "plakat_url": film.plakat_url,
        "data_premiery": film.data_premiery,
        "opis": film.opis,
        "czas_trwania": film.czas_trwania,
        "gatunki": film.gatunki,
        "obsada": film.obsada,
        "average_rating": float(average_rating) if average_rating is not None else None,
        "rating_count": rating_count,
        "rezyserzy": film.rezyserzy
    }

    return FilmDetail.model_validate(film_data)
