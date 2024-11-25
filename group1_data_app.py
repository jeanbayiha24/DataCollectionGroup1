import streamlit as st
import pandas as pd

st.markdown("<h1 style='text-align: center; color: black;'>GROUP 1 DATA APP</h1>", unsafe_allow_html=True)

st.markdown("""
This app performs webscraping of data from dakar-auto over multiples pages. And we can also download scraped data from the app directly without scraping them.

* **Python libraries:** base64, pandas, streamlit, requests, bs4
* **Data source:** [Expat-Dakar-ordinateurs](https://www.expat-dakar.com/ordinateurs) — [Expat-Dakar-telephones](https://www.expat-dakar.com/telephones) - [Expat-Dakar-cinema](https://www.expat-dakar.com/tv-home-cinema).
""")
