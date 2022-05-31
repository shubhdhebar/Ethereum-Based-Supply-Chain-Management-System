import streamlit as st
import requests 
from web3 import Web3
import json
import datetime 
import pytz #timezone

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
status=web3.isConnected()

def app():
    st.title("Retailer")
    retailer=st.text_input("Retailer ID")
    showStock=st.button('Display Stock')
    stock=[]
    if(showStock):
        stock=requests.get(url=f"http://localhost:8000/getStock?retailer={int(retailer)}").json()
        st.table(stock)

    st.write("Order Automobile Units")
    qty=st.selectbox("Order Quantity",options=[1,2,3,4,5,6])
    orderButton=st.button("Place Order")
    
    if(orderButton):
        web3.eth.defaultAccount=web3.eth.accounts[1]
        prevOrder=requests.get(url=f"http://localhost:8000/getPreviousOrder").json()
        
        order_id=prevOrder+1
        timestamp = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    
        address = web3.toChecksumAddress("0x508239a98b2b7a333d03d1f6522d238b76795E67")
        abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"}],"name":"manufacture","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"}],"name":"newBatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"order_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"retailer","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"qty","type":"uint256"}],"name":"newOrder","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"grade","type":"uint256"},{"indexed":false,"internalType":"string","name":"comment","type":"string"}],"name":"qualityControl","type":"event"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"order_id","type":"uint256"},{"internalType":"uint256","name":"retailer","type":"uint256"},{"internalType":"uint256","name":"qty","type":"uint256"}],"name":"generateOrder","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"batchID","type":"uint256"}],"name":"orderNewBatch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"},{"internalType":"uint256","name":"grade","type":"uint256"},{"internalType":"string","name":"comment","type":"string"}],"name":"qualityCheck","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"}],"name":"sendToInventory","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
        contract = web3.eth.contract(address=address,abi=abi)

        tx=web3.toHex(contract.functions.generateOrder(str(timestamp),  order_id, int(retailer), qty).transact())

        requests.post(url=f"http://localhost:8000/addOrder?order_id={order_id}&retailer={retailer}&qty={qty}&timestamp={str(timestamp)}&tx={tx}")

        st.success("Order placed successfuly.")
        st.write('Order ID:',order_id)
        st.write('tx:',tx)


        


