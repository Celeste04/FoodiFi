import { useState, useEffect } from 'react';
import './shopping-list.css';
import List from '../components/list';
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
        <div className="page-container">
            <h1 className='shopping-list-title'>Shopping List</h1>
            <List></List>
        </div>
    );
}