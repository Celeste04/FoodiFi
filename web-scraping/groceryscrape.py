from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
hdrs = {'User-Agent': UserAgent().random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}
url = "https://www.realcanadiansuperstore.ca/food/fruits-vegetables/c/28000?navid=flyout-L2-see-all-Fruits-and-Vegetables"
html = requests.get(url,headers=hdrs)
print(html.text)
soup = BeautifulSoup(html.content, 'html.parser')
results = soup.find_all('div')

#costco