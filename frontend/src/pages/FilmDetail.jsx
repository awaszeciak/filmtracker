import { useParams } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { Star } from 'lucide-react'
import './FilmDetail.css'

function FilmDetail() {
    const {id} = useParams()
    const [film, setFilm] = useState(null)

    useEffect(()=>{
        fetch(`http://127.0.0.1:8001/films/${id}`).then(response => response.json()).then(data => setFilm(data)).catch(error => console.error('Błąd pobierania filmów: ', error));
    }, [id])

    if (film == null) {
        return <p>Ładowanie filmu...</p>
    }

    return(
        <div className="film-detail">
            <div className="film-detail-card">


                <div className="film-poster">
                    <img src={film.poster_url} alt={`${film.title}`}></img>
                </div>

                <div className="film-info">

                    <h1>{film.title}</h1>
                    <p>{film.year}</p>

                    <div className='film-genres'>
                        {film.genres.map(genre => (
                        <span key={genre}>{genre}</span>
                        ))}
                    </div>


                    <p>{film.description}</p>
                    

                    <div className='film-rating'>
                        {film.average_rating !== null ? (
                            <>
                                <Star size={22} color="#FFAA00"/>
                                <div className="rating-info">
                                    <span className='rating-value'>
                                        {film.average_rating.toFixed(1)} / 10
                                    </span>
                                    <span className='rating-count'>
                                        ({film.rating_count} ocen)
                                    </span>
                                </div>
                            </>
                        ) : (
                            <p>Brak ocen</p>
                        )}
                    </div>


                </div>
       


            </div>
            
            <section className="film-cast">
                <h2>Główna obsada</h2>
                

                <div className="cast-grid">
                    {film.cast.map(actor => (
                        <div className="cast-card" key={actor.id}>
                            <div className="cast-avatar">
                                {actor.name.split(' ').map(word => word.charAt(0)).join('')}
                            </div>   
                          
                            <div className="cast-info">
                                <h3>{actor.name}</h3>
                                <p>{actor.character}</p>
                            </div>
                        </div> 
                    ))}
                </div>
            </section>

            <section className='film-metadata'>
                <h3>Informacje</h3>
                <div className="metadata-row">
                    <span>Rok produkcji</span>
                    <span>{film.year}</span>
                </div>
                <div className="metadata-row">
                    <span>Gatunki</span>
                    <span>{film.genres.join(', ')}</span>
                </div>
                <div className='metadata-row'>
                    <span>Czas trwania</span>
                    <span>{film.runtime} minut</span>
                </div>
            </section>
            
        
        </div>
    )
}

export default FilmDetail