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

    tx=st.text_input("Enter Transaction Hash")
    button2=st.button("Generate Transaction Reciept")

    if button2:
        transaction=web3.eth.get_transaction(tx)
        blockNumber=transaction['blockNumber']

        address = web3.toChecksumAddress("0x9C2509bba6d2C3e3Dc9Afd4EFd175989177f5982")
        abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"order_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"retailer","type":"uint256"}],"name":"dispatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"}],"name":"manufacture","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"}],"name":"newBatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"order_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"retailer","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"qty","type":"uint256"}],"name":"newOrder","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"grade","type":"uint256"},{"indexed":false,"internalType":"string","name":"comment","type":"string"}],"name":"qualityControl","type":"event"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"},{"internalType":"uint256","name":"order_id","type":"uint256"},{"internalType":"uint256","name":"retailer","type":"uint256"}],"name":"assignRetailer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"order_id","type":"uint256"},{"internalType":"uint256","name":"retailer","type":"uint256"},{"internalType":"uint256","name":"qty","type":"uint256"}],"name":"generateOrder","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"batchID","type":"uint256"}],"name":"orderNewBatch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"},{"internalType":"uint256","name":"grade","type":"uint256"},{"internalType":"string","name":"comment","type":"string"}],"name":"qualityCheck","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"}],"name":"sendToInventory","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
        contract = web3.eth.contract(address=address,abi=abi)

        filter=contract.events.supplyChainEvent.createFilter(fromBlock=blockNumber,toBlock=blockNumber+1)
        entry = filter.get_all_entries()
        outputReciept=[tx,f"ProccessID: {entry[0]['args']['processID']}",f"Timestamp: {entry[0]['args']['timestamp']}",f"Product ID:{entry[0]['args']['product_id']}"]
        st.write(outputReciept)