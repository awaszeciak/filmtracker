from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Identity, String
from .film_genre import film_genre

class Genre(Base):
    __tablename__ = "gatunek"
    __table_args__ = {"schema": "filmtracker"}

    id_gatunku: Mapped[int] = mapped_column(Identity(always=False), primary_key=True)
    nazwa: Mapped[str] = mapped_column(String(50))
    filmy: Mapped[list["Film"]] = relationship(secondary=film_genre, back_populates="gatunki")