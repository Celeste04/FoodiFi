import pandas as pd
from flask import Flask
from flask_restful import Resource, Api

app = Flask("GroceryStorePricesAPI")
api = Api(app)
df = pd.read_csv('api\grocery_store_prices.csv')
df = df.astype({'Product' : 'string'})
for i in range(len(df['Product'])):
    df.loc[i, 'Product'] = df.loc[i, 'Product'].lower().replace(' ', '_')

def url_friendly(string):
    return string.lower().replace(' ', '_')

class GroceryPrice(Resource):
    

    def get(self, product_name):
        product_name = url_friendly(product_name)
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
        
    

api.add_resource(GroceryPrice, '/products/<product_name>')

if __name__ == '__main__':
    app.run()