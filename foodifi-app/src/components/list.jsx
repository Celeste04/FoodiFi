import React, { useState } from 'react';
import ListForm from './list-form';
import ListItem from './list-item';
import  './list-styles.css'

function List() {
    const [items, setItems] = useState([]);

    const addItem = item => {
        if (!item.text || /^\s*$/.test(item.text)) {
            return;
        }
        const newItems = [item, ...items];
        setItems(newItems);
        console.log(newItems); 
    };
    
    const removeItem = id => {
        const removeArr = [...items].filter(item => item.id !== id);
        setItems(removeArr);
    };

    const updateItem = (itemId, newValue) => {
        if (!newValue.text || /^\s*$/.test(newValue.text)) {
            return;
        }
        setItems(prev=> prev.map(obj => (obj.id === itemId ?  newValue : obj)))
    }

    return (
        <div className="list-wrapper">
            <ListForm onSubmit={addItem} />
            <ListItem items={items} removeItem={removeItem} updateItem={updateItem}/>
        </div>
    );
}

export default List;