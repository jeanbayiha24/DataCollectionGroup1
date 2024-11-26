# import packages
#from bs4 import BeautifulSoup as bs
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
import streamlit as st
import pandas as pd


st.markdown("<h1 style='text-align: center; color: black;'>GROUP 1 DATA APP</h1>", unsafe_allow_html=True)

st.markdown("""
This app performs webscraping of data from dakar-auto over multiples pages. And we can also download scraped data from the app directly without scraping them.

* **Python libraries:** base64, pandas, streamlit, requests, bs4
* **Data source:** [Expat-Dakar-ordinateurs](https://www.expat-dakar.com/ordinateurs) — [Expat-Dakar-telephones](https://www.expat-dakar.com/telephones) - [Expat-Dakar-cinema](https://www.expat-dakar.com/tv-home-cinema).
""")



#Function for scraping data
# instantiate a Chrome options object
options = webdriver.ChromeOptions() 
# set the options to use Chrome in headless mode (used for running the script in the background)
options.add_argument("--headless=new") 
# initialize an instance of the Chrome driver (browser) in headless mode
driver = webdriver.Chrome(ChromeDriverManager().install())

def scrape_all(pages_nb, link):
    # generalize the scraping over all containers
    data = []
    df1 = pd.DataFrame()
    for page in range(1,pages_nb+1):
        url = link+f'?page={page}' 
        driver.get(url)
        # find containers
        containers = driver.find_elements(By.CSS_SELECTOR, "[class= 'listing-card__content 1']")
        images = driver.find_elements(By.CSS_SELECTOR, "[class='listing-card__image__resource vh-img']")
        page_data = []  # Temporary list to hold data for the current page
        for container, img in zip(containers, images) :
            try:
                # get the details
                details = container.find_element(By.CSS_SELECTOR, "[class='listing-card__header__title']").text
                # get the price
                price = container.find_element(By.CSS_SELECTOR, "[class='listing-card__price__value 1']").text#.replace('GH₵ ', '').replace(',','')
                # get the location
                address = container.find_element(By.CSS_SELECTOR, "[class='listing-card__header__location']").text
                tags = container.find_element(By.CSS_SELECTOR, "[class='listing-card__header__tags']")
                brand = tags.find_elements(By.TAG_NAME, "span")[1].text
                # get the condition
                condition = tags.find_elements(By.TAG_NAME, "span")[0].text
                img_link = img.get_attribute('src')
                page_data.append({'details':details, 'brand':brand, 'price':price, 'address':address, 'condition': condition, 'link_image':img_link})
            except Exception as e:
                print(f"Error scraping a container: {e}")
                continue  # Skip this container in case of an error
        # Add current page data to the main list
        data.extend(page_data)
    df1 = pd.DataFrame(data)
    
    return df1



