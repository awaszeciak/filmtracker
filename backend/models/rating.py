from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Identity, Numeric, func, ForeignKey
from .base import Base
from datetime import datetime
from decimal import Decimal

class Rating(Base):
    __tablename__ = "ocena"
    __table_args__ = {"schema": "filmtracker"}

    id_oceny: Mapped[int] = mapped_column(Identity(always=False), primary_key=True)
    id_uzytkownika: Mapped[int] = mapped_column(ForeignKey("filmtracker.uzytkownik.id_uzytkownika"))
    id_filmu: Mapped[int] = mapped_column(ForeignKey("filmtracker.film.id_filmu"))
    wartosc: Mapped[Decimal] = mapped_column(Numeric(3, 1))
    data_wystawienia: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())
    data_modyfikacji: Mapped[datetime | None]