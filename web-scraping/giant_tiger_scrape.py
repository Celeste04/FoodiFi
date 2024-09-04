from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import time
import scraping_vars 
import requests
import json

user_agent = UserAgent().random

# edit with the path to your chrome driver
chromedriver_path = './chromedriver.exe'
# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')


service = Service(executable_path=chromedriver_path)

# Path to your chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)


# emulating geolocation - currently set to Mississauga
# note that Giant Tiger is only found in Ontario
location = {
    "latitude": 43.593878,
    "longitude": -79.646979,
    "accuracy":100,
}

driver.execute_cdp_cmd("Page.setGeolocationOverride", location)

# grocery urls
URL_PART_1 = "https://www.gianttiger.com/search?q="
URL_PART_2 = "&store_inventory=bopis&online_inventory=sth"
PAGE_URL = "&p="

# in case we are differentiating by weight and package size
AMT_RELATED_WORDS = {'pk', 'pack', 'g', 'ml'}


def save_prev_scraped():
    with open('prev_scraped.json', 'w') as f:
        json.dump(scraping_vars.prev_scraped, f)

def load_prev_scraped():
    try:
        with open('prev_scraped.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

scraping_vars.prev_scraped = load_prev_scraped()

# Generates a random proxy from the valid proxy list
# Note: random proxy list may have to be regenerated from time to time
def random_proxy():
    for _ in range(30):  # Retry up to 30 times
        proxy = random.choice(scraping_vars.valid_proxies)
        try:
            res = requests.get("http://ipinfo.io/json", proxies={"http": proxy, "https": proxy}, timeout=5)
            if res.status_code == 200:
                return proxy
        except requests.RequestException as e:
            print(f"Proxy {proxy} failed: {e}")
    return None

print("PREV SCRAPED")
print(scraping_vars.prev_scraped)
print("----------")

# returns a dictionary of items and prices
def retrieve_items_and_prices(item_name):
    # if search has already been made before
    if item_name in scraping_vars.prev_scraped:
        return scraping_vars.prev_scraped[item_name]
    
    # initialize an item in the dictionary if not found before
    scraping_vars.prev_scraped[item_name] = []
    while True:
        # using a random proxy each time
        '''
        proxy = random_proxy()
        if proxy:
            chrome_options.add_argument(f'--proxy-server={proxy}')
        '''
        page_num = 1

        # the url we will be searching for 
        search_url = URL_PART_1+item_name+URL_PART_2+PAGE_URL+str(page_num)
        # first page has a different url layout
        if (page_num == 1):
            search_url = URL_PART_1+item_name+URL_PART_2

        driver.get(search_url)

        # Let the page load completely
        driver.implicitly_wait(15)  # Wait for up to 10 seconds for elements to load

        # Get the page source after JS has executed
        page_source = driver.page_source

        # Now parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        product_titles = soup.find_all('h2', class_='product-tile__title body-bold-sm')
        product_prices = soup.find_all('span', class_='price__value')

        print("finished parsing with soup")

        # no more items on the page
        if (len(product_titles)) == 0:
            break
    
        # Print each product tile
        for i in range(len(product_titles)):
            scraping_vars.prev_scraped[item_name].append((product_titles[i].get_text(),product_prices[i].get_text()))
        page_num+=1
        time.sleep(5)
    save_prev_scraped()
    print(scraping_vars.prev_scraped)
    return scraping_vars.prev_scraped[item_name]

retrieve_items_and_prices("mayo")
retrieve_items_and_prices("cucumber")
driver.quit()

