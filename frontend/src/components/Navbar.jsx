import './Navbar.css'
import { NavLink } from 'react-router-dom'
import { Clapperboard, Search} from 'lucide-react'

function Navbar() {
    return (
        <header className="navbar">
            <div className="navbar-brand">
                <div className="navbar-brand-icon">
                    <Clapperboard size={20} strokeWidth={2.5}/>
                </div>
                <span>Film<span className="brand-accent">Tracker</span></span>
            </div>
            <nav>
                <ul>
                    <li>
                        <NavLink to="/">Strona główna</NavLink>
                    </li>
                    <li>
                        <NavLink to="/films">Filmy</NavLink>
                    </li>
                    <li>
                        <NavLink to="/lists">Moje listy</NavLink>
                    </li>
                    <li>
                        <NavLink to="/favourites">Ulubione</NavLink>
                    </li>
                    <li>
                        <NavLink to="/stats">Statystyki</NavLink>
                    </li>
                </ul>
            </nav>
            <div className='navbar-actions'>
                <NavLink to="/search" aria-label="Szukaj">
                    <Search size={20}/>
                </NavLink>

            </div>

        </header>
    )
}

export default Navbar