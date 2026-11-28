import './App.css'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Lists from './pages/Lists'
import Films from './pages/Films'
import Watched from './pages/Watched'
import {Routes, Route} from 'react-router-dom'
import Favourites from './pages/Favourites'
import Search from './pages/Search'
import Stats from './pages/Stats'
import FilmDetail from './pages/FilmDetail'

function App() {
  return(
    <div className="app-layout">
      <Navbar/>
      <main>
        <Routes>
          <Route path="/" element={ <Home />} />
          <Route path="/films" element={<Films />} />
          <Route path="/lists" element={<Lists />} />
          <Route path="/watched" element={<Watched />} />
          <Route path="/favourites" element ={<Favourites />} />
          <Route path="/search" element={<Search />} />
          <Route path="/stats" element={<Stats />} />
          <Route path="/films/:id" element={<FilmDetail />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
