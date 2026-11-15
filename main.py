from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FilmTracker API is running!"}


@app.get("/films")
def get_films():
    pass