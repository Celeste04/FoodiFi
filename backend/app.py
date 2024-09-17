import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS
from ..web_scraping import walmart_scrape, giant_tiger_scrape

df = pd.read_csv('grocery_store_prices.csv')
df = df.astype({'Product' : 'string'})
for i in range(len(df['Product'])):
    df.loc[i, 'Product'] = df.loc[i, 'Product'].lower().replace(' ', '_')


app = Flask(__name__)
CORS(app)

@app.route("/products/<product_name>")
def products(product_name):
    response = jsonify({'error': 'Product name is missing'})
    if product_name == "":
        response = jsonify({'error': 'Produce name is missing'})
    else:
        response = jsonify(get_product_price(product_name))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def get_product_price(product_name:str):
    # get walmart and giant tiger prices for a specific product search
    wm_data = walmart_scrape.retrieve_items_and_prices(product_name)
    gt_data = giant_tiger_scrape.retrieve_items_and_prices(product_name)
    
    # get the cheapest item in each dataframe
    wm_item, wm_price = get_cheapest_price(wm_data)
    # gt_item, gt_price = get_cheapest_price(gt_data) # commented out until giant tiger also returns a dataframe

    # return a JSON object
    return jsonify({"Giant Tiger" : ["item", "price"], "Walmart" : [wm_item, wm_price]}) # rmbr to fill in giant tiger item & price later
        
def get_cheapest_price(data:pd.DataFrame):
    min_price = 100000000
    min_item = "na"
    for i in range(len(data['Price'])):
        item = str(df.iloc[i, 1])
        price = float(df.iloc[i, 2])
        if price < min_price:
            min_price = price
            min_item = item
    return min_item, min_price


if __name__ == '__main__':
    app.run(debug=True)