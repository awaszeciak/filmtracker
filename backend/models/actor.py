from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Identity, String
from datetime import date

class Actor(Base):
    __tablename__ = "aktor"
    __table_args__ = {"schema": "filmtracker"}

    id_aktora: Mapped[int] = mapped_column(Identity(always=False), primary_key=True)
    id_tmdb: Mapped[int | None]
    nazwa: Mapped[str] = mapped_column(String(200))
    data_urodzenia: Mapped[date | None]
    miejsce_urodzenia: Mapped[str | None] = mapped_column(String(200))
    role: Mapped[list["FilmActor"]] = relationship(back_populates="aktor")