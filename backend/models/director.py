from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Identity, String

class Director(Base):
    __tablename__ = "rezyser"
    __table_args__ = {"schema": "filmtracker"}

    id_rezysera: Mapped[int] = mapped_column(Identity(always=False), primary_key=True)
    id_tmdb: Mapped[int | None]
    nazwa: Mapped[str] = mapped_column(String(200))

    filmy: Mapped[list["FilmDirector"]] = relationship(back_populates="rezyser")