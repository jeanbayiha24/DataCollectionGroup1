# import packages
from bs4 import BeautifulSoup as bs
from requests import get
#from selenium import webdriver 
#from selenium.webdriver.common.by import By 
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.service import Service
import streamlit as st
import pandas as pd


st.markdown("<h1 style='text-align: center; color: black;'>GROUP 1 DATA APP</h1>", unsafe_allow_html=True)

st.markdown("""
This app performs webscraping of data from dakar-auto over multiples pages. And we can also download scraped data from the app directly without scraping them.

* **Python libraries:** base64, pandas, streamlit, requests, bs4
* **Data source:** [Expat-Dakar-ordinateurs](https://www.expat-dakar.com/ordinateurs) — [Expat-Dakar-telephones](https://www.expat-dakar.com/telephones) - [Expat-Dakar-cinema](https://www.expat-dakar.com/tv-home-cinema).
""")






def scrape_all_bs(pages_nb, link):
    # Generalize the scraping over all pages
    data = []
    
    for page in range(1, pages_nb + 1):
        url = f"{link}?page={page}"
        res = get(url)
        
        soup = bs(res.text, 'html.parser')
            
        # Find all containers for listings
        containers = soup.find_all("div", class_="listing-card__content")
            
        for container in containers:
            try:
                # Extract details
                details = container.find("div", class_="listing-card__header__title").text.strip().replace('\n','')
              
                # Extract price
                price = container.find("span", class_="listing-card__price__value").text.strip()
                    
                # Extract address
                address = container.find("div", class_="listing-card__header__location").text.strip().replace('\n','')
                    
                # Extract tags (brand and condition)
                tags = container.find("div", class_="listing-card__header__tags").find_all("span")
                condition = tags[0].text.strip()
                brand = tags[-1].text.strip()
                    
                # Extract image link
                img = container.find_previous("img", class_="listing-card__image__resource vh-img")
                img_link = img['src']
                    
                # Append extracted data
                data.append({'details': details,
                        'brand': brand,
                        'price': price,
                        'address': address,
                        'condition': condition,
                        'link_image': img_link
                    })
                
            except Exception as e:
                pass  # Skip this container in case of an error
    
    # Convert collected data to a DataFrame
    df = pd.DataFrame(data)
    return df




