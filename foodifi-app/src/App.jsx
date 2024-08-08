import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/home';
import ShoppingList from './pages/shopping-list';
import ShoppingLists from './pages/shopping-lists';
import NoPage from './pages/nopage';

export default function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route index element={<Home/>}/>
          <Route path="/home" element={<Home/>}/>
          <Route path="/shopping-list" element={<ShoppingList/>}/>
          <Route path="/shopping-lists" element={<ShoppingLists/>}/>
          <Route index="*" element={<NoPage/>}/>
        </Routes>
      </BrowserRouter>
    </div>
  )
}