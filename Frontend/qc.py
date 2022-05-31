import streamlit as st
import requests
from web3 import Web3
import json
import datetime 
import pytz #timezone


ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

supplier = "0x201d4f0E4BD39930Aa905B6A2A2803616dCfaA03"
assembler = "0x9c9Cc5Fdaf14e3D3Dcdb0E640448ddEBBF686720"
inventory = "0x04750f8664c32208CC80C4c60bDD2871467c7dc5"
qualityControl = "0xDd7dB8434f218e62fb3c6DF6C6eeED47121C54f0"

def app():
    address = web3.toChecksumAddress("0x21A18D70B596190E153358B2E87CeDF5dF4e3706")
    abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"}],"name":"manufacture","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"}],"name":"newBatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"grade","type":"uint256"},{"indexed":false,"internalType":"string","name":"comment","type":"string"}],"name":"qualityControl","type":"event"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"batchID","type":"uint256"}],"name":"orderNewBatch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"},{"internalType":"uint256","name":"grade","type":"uint256"},{"internalType":"string","name":"comment","type":"string"}],"name":"qualityCheck","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"}],"name":"sendToInventory","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
    contract = web3.eth.contract(address=address,abi=abi)
    
    qc_list = requests.get(url=f"http://localhost:8000/getQualityQueue")
    
    Q=qc_list[0]
    
    

    st.title("Quality Control")
    product_id=st.selectbox("Product ID",options=Q)
    message = st.text_input("Comment")
    grade=st.text_input("Grade(1/0)")

    button1=st.button("Certify")
    if button1:
        web3.eth.defaultAccount=web3.eth.accounts[2]
        timestamp = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        
        product_id=int(product_id)#input from dropbox
        tx=web3.toHex(contract.functions.qualityCheck(str(timestamp),  product_id, int(grade), str(message)).transact())
        
        requests.post(url=f"http://localhost:8000/qualityControl?product_id={product_id}&tx={tx}&message={message}&grade={grade}")

        st.success(f"Certified Product ID:{product_id} at {timestamp}")
        st.success(f"Transaction Hash: {tx}")
