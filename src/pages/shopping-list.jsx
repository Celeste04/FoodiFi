import { useState } from 'react';
import './shopping-list.css';
export default function ShoppingList() {
    const [items, setItems] = useState([]);
    const [input, setInput] = useState("");
    return (
        <div>
            <h1 className='shopping-list-title'>Shopping List</h1>
            <div className="list-container">
                <div className ="add-items-container">
                   <input type='text' value={input} onChange={(e) => {setInput(e.target.value)}} placeholder='Add Item'></input>
                </div>
            </div>
        </div>
    );
}