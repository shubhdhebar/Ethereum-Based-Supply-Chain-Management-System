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
qualityControl = "0xDd7dB8434f218e62fb3c6DF6C6eeED47121C54f0"
    
def app():
    st.title("Assembly Unit")
    st.write("web3 Connection Status:",str(status))
    button1=st.button("Assemble New Unit")

    if button1:
        web3.eth.defaultAccount=web3.eth.accounts[1]#address of assembler

        #Smart Contract for manufacturing new product
        address = web3.toChecksumAddress("0x21A18D70B596190E153358B2E87CeDF5dF4e3706")
        abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"}],"name":"manufacture","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"}],"name":"newBatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"grade","type":"uint256"},{"indexed":false,"internalType":"string","name":"comment","type":"string"}],"name":"qualityControl","type":"event"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"batchID","type":"uint256"}],"name":"orderNewBatch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"},{"internalType":"uint256","name":"grade","type":"uint256"},{"internalType":"string","name":"comment","type":"string"}],"name":"qualityCheck","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"}],"name":"sendToInventory","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
        contract = web3.eth.contract(address=address,abi=abi)
        
        lastProduct=requests.get(url=f"http://localhost:8000/getPrevProduct")
        batch_id=lastProduct//100

        timestamp = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        tx=web3.toHex(contract.functions.sendToInventory(str(timestamp), lastProduct).transact())
        
        #Check if newBatch was called
        blockNum=web3.eth.get_block_number()
        filter=contract.events.supplyChainEvent.createFilter(fromBlock=blockNum-1)
        entry = filter.get_all_entries()
        if entry[0]['args']['processID'] == 0:
            batch_id=int(entry[0]['args']['batch_id'])
            timestamp=str(timestamp)
            tx=str(web3.toHex(entry['transactionHash']))
            requests.post(url=f"http://localhost:8000/insertBatch?batch_id={batch_id}&timestamp={timestamp}&tx={tx}")
        
        filter=contract.events.supplyChainEvent.createFilter(fromBlock='latest')
        entry = filter.get_all_entries()
        pid=entry[0]['args']['product_id']
        batch_id=pid//100
        timestamp=str(timestamp)
        requests.post(url=f"http://localhost:8000/assembler?batch_id={batch_id}&product_id={pid}&timestamp={timestamp}&tx={tx}")

        st.write('Product Serial ID:',pid,'Batch:',batch_id,'Transaction ID:',tx,'timestamp:',timestamp)

