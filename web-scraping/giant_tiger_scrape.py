from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

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

AMT_RELATED_WORDS = {'pk', 'pack', 'g', 'ml'}

def retrieve_items_and_prices(item_name):
    while True:
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

        product_titles = soup.find_all('h2', {'class':'product-tile__title body-bold-sm'})
        product_prices = soup.find_all('span', {'class':'price__value'})

        # no more items on the page
        if (len(product_titles)) == 0:
            break
    
        # Print each product tile
        for product_title in product_titles:
            print(product_title)
    
        page_num+=1

# tests
search_url = "https://www.gianttiger.com/search?q=apple&store_inventory=bopis&online_inventory=sth&p=2"
driver.get(search_url)

# Let the page load completely
driver.implicitly_wait(15)  # Wait for up to 10 seconds for elements to load

# Get the page source after JS has executed
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
product_titles = soup.find_all('h2', class_='product-tile__title body-bold-sm')
print("printing titles")
for product_title in product_titles:
    print(product_title)
print("end-------")
driver.quit()

