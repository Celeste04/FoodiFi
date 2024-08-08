import { useState } from 'react';
import './shopping-list.css';
import List from '../components/list';
export default function ShoppingList() {
    const [items, setItems] = useState([]);
    const [input, setInput] = useState("");
    return (
        <div className="page-container">
            <h1 className='shopping-list-title'>Shopping List</h1>
            <List></List>
        </div>
    );
}