import pandas as pd
from nltk.tokenize import wordpunct_tokenize

# get lowest price between walmart and giant tiger
def get_lowest_price(search_entry):
    walmart_product, walmart_price = get_walmart_price(search_entry)
    gt_product, gt_price = "tiger", 0.99 # placeholder values
    if gt_price > walmart_price:
        return walmart_product, walmart_price
    else:
        return gt_product, gt_price

def get_walmart_price(search_entry:str):
    df = pd.read_csv('..\web-scraping\store-data\walmart_grocery_prices_keywords.csv', index_col=None)
    df = df.astype({'Product Name' : 'string', 'Keywords' : 'string'})
    print(df.info())
    # find product with best match to search terms
    max_match = 0.0
    walmart_price = 0.0
    walmart_product = ""

    for i in range(len(df['Product Name'])):
        # print(df.iloc[i])
        name, price, kw = df.iloc[i]
        kw = str(kw).split("_")
        # get match score
        match_score = get_name_match(search_entry, kw)
        if match_score > max_match:
            max_match = match_score
            walmart_price = price
            walmart_product = name

    return walmart_product, walmart_price

def get_name_match(name:str, kw) -> float:
    s = wordpunct_tokenize(name)
    ctr = 0
    for i in kw:
        if i in s:
            ctr += 1
    return ctr / len(kw)

print(get_walmart_price("sunflower oil"))

def get_shopping_list(product_list):
    return