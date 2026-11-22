from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.database import get_db
from backend.models import Film
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

    return film
