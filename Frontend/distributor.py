import streamlit as st
    
def app():
    st.title("Distributor")
    Distributor = st.text_input("Distributor Name")
    event = st.radio(
     "Options",
     ('View Orders', 'Place Order','Present Stock'))
