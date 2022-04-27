import streamlit as st
import requests
from web3 import Web3
import json
import datetime 
import pytz #timezone


ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

def app():
    st.title("Quality Control")
    product_id=st.text_input("Product ID")
    officer_name=st.text_input("Officer Name")
    message = st.text_input("Comment")
    grade=st.text_input("Grade(1/0)")

    button1=st.button("Certify")
    if button1:
        web3.eth.defaultAccount=web3.eth.accounts[2]
        timestamp = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

        address = web3.toChecksumAddress("0xf2DC6E048737956f0adE6675b3fd5A232Db1591e")
        abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"},{"indexed":false,"internalType":"string","name":"officer","type":"string"},{"indexed":false,"internalType":"string","name":"message","type":"string"},{"indexed":false,"internalType":"uint256","name":"grade","type":"uint256"}],"name":"qualityControl","type":"event"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"},{"internalType":"string","name":"officer","type":"string"},{"internalType":"string","name":"message","type":"string"},{"internalType":"uint256","name":"grade","type":"uint256"}],"name":"qualityCheck","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
        contract = web3.eth.contract(address=address,abi=abi)
        
        tx=web3.toHex(contract.functions.qualityCheck(str(timestamp), int(product_id), str(officer_name),str(message),int(grade)).transact())
        
        requests.post(url=f"http://localhost:8000/qualityControl?product_id={product_id}&tx={tx}&officer_name={officer_name}&message={message}&grade={grade}")

        st.success(f"Certified Product ID:{product_id} at {timestamp}")
        st.success(f"Transaction Hash: {tx}")
