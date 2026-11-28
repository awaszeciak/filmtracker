from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class FilmDirector(Base):
    __tablename__ = "film_rezyser"
    __table_args__ = {"schema": "filmtracker"}

    id_filmu: Mapped[int] = mapped_column(ForeignKey("filmtracker.film.id_filmu"), primary_key=True)
    id_rezysera: Mapped[int] = mapped_column(ForeignKey("filmtracker.rezyser.id_rezysera"), primary_key=True)

    film: Mapped["Film"] = relationship(back_populates="rezyserzy")
    rezyser: Mapped["Director"] = relationship(back_populates="filmy")