import { useState, useEffect } from 'react'
import './Films.css'
import { Link } from 'react-router-dom'

function Films() {

    const [films, setFilms] = useState([])

    useEffect(() => {
        fetch('http://127.0.0.1:8001/films').then(response => response.json()).then(data => setFilms(data)).catch(error => console.error('Błąd pobierania filmów: ', error));
    }, [])


    return (
        <div className="films-grid">
            {films.map( film => (
                <Link to={`/films/${film.id}`} className="film-card" key={film.id}>
                    <img src={film.poster_url} alt={film.title} />
                    <h3>{film.title}</h3>
                    <p>{film.year}</p>
                </Link>
            ))}
        </div>
    )
}

export default Films