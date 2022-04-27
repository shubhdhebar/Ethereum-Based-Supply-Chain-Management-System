import streamlit as st
import manufacture, qc, track,retailer, distributor

st.sidebar.title("Navigation")
PAGES = {
    "Assembly": manufacture,
    "Quality Control": qc,
    "Track Product":track,
    "Retailer":retailer,
    "Distributor": distributor
}

selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()