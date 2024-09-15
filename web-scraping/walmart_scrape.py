from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import pandas as pd
from string import punctuation
import re
import requests

BASE_URL = "https://www.walmart.ca/en/search?q="
PAGE_URL = "&page="
SORT_URL = "&sort=price_low"

HEADERS = {'User-Agent': UserAgent().random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}
COLUMNS = ['Search','Item','Price']


prev_scraped_path = 'walmart_prev_scraped.csv'
def save_prev_scraped(products:pd.DataFrame):
    with open(prev_scraped_path, 'a') as f:
        f.write('\n')
    products.to_csv(prev_scraped_path, mode='a', header=False, index=False)

def load_prev_scraped():
    try:
        return pd.read_csv(prev_scraped_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(prev_scraped_path, index=False) # save empty CSV
        return df
    
prev_scraped = load_prev_scraped()

def convert_price_to_float(price:str) -> float:
    price_float = 0
    if '$' in price:
        price_float = float(re.sub('[^0-9.]', "", price))
    elif '¢' in price:
        cents = int(re.sub('[^0-9]', "", price))
        price_float = cents/100
    return price_float

def convert_name_to_search_query(item_name:str) -> str:
    item_name = item_name.lower().translate(str.maketrans('','',punctuation))
    item_name = item_name.replace(" ", "+")
    return item_name

def retrieve_items_and_prices(item_name:str):
    item_name = convert_name_to_search_query(item_name)

    # check if item has been previously searched
    if item_name in prev_scraped['Search']:
        return prev_scraped['Search' == item_name]

    # dataframe of items, prices, and searches
    products = pd.DataFrame(columns=COLUMNS)
    pg = 1
    while True:
        # create URL to be searched
        search_url = BASE_URL+item_name+PAGE_URL+str(pg)+SORT_URL
        page = requests.get(search_url, headers=HEADERS, timeout=5)

        # parse through page using bs4
        soup = BeautifulSoup(page.content, 'html.parser')
        items = soup.find('div', {'data-testid' : 'item-stack'}) # get all item divs
        if items is None: # break out of while loop when there are no more items to scrape
            break
        name_text = []
        price_text = []
        for i in items.children:
            # get item's name and price
            name = i.find('span', {'data-automation-id' : 'product-title'}).get_text()
            price = convert_price_to_float(i.find('div', {'data-automation-id' : 'product-price'}).div.get_text())
            # check if item is in stock. if so, add it to list
            if len(i.find('div', {'data-automation-id' : 'inventory-status'})) == 0:
                name_text.append(name)
                price_text.append(price)

        page_names_prices = pd.DataFrame(zip([item_name] * len(name_text), name_text, price_text), columns=COLUMNS)
        # add scraped data to dataframe for safe keeping
        products = (page_names_prices.copy() if products.empty else pd.concat([products, page_names_prices], ignore_index=True))
        # go to next page
        pg += 1
        time.sleep(10) # wait for 10 seconds so walmart doesn't block the scraping
    save_prev_scraped(products)
    print(products)
    return products

# testing
# retrieve_items_and_prices("apple juice")