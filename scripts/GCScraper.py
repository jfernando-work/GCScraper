import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import random
from fake_useragent import UserAgent
from sqlalchemy import create_engine

titles = []
prices = []
stores = []
conditions = []
image_url = []
listing_url = []
data = []

# categories
url_options = {
    "a": ("All Items", "https://www.guitarcenter.com/Used?recsPerPage=96&page={}"),
    "b": ("Accessories", "https://www.guitarcenter.com/Used/Accessories.gc?facetChangeCategory=Accessories&recsPerPage=96&page={}"),
    "c": ("Amps & Effects", "https://www.guitarcenter.com/Used/Amplifiers-Effects.gc?facetChangeCategory=Amplifiers%20&%20Effects=&recsPerPage=96&page={}"),
    "d": ("Bass", "https://www.guitarcenter.com/Used/Bass.gc?facetChangeCategory=Bass&recsPerPage=96&page={}"),
    "e": ("Books & Sheet Music", "https://www.guitarcenter.com/Used/Books-Sheet-Music-Media.gc?facetChangeCategory=Books,%20Sheet%20Music%20&%20Media&recsPerPage=96&page={}"),
    "f": ("Brass Instruments", "https://www.guitarcenter.com/Used/Brass-Instruments.gc?facetChangeCategory=Brass%20Instruments&recsPerPage=96page={}"),
    "g": ("Concert Percussion", "https://www.guitarcenter.com/Used/Concert-Percussion.gc?facetChangeCategory=Concert%20Percussion&recsPerPage=96&page={}"),
    "h": ("Consumer Electronic", "https://www.guitarcenter.com/Used/Consumer-Electronics.gc?facetChangeCategory=Consumer%20Electronics&recsPerPage=96&page={}"),
    "i": ("Drums & Percussion", "https://www.guitarcenter.com/Used/Drums-Percussion.gc?facetChangeCategory=Drums%20&%20Percussion=&recsPerPage=96&page={}"),
    "j": ("Folk & Traditional Instruments", "https://www.guitarcenter.com/Used/Folk-Traditional-Instruments.gc?facetChangeCategory=Folk%20&%20Traditional%20Instruments=&recsPerPage=96&page={}"),
    "k": ("Guitars", "https://www.guitarcenter.com/Used/Guitars.gc?facetChangeCategory=Guitars&recsPerPage=96&page={}"),
    "l": ("Keyboards & MIDI", "https://www.guitarcenter.com/Used/Keyboards-MIDI.gc?facetChangeCategory=Keyboards%20&%20MIDI=&recsPerPage=96&page={}"),
    "m": ("Marching Band", "https://www.guitarcenter.com/Used/Marching-Band.gc?facetChangeCategory=Marching%20Band&recsPerPage=96&page={}"),
    "n": ("Orchestral Strings", "https://www.guitarcenter.com/Used/Orchestral-Strings.gc?facetChangeCategory=Orchestral%20Strings&recsPerPage=96&page={}"),
    "o": ("Pro Audio", "https://www.guitarcenter.com/Used/Pro-Audio.gc?facetChangeCategory=Pro%20Audio&recsPerPage=96&page={}"),
    "p": ("Woodwinds", "https://www.guitarcenter.com/Used/Woodwinds.gc?facetChangeCategory=Woodwinds&recsPerPage=96&page={}")
}

# menu
print()
print("Select a category to scrape:")
for key, (label, _) in url_options.items():
    print(f"{key}. {label}")

# user selection
print()
selection = input("Enter a letter to select the category: ")
print()

# validate selection
if selection not in url_options:
    print("Invalid choice.")
    exit()

# get selected url
category_name, base_url = url_options[selection]
print(f"Selected: {category_name}")
print()

num_pages = input("Enter the number of pages to scrape: ")
print()

try:
    num_pages = int(num_pages)
except ValueError:
    print("Please enter a valid number.")
    exit()

for page in range(1, num_pages + 1):  
    url = base_url.format(page)
    print(f"Scraping page {page}: {url}")
    
    # create a UserAgent
    ua = UserAgent()

    try:
        user_agent = ua.random
    except:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    
    # pick random user-agent
    headers = {'User-Agent': user_agent}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, features="lxml")


    titles = soup.find_all('h2', class_='jsx-f0e60c587809418b')
    prices = soup.find_all('span', class_='jsx-f0e60c587809418b sale-price font-bold text-[#2d2d2d]')
    stores = soup.find_all('span', class_='jsx-8bbe5b09d939d3ef store-name-text')

    img_tag = soup.find_all('img', class_='w-full h-auto')
    image_url = [img.get('src') for img in img_tag if img.get('src')]

    a_tag = soup.find_all('a', title='product img')
    listing_url = ['https://www.guitarcenter.com' + a.get('href') for a in a_tag if a.get('href')]

    conditions_raw = soup.find_all('p', class_='jsx-8bbe5b09d939d3ef')
    conditions = [
        c.contents[-1].strip()
        for c in conditions_raw
        if c.get_text(strip=True).startswith('Condition:')
    ]

    time.sleep(random.uniform(2, 5)) 

    # check lists to make sure the lengths match
    for i in range(min(len(titles), len(prices), len(stores), len(conditions), len(image_url), len(listing_url))):
        title = titles[i].get_text(strip=True)
        if title.startswith(('Used', 'New', 'Vintage')):
            price = prices[i].get_text(strip=True)
            store = stores[i].get_text(strip=True)
            condition = conditions[i]
            image = image_url[i]
            link = listing_url[i]

            data.append({
                'Title': title,
                'Price': price,
                'Store': store,
                'Condition': condition,
                'Image': image,
                'Link': link
            })

df = pd.DataFrame(data)

engine = create_engine("postgresql://neondb_owner:npg_fv1tZsePnuK2@ep-silent-pond-a5fqrhcs-pooler.us-east-2.aws.neon.tech/gc_items?sslmode=require")

#filename = f"../output/gc_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
#df.to_csv(filename, index=False)

df.to_sql('listings', engine, if_exists='replace', index=False)
