import streamlit as st
import requests 
import json


def app():
    st.title("Track Product")
    product=st.text_input("Enter Product ID")
    
    
    button1=st.button("Check")

    if button1:
        result=requests.get(url=f"http://localhost:8000/track?product_id={product}").json()
        st.json(result)