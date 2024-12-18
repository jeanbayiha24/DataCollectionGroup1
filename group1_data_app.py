# import packages
from bs4 import BeautifulSoup as bs
import random
import base64
from requests import get
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components
from urllib.parse import quote
import time


st.markdown("<h1 style='text-align: center; color: black;'>GROUP 1 DATA APP</h1>", unsafe_allow_html=True)

st.markdown("""
This app performs webscraping of data from expat-dakar over multiples pages. And we can also download scraped data from the app directly without scraping them.

* **Python libraries:** base64, pandas, streamlit, requests, bs4, matplotlib
* **Data source:** [Expat-Dakar-ordinateurs](https://www.expat-dakar.com/ordinateurs) - [Expat-Dakar-telephones](https://www.expat-dakar.com/telephones) - [Expat-Dakar-cinema](https://www.expat-dakar.com/tv-home-cinema).
""")
col1, col2, col3, col4 = st.columns([5, 5, 5, 5])

with col1:
    st.image('images/expat_dakar_logo.png', width=150)  
with col2:
    st.image('images/computer_image.jpg', width=130)
with col3:
    st.image('images/phones_image.webp', width=100)
with col4:
    st.image('images/tv.jpg', width=100)

st.sidebar.markdown(
    """<h2 style='color: #0e0f10; background-color: #87CEEB; padding: 10px; text-align: center; border-radius: 10px;'>User Input Features</h2>
    <style>.stSelectbox > label { 
        color: #0e0f10; 
    }
    </style>""",
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

# Background function
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

#We tried to use a proxy server to enter in the expat-dakar website but it failed
#proxies = {
#    "http": "http://D4MgFT6C9WSP:DB06xRBK1v4s_region-af_ttl-30s_session-ZF2nnrSU8ns4@superproxy.zenrows.com:1337",
#    "https": "https://D4MgFT6C9WSP:DB06xRBK1v4s_region-af_ttl-30s_session-ZDPAx4mVDWIm@superproxy.zenrows.com:1338"
#}

# Web scraping of Vehicles data on expat-dakar
@st.cache_data(show_spinner=False, persist=True)
def scrape_all_bs(pages_nb, link):
    # Generalize the scraping over all pages
    data = []
    
    for page in range(1, pages_nb + 1):
        
        url = f"{link}?page={page}"

        #proxy = "http://7153b3ea86ef620b6b9b6f6b9271028a928e475b:premium_proxy=true@api.zenrows.com:8001"
        #proxies = {"http": proxy, "https": proxy}
        
        
        res = get(url, verify=False)
        if res.status_code != 200:
            st.write(f"Error on the page {page}: Code HTTP {res.status_code}")
            continue
        
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
        time.sleep(2)  # Wait 2 seconds before the next request
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
    
add_bg_from_local('images/pngtree-technology-data.jpg')

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

    st.markdown("<h3 style='text-align: center; color: black;'>Computers plots</h3>", unsafe_allow_html=True)
    #For the computers data
    df_ordis = df_ordis.drop(['web-scraper-order','web-scraper-start-url'], axis = 1) #We drop the useless columns
    df_ordis['price'] = pd.to_numeric(df_ordis['price'].str.replace('F Cfa', '').str.replace('\u202f', ''),  errors='coerce')#We clean the 'price' column
    avg_prices_by_brand = df_ordis.groupby('brand')['price'].mean().dropna()
    plot1 = plt.figure(figsize=(11, 7))
    avg_prices_by_brand.plot(kind='bar', color=(0.2, 0.4, 0.2, 0.6))
    plt.title('Average price of computers per brand', fontsize=14)
    plt.xlabel('Brands', fontsize=12)
    plt.ylabel('Average prices (FCFA)', fontsize=12)
    plt.xticks(rotation=45, ha='right')#Rotate the names of the bars
    st.pyplot(plot1)

    # Verify the importants columns (computer_condition, brand, etc.)
    df_ordis['computer_condition'] = df_ordis['computer_condition'].str.strip()  # clean the spaces
    df_ordis['brand'] = df_ordis['brand'].str.strip()  # clean the spaces
    
    # Drop the NaN values
    df_ordis = df_ordis.dropna(subset=['price', 'brand', 'computer_condition'])  
    plot4 =  plt.figure(figsize=(12, 6))
    sns.boxplot(data=df_ordis, x='computer_condition', y='price', palette='Set2')
    plt.title("Price distribution by computer status")
    plt.xlabel("Status of the computer")
    plt.ylabel("Price (F CFA)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plot4)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: black;'>Telephones plots</h3>", unsafe_allow_html=True)
    #For the Telephones data
    df_phones = df_phones.drop(['web-scraper-order','web-scraper-start-url'], axis = 1) #We drop the useless columns
    df_phones['price'] = pd.to_numeric(df_phones['price'].str.replace('F Cfa', '').str.replace('\u202f', ''),  errors='coerce')#We clean the 'price' column
    avg_prices_by_brand2 = df_phones.groupby('brand')['price'].mean().dropna()
    plot2 = plt.figure(figsize=(11, 7))
    avg_prices_by_brand2.plot(kind='bar', color=(0.2, 0.4, 0.7, 0.6))
    plt.title('Average price of telephones per brand', fontsize=14)
    plt.xlabel('Brands', fontsize=12)
    plt.ylabel('Average prices (FCFA)', fontsize=12)
    plt.xticks(rotation=45, ha='right')#Rotate the names of the bars
    st.pyplot(plot2)

    # We clean the column "phone_condition"
    df_phones['phone_condition'] = df_phones['phone_condition'].str.strip()  
    # We clean the column "brand"
    df_phones['brand'] = df_phones['brand'].str.strip()  # Supprime les espaces
    # We drop the NaN values
    df_phones = df_phones.dropna(subset=['price', 'brand', 'phone_condition']) 

    plot5 = plt.figure(figsize=(10, 6))
    sns.boxplot(data=df_phones, x='phone_condition', y='price', palette='Set2')
    plt.title("Phone prices by state", fontsize=16)
    plt.xlabel("Phone status", fontsize=14)
    plt.ylabel("Price (F CFA)", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plot5)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: black;'>Cinema(TV) plots</h3>", unsafe_allow_html=True)
    #For the Cinema data
    df_cinema = df_cinema.drop(['web-scraper-order','web-scraper-start-url'], axis = 1) #We drop the useless columns
    df_cinema['price'] = pd.to_numeric(df_cinema['price'].str.replace('F Cfa', '').str.replace('\u202f', ''),  errors='coerce')#We clean the 'price' column
    avg_prices_by_brand3 = df_cinema.groupby('brand')['price'].mean().dropna()
    plot3 = plt.figure(figsize=(11, 7))
    avg_prices_by_brand3.plot(kind='bar', color=(0.4, 0.4, 0.7, 0.6))
    plt.title('Average price of TV per brand', fontsize=14)
    plt.xlabel('Brands', fontsize=12)
    plt.ylabel('Average prices (FCFA)', fontsize=12)
    plt.xticks(rotation=45, ha='right')#Rotate the names of the bars
    st.pyplot(plot3)


else:
    components.html("""
    <iframe src="https://ee.kobotoolbox.org/i/QSMp2YGW" width="800" height="600"></iframe>
    """,height=1100,width=800)

    
    

    
    






