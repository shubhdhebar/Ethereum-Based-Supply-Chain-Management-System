import streamlit as st
import manufacture, qc, track,retailer, distributor

st.sidebar.title("Navigation")
PAGES = {
    "Assembly": manufacture,
    "Quality Control": qc,
    "Distributor": distributor,
    "Retailer":retailer,
    "Track Product":track
    
}

selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()