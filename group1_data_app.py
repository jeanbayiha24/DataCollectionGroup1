# import packages
from bs4 import BeautifulSoup as bs
from requests import get
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components

st.markdown("<h1 style='text-align: center; color: black;'>GROUP 1 DATA APP</h1>", unsafe_allow_html=True)

st.markdown("""
This app performs webscraping of data from dakar-auto over multiples pages. And we can also download scraped data from the app directly without scraping them.

* **Python libraries:** base64, pandas, streamlit, requests, bs4
* **Data source:** [Expat-Dakar-ordinateurs](https://www.expat-dakar.com/ordinateurs) — [Expat-Dakar-telephones](https://www.expat-dakar.com/telephones) - [Expat-Dakar-cinema](https://www.expat-dakar.com/tv-home-cinema).
""")

st.sidebar.markdown(
    "<h2 style='color: #ffffff; background-color: #5a9; padding: 10px; text-align: center;'>User Input Features</h2>",
    unsafe_allow_html=True,
)

# Add options to the lateral bar
pages_indexes = st.sidebar.selectbox("Pages indexes", list(range(1, 250)), index=2)
options = st.sidebar.selectbox("Options", ["Scrape data using BeautifulSoup","Download scraped data", "Dashboard of the data", "Fill the form"], index=1)

#url of the websites
url_ordis = "https://www.expat-dakar.com/ordinateurs"
url_phones = "https://www.expat-dakar.com/telephones"
url_cinema = "https://www.expat-dakar.com/tv-home-cinema"

st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    
def scrape_all_bs(pages_nb, link):
    # Generalize the scraping over all pages
    data = []
    
    for page in range(1, pages_nb + 1):
        
        url = f"{link}?page={page}"

        proxy_list = [{"http": "http://13.36.87.105:3128", "https": "http://13.36.87.105:3128"},{"http": "http://154.0.12.163:80", "https": "http://154.0.12.163:80"}]

        res = None
        for proxy in proxy_list:
            try:
                res = get(url, proxies=proxy, timeout=5)
                if res.status_code != 200:
                    st.write(f"Erreur sur la page {page}: Code HTTP {res.status_code}")
                    continue
            except Exception as e:
                print(f"Proxy {proxy['http']} failed: {e}")
               
        
        
        soup = bs(res.text, 'html.parser')
            
        # Find all containers for listings
        containers = soup.find_all("div", class_="listing-card__content")

        if not containers:
            st.write(f"Aucun conteneur trouvé sur la page {page}")
            
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
        #time.sleep(2)  # Wait 2 seconds before the next request
    # Convert collected data to a DataFrame
    df = pd.DataFrame(data)
    return df

# Function for loading the data
def load_(dataframe, title, key) :
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title,key):
      
        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
        st.dataframe(dataframe)

#The conditions of the options of the sidebar
if options=="Scrape data using BeautifulSoup":
    if st.button("Computer data"):
        df = scrape_all_bs(pages_indexes, url_ordis)
        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + ' columns.')
        st.dataframe(df)
    
    elif st.button("Telephones data"):
        df = scrape_all_bs(pages_indexes, url_phones)
        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + ' columns.')
        st.dataframe(df)
    
    elif st.button("Cinema data"):
        df = scrape_all_bs(pages_indexes, url_cinema)
        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + ' columns.')
        st.dataframe(df)


# load the data
elif options == "Download scraped data":
    load_(pd.read_csv('data/ordi_expat_dakar.csv'), 'Computers data', '1')
    load_(pd.read_csv('data/phone_expat_dakar.csv'), 'Telephones data', '2')
    load_(pd.read_csv('data/expat_cinema_dakar.csv'), 'Cinema data', '3')
   
elif options == "Dashboard of the data":
    df_ordis = pd.read_csv('data/ordi_expat_dakar.csv')
    df_phones = pd.read_csv('data/phone_expat_dakar.csv')
    df_cinema= pd.read_csv('data/expat_cinema_dakar.csv')

    df_ordis = df_ordis.drop(['web-scraper-order','web-scraper-start-url'], axis = 1) #We drop the useless columns
    df_ordis['price'] = pd.to_numeric(df_ordis['price'].str.replace('F Cfa', '', regex=False).str.replace(' ', ''),  errors='coerce')#We clean the 'price' column

    avg_prices_by_brand = df_ordis.groupby('brand')['price'].mean().dropna()

    plot1 = plt.figure(figsize=(11, 7))
    avg_prices_by_brand.plot(kind='bar', color=(0.2, 0.4, 0.2, 0.6))
    plt.title('Average price per brand', fontsize=14)
    plt.xlabel('Brands', fontsize=12)
    plt.ylabel('Average prices (FCFA)', fontsize=12)
    plt.xticks(rotation=45, ha='right')#Rotate the names of the bars
    st.pyplot(plot1)

    st.dataframe(avg_prices_by_brand)

else:
    components.html("""
    <iframe src="https://ee.kobotoolbox.org/i/QSMp2YGW" width="800" height="600"></iframe>
    """,height=1100,width=800)

    
    

    
    






