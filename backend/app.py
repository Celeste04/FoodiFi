import pandas as pd
from flask import Flask, jsonify, request

df = pd.read_csv('grocery_store_prices.csv')
df = df.astype({'Product' : 'string'})
for i in range(len(df['Product'])):
    df.loc[i, 'Product'] = df.loc[i, 'Product'].lower().replace(' ', '_')


app = Flask(__name__)
@app.route("/products")
def products():
    data = request.json
    text = data.get('text')
    print(text)
    if text != "":
        return jsonify({'error': 'Text parameter is missing'}), 400
    else:
        return jsonify(get_product_price(text)), 201


def get_product_price(product_name):
    product_name = product_name.lower().replace(' ', '_')
    # Extract the header row for store names
    store_names = df.columns[1:]
    
    # Find the row corresponding to the product
    product_row = df[df["Product"] == product_name]
    
    if product_row.empty:
        return {}
    
    # Extract the prices for the product
    prices = product_row.iloc[0, 1:]
    
    # Create a dictionary mapping store names to prices
    price_dict = dict(zip(store_names, prices))
    
    return price_dict
        

if __name__ == '__main__':
    app.run(debug=True)