from sqlalchemy import Identity, String, Text, func
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from .film_genre import film_genre

class Film(Base):
    __tablename__ = "film"
    __table_args__ = {"schema": "filmtracker"}

    id_filmu: Mapped[int] = mapped_column(Identity(always=False), primary_key=True)
    id_tmdb: Mapped[int | None]
    tytul: Mapped[str] = mapped_column(String(200))
    rok_produkcji: Mapped[int]
    data_dodania: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())
    data_premiery: Mapped[date | None]
    opis: Mapped[str | None] = mapped_column(Text)
    plakat_url: Mapped[str | None] = mapped_column(Text)
    czas_trwania: Mapped[int | None]
    gatunki: Mapped[list["Genre"]] = relationship(secondary=film_genre, back_populates="filmy")
    obsada: Mapped[list["FilmActor"]] = relationship(back_populates="film")
    