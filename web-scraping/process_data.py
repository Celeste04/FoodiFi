import os
import pandas as pd
import re
from nltk.tokenize import wordpunct_tokenize
from string import punctuation
from nltk.corpus import stopwords

PUNCT = list(punctuation)
SW = stopwords.words("english")

f = open('food.txt', 'r')
fw = f.read().split('\n')
print(len(fw))

directory = os.fsencode("scraped-data")
# print(directory)
all_data = pd.DataFrame(columns=['Product Name', 'Product Price', 'Keywords'])

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv") and filename.startswith("walmart"): 
        print(filename)
    else:
        continue
    df = pd.read_csv('scraped-data/'+filename)
    df = df.astype({'Product Name' : 'string', 'Product Price' : 'string'})
    keywords = []

    for i in range(len(df['Product Name'])):
        # convert prices from strings into floats, removes dollar or cents sign
        name, price = df.iloc[i]
        if '$' in price:
            price = re.sub('[^0-9.]', "", price)
        elif '¢' in price:
            cents = int(re.sub(r'\D', "", price))
            price = str(cents/100)
        df.iloc[i,1] = price
        # grab keywords in product name
        kw = ""
        words = wordpunct_tokenize(name)
        for w in words:
            w_lower = w.lower()
            if w_lower in fw and (w_lower + "_") not in kw:
                kw += w_lower + "_"
        keywords.append(kw)
    # print(keywords)
    df = df.assign(Keywords=keywords)
    all_data = pd.concat([df, all_data], ignore_index=True)

# print(all_data)
all_data.to_csv("store-data/walmart_grocery_prices_keywords.csv", index=False)

            

