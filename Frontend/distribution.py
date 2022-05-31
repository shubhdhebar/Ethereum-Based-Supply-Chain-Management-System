import streamlit as st
import requests
from web3 import Web3
import json
import datetime 
import pytz #timezone


ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

def app():
    address = web3.toChecksumAddress("0x9C2509bba6d2C3e3Dc9Afd4EFd175989177f5982")
    abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"order_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"retailer","type":"uint256"}],"name":"dispatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"}],"name":"manufacture","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"}],"name":"newBatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"order_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"retailer","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"qty","type":"uint256"}],"name":"newOrder","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"grade","type":"uint256"},{"indexed":false,"internalType":"string","name":"comment","type":"string"}],"name":"qualityControl","type":"event"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"},{"internalType":"uint256","name":"order_id","type":"uint256"},{"internalType":"uint256","name":"retailer","type":"uint256"}],"name":"assignRetailer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"order_id","type":"uint256"},{"internalType":"uint256","name":"retailer","type":"uint256"},{"internalType":"uint256","name":"qty","type":"uint256"}],"name":"generateOrder","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"batchID","type":"uint256"}],"name":"orderNewBatch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"},{"internalType":"uint256","name":"grade","type":"uint256"},{"internalType":"string","name":"comment","type":"string"}],"name":"qualityCheck","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"}],"name":"sendToInventory","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
    contract = web3.eth.contract(address=address,abi=abi)
    
    st.title("Distribution")
    
    rem_order = requests.get(url=f"http://localhost:8000/remainingOrders").json()
    available_units = requests.get(url=f"http://localhost:8000/availableUnits").json()
    st.write("Units available in Inventory after Quality Check:",len(available_units))
    st.write("Orders recieved from retailers:")
    st.table(rem_order)
    st.write("col0: Order Id, col1: Retailer Id, col2: Remaining Order")

    #Orders will be fulfilled on first-come-first-serve basis

    dispatchButton=st.button("Auto Fulfil Orders")
    n=len(available_units) #units remaining in inventory

    if(dispatchButton):
        web3.eth.defaultAccount=web3.eth.accounts[3]
        for row in rem_order:
            timestamp = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            req=row[2]
            while req>0:
                product_id=available_units[n-1][0]
                tx=web3.toHex(contract.functions.assignRetailer(str(timestamp),  product_id, row[0], row[1]).transact())
                requests.post(url=f"http://localhost:8000/dispatch?product_id={product_id}&order_id={row[0]}&retailer={row[1]}&tx={tx}")
                n=n-1
                req=req-1
                if n==0:
                    break
            if n==0:
                break

