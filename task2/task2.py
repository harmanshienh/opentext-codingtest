from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

driver = webdriver.Chrome()

url = 'https://www.microfocus.com/en-us/products?trial=true'
driver.get(url)
#Allow for content to load
time.sleep(5)
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

products = []

#Parent div containing all cards
cards = soup.find('div', class_ = "products-grid")

if cards:
    #Instantiate list of all cards to be iterated over
    product_cards = cards.find_all('div', class_='uk-card')
    for card in product_cards:
        trial_demo_url = None
        support_link_url = None
        community_link_url = None

        #Store product name
        product_name = card.find('h3').get_text().strip()
        
        starting_letter = product_name[0]
        
        #Extract the description
        description_div = card.find('div', class_='description')
        description = description_div.find('p').get_text().strip()

        #Check for CTA section and extract the first link in that section
        #This is assuming only one of the two possible links should be extracted
        cta_section = card.find('div', class_='cta-section')
        #Some buttons had other tags relating to margin
        #Use lambda function to select all link tags whose classnames contain the given strings
        trial_demo = cta_section.find_all(lambda tag: tag.name == 'a' and 
                                    'uk-button' in tag.get('class', []) and 
                                    'uk-button-primary' in tag.get('class', []))
        
        #Store the first link since some cards have both
        if trial_demo and 'href' in trial_demo[0].attrs:
            trial_demo_url = trial_demo[0]['href']

        footer = card.find('div', class_='footer')
        
        #Check for the "Support" link and extract the href
        support_link = footer.find('a', class_='uk-link uk-text-bold', text="Support")
        if support_link and 'href' in support_link.attrs:
            support_link_url = support_link['href']

        #Check for the "Community" link and extract the href
        community_link = footer.find('a', class_='uk-link uk-text-bold', text="Community")
        if community_link and 'href' in community_link.attrs:
            community_link_url = community_link['href']

        products.append({
            'Product Name': product_name,
            'Starting Letter': starting_letter,
            'Description': description,
            'Free Trial / Demo Request URL': trial_demo_url,
            'Support Link URL': support_link_url,
            'Community Link URL': community_link_url 
        })

products_json = json.dumps(products, indent=4)

with open('products.json', 'w', encoding='utf-8') as file:
    file.write(products_json)