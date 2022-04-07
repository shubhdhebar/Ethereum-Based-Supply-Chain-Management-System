from web3 import Web3
import json
import datetime 
import pytz #timezone
import dbQueries

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

from fastapi import FastAPI
import uvicorn
from typing import Optional
from pydantic import BaseModel


app=FastAPI()

supplier = "0x201d4f0E4BD39930Aa905B6A2A2803616dCfaA03"
assembler = "0x9c9Cc5Fdaf14e3D3Dcdb0E640448ddEBBF686720"
inventory = "0x04750f8664c32208CC80C4c60bDD2871467c7dc5"
pid=0

@app.post("/assembler/manufacture")
def assemble():
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
    batch_id=entry[-1]['args']['batch_id']
    pid=pid+1

    timestamp = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    tx=web3.toHex(contract.functions.sendToInventory(str(timestamp), assembler,inventory,pid,supplier).transact())
    
    #Check if newBatch was called
    filter=contract.events.newBatch.createFilter(fromBlock='latest')
    for entry in filter.get_all_entries():
        if entry['args']['timestamp'] == str(timestamp):
            dbQueries.addBatch(int(entry['args']['batch_id']),str(timestamp),str(web3.toHex(entry['transactionHash'])))
    
    filter=contract.events.manufacture.createFilter(fromBlock='latest')
    
    for entry in filter.get_all_entries():
        pid=entry['args']['product_id']
        batch_id=entry['args']['batch_id']
    
    dbQueries.addProduct(pid//100,pid,timestamp,tx)
    return {'Product Serial ID':pid,'Batch':batch_id,'Transaction ID':tx,'timestamp':timestamp}

@app.post("/qualityControl")
def checkQuality(product_id,officer_name,message,grade):
    web3.eth.defaultAccount=web3.eth.accounts[2]

    timestamp = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

    address = web3.toChecksumAddress("0xf2DC6E048737956f0adE6675b3fd5A232Db1591e")
    abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"},{"indexed":false,"internalType":"string","name":"officer","type":"string"},{"indexed":false,"internalType":"string","name":"message","type":"string"},{"indexed":false,"internalType":"uint256","name":"grade","type":"uint256"}],"name":"qualityControl","type":"event"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"},{"internalType":"string","name":"officer","type":"string"},{"internalType":"string","name":"message","type":"string"},{"internalType":"uint256","name":"grade","type":"uint256"}],"name":"qualityCheck","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
    contract = web3.eth.contract(address=address,abi=abi)
    
    tx=web3.toHex(contract.functions.qualityCheck(str(timestamp), int(product_id), str(officer_name),str(message),int(grade)).transact())
    dbQueries.addQC(product_id,str(timestamp),tx,officer_name,message,grade)
    return {product_id:message,'Grade':grade}

@app.get("/track")
def trackProduct(product_id):
    data=dbQueries.fetchProduct(product_id)
    return {
        'ProductID':data[0],
        'BatchID':data[8],
        'Product Assembled on':data[1],
        'Transaction hash for assembly':data[2],
        'Quality assessment done on':data[3],
        'Quality assessment done by':data[5],
        'Grade assigned':data[7],
        'Comment(s) by Quality Control':data[6],
        'Transaction hash for Quality Control':data[4]
    }

    
    
    






    








