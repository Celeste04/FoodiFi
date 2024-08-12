import time
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

print("Enter walmart.ca URL:")
base_url = str(input())
print("Enter # of pages:")
pgs = int(input())
print("Enter name of .csv file (with .csv extension):")
csv_file = str(input())

products = pd.DataFrame(columns=['Product Name', 'Product Price'])

for i in range(1, pgs+1):
    hdrs = {'User-Agent': UserAgent().random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}
    url = base_url + "?page="+str(i)
    page = requests.get(url=url, headers=hdrs)
    soup = BeautifulSoup(page.content, 'lxml')
    prices = soup.find_all('div', {'data-automation-id' : 'product-price'})
    names = soup.find_all('span', {'data-automation-id' : 'product-title'})
    name_text = []
    price_text = []
    
    for n, p in zip(names, prices):
        name_text.append(n.get_text())
        price_text.append(p.div.get_text())

    products = pd.concat([pd.DataFrame(zip(name_text, price_text), columns=products.columns), products], ignore_index=True)
    time.sleep(5)

products.to_csv("data/"+csv_file, index=False)
# print(products)