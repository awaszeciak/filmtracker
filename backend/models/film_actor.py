from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class FilmActor(Base):
    __tablename__ = "film_aktor"
    __table_args__ = {"schema": "filmtracker"}


    id_filmu: Mapped[int] = mapped_column(ForeignKey("filmtracker.film.id_filmu"), primary_key=True)
    id_aktora: Mapped[int] = mapped_column(ForeignKey("filmtracker.aktor.id_aktora"), primary_key=True)
    postac: Mapped[str | None] = mapped_column(String(150))

    film: Mapped["Film"] = relationship(back_populates="obsada")
    aktor: Mapped["Actor"] = relationship(back_populates="role")
