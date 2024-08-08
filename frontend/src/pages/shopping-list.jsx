import { useState, useEffect } from 'react';
import './shopping-list.css';
import Button from '../components/button';
import axios from 'axios';


export default function ShoppingList() {
    const [items, setItems] = useState([]);
    const [input, setInput] = useState("");
    const [product, setProduct] = useState("");
    const [priceData, setPriceData] = useState([{}]);

   useEffect(() =>  {
        async function getProductPrice() {
            const header = {'Access-Control-Allow-Origin':"*", 'Content-Type': 'application/json',}
            try {
                console.log(product);
                const res = await axios({
                    url: "http://127.0.0.1:5000/products/" + product.toLowerCase().replace(" ", "_"),
                    method: 'get',
                    headers: header,
                });
                const data = await res.data;
                setPriceData(data);
                console.log(data);
                
            } catch (err) {
                console.log(err);
            }
        }
        if (product === ""){
            return;
        }
        else {
            getProductPrice();
        }
    }, [product, priceData]); // will automatically update priceData when product is set

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