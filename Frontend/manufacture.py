import streamlit as st
import requests
from web3 import Web3
import json
import datetime 
import pytz #timezone

import sys
sys.path.append('/home/shubhdhebar/Documents/Blockchain/Automobile Supply Chain Management/')

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
status=web3.isConnected()

supplier = "0x201d4f0E4BD39930Aa905B6A2A2803616dCfaA03"
assembler = "0x9c9Cc5Fdaf14e3D3Dcdb0E640448ddEBBF686720"
inventory = "0x04750f8664c32208CC80C4c60bDD2871467c7dc5"

    
def app():
    st.title("Assembly Unit")
    st.write("web3 Connection Status:",str(status))
    button1=st.button("Assemble New Unit")

    if button1:
        web3.eth.defaultAccount=web3.eth.accounts[1]#address of assembler

        #Smart Contract for manufacturing new product
        address = web3.toChecksumAddress("0x41BC77FD0106104DB2371bBa7044F5D51759ADe8")
        abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"address","name":"assembler","type":"address"},{"indexed":false,"internalType":"address","name":"inventory","type":"address"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"}],"name":"manufacture","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"address","name":"supplier","type":"address"},{"indexed":false,"internalType":"address","name":"assembler","type":"address"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"}],"name":"newBatch","type":"event"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"address","name":"supplier","type":"address"},{"internalType":"address","name":"assembler","type":"address"},{"internalType":"uint256","name":"batchID","type":"uint256"}],"name":"orderNewBatch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"address","name":"assembler","type":"address"},{"internalType":"address","name":"inventory","type":"address"},{"internalType":"uint256","name":"product_id","type":"uint256"},{"internalType":"address","name":"supplier","type":"address"}],"name":"sendToInventory","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
        contract = web3.eth.contract(address=address,abi=abi)
        pid=0
        filter=contract.events.manufacture.createFilter(fromBlock=65,toBlock='latest')
        
        entry = filter.get_all_entries()
        getProduct=entry.pop()
        pid=getProduct['args']['product_id']
        batch_id=getProduct['args']['batch_id']
        pid=pid+1

        timestamp = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        tx=web3.toHex(contract.functions.sendToInventory(str(timestamp), assembler,inventory,pid,supplier).transact())
        
        #Check if newBatch was called
        filter=contract.events.newBatch.createFilter(fromBlock='latest')
        for entry in filter.get_all_entries():
            if entry['args']['timestamp'] == str(timestamp):
                batch_id=int(entry['args']['batch_id'])
                timestamp=str(timestamp)
                tx=str(web3.toHex(entry['transactionHash']))
                requests.post(url=f"http://localhost:8000/insertBatch?batch_id={batch_id}&timestamp={timestamp}&tx={tx}")
        
        filter=contract.events.manufacture.createFilter(fromBlock='latest')
        
        for entry in filter.get_all_entries():
            pid=entry['args']['product_id']
        batch_id=pid//100
        timestamp=str(timestamp)
        requests.post(url=f"http://localhost:8000/assembler?batch_id={batch_id}&product_id={pid}&timestamp={timestamp}&tx={tx}")

        st.write('Product Serial ID:',pid,'Batch:',batch_id,'Transaction ID:',tx,'timestamp:',timestamp)

