import streamlit as st


def app():
    st.title("Retailer")
    retailer = st.text_input("Retailer ID")
    option = st.selectbox(
        'Distributor Name', ('D1', 'D2', 'D3'))
        
    st.write('You selected:', option)

    button1 = st.button("Order")

    # if button1:
    #     result = requests.get(
    #         url=f"http://localhost:8000/track?product_id={product}").json()
    #     st.json(result)
