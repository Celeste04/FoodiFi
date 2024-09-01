import { useState, useEffect } from 'react';
import './shopping-list.css';
import List from '../components/list';
import frogPic from '../images/frog.svg';
import speechBubble from '../images/speechbubble.svg'
import axios from 'axios';
import CurrencyInput from 'react-currency-input-field';


export default function ShoppingList() {
    const [goal, setGoal] = useState(0);
    /*
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
    */

    return (
        <div className="page-container">
            <h1 className='shopping-list-title'>Shopping List</h1>
            <div className="content-wrapper">
                <List></List>
                <div className="spending-goal">
                    <h3>Spending Goal: $</h3>
                    <CurrencyInput
                    className="goal-input"
                    id="input-example"
                    name="input-name"
                    placeholder="Enter your spending goal"
                    defaultValue={0}
                    decimalsLimit={2}
                    onValueChange={(value, name, values) => {
                        setGoal(value)
                        }}
                    />
                </div>
                <img src={frogPic} className="frog-pic"></img>
                <div className="advice"></div>
            </div>
        </div>
    );
}