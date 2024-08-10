import React, { useState, useEffect, useRef } from 'react';

import { v4 as uuidv4 } from 'uuid';
import './list-styles.css';

function ListForm(props) {
    const [input, setInput] = useState('');
    const inputRef = useRef(null);
    useEffect(()=>{
        inputRef.current.focus();
    })
    const handleChange = e => {
        setInput(e.target.value);
    }

    const handleSubmit = e => {
        e.preventDefault();
        props.onSubmit({
            id: uuidv4(),
            text: input
        });

        setInput('');
    };

    return (
        <form className="list-form" onSubmit={handleSubmit}>
            <input 
            type="text" 
            placeholder="Add item" 
            value={input} 
            name="text" 
            className="list-input"
            onChange={handleChange}
            ref={inputRef}></input>

            <button className="list-button">Add</button>
        </form>
    );
}

export default ListForm;
