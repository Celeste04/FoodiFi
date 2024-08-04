import { useState, useEffect } from 'react';
import './shopping-list.css';
export default function ShoppingList() {
    const [items, setItems] = useState([]);
    const [input, setInput] = useState("");
    const [product, setProduct] = useState("");
    const [priceData, setPriceData] = useState([{}]);

    const getProductPrices = async () => {
        try {
            const response = await axios.post('/sentiment-analysis', {
                text: product
            });
            setPriceData(response.data);
            console.log(data)
        } catch (err) {
            console.log(err);
        }
        
    }
    
    useEffect(() => {
        fetch("/products").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log(data)
            }
        )
    })

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