import streamlit as st
import manufacture, qc, track,retailer,distribution
 
st.sidebar.title("Navigation")
PAGES = {
    "Assembly": manufacture,
    "Quality Control": qc,
    "Distribution": distribution,
    "Retailer":retailer,
    "Track Product":track
    
}

selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()