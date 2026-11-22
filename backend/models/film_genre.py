from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import Base

film_genre = Table(
    "film_gatunek",
    Base.metadata,
    Column("id_filmu", Integer, ForeignKey("filmtracker.film.id_filmu"), primary_key=True),
    Column("id_gatunku", Integer, ForeignKey("filmtracker.gatunek.id_gatunku"), primary_key=True),
    schema = "filmtracker"
)