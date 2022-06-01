import streamlit as st
from web3 import Web3
import requests 
import json


ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

def app():
    st.title("Track Product")
    product=st.text_input("Enter Product ID")
    
    
    button1=st.button("Check")

    if button1:
        result=requests.get(url=f"http://localhost:8000/track?product_id={product}").json()
        st.json(result)

    
    
    