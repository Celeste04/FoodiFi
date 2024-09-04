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
    hdrs = {'User-Agent': UserAgent().chrome,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}
    proxy_addresses = {
    'socks5' : 'http://72.214.108.67:4145',
    'socks5' : 'http://98.181.137.80:4145'
    }
    url = base_url + "&page="+str(i)
    page = requests.get(url=url, headers=hdrs, proxies=proxy_addresses)
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup)
    prices = soup.find_all('div', {'data-automation-id' : 'product-price'}, limit=50)
    names = soup.find_all('span', {'data-automation-id' : 'product-title'}, limit=50)
    name_text = []
    price_text = []
    
    for n, p in zip(names, prices):
        name_text.append(n.get_text())
        price_text.append(p.div.get_text())

    products = pd.concat([pd.DataFrame(zip(name_text, price_text), columns=products.columns), products], ignore_index=True)
    print(len(name_text))
    if i < pgs:
        time.sleep(30)

products.to_csv("scraped-data/"+csv_file, index=False)
# print(products)