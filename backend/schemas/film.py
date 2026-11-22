from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import date

class FilmListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(validation_alias="id_filmu")
    title: str = Field(validation_alias="tytul")
    year: int = Field(validation_alias="rok_produkcji")
    poster_url: str | None = Field(validation_alias="plakat_url")


class CastItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    character: str | None 


class FilmDetail(FilmListItem):

    release_date: date | None = Field(validation_alias="data_premiery")
    description: str | None = Field(validation_alias="opis")
    runtime: int | None = Field(validation_alias="czas_trwania")

    genres: list[str] = Field(validation_alias="gatunki")
    @field_validator("genres", mode="before")
    @classmethod
    def convert_genres(cls, value):
        return [genre.nazwa for genre in value]
    
    cast: list[CastItem] = Field(validation_alias="obsada")
    @field_validator("cast", mode="before")
    @classmethod
    def convert_cast(cls, value):
        cast = []

        for role in value:
            actor = {
                "id": role.aktor.id_aktora,
                "name": role.aktor.nazwa,
                "character": role.postac
            }
            cast.append(actor)

        return cast
