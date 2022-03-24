from web3 import Web3
import json

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

from fastapi import FastAPI
import uvicorn
from typing import Optional
from pydantic import BaseModel
import pymongo

import dbTransactions

app=FastAPI()


@app.post("/supplier/sendParts")
def sendParts():
    web3.eth.defaultAccount=web3.eth.accounts[0]
    abi = json.loads('[{"constant":true,"inputs":[{"internalType":"uint256","name":"prevBatchID","type":"uint256"}],"name":"sendNewBatch","outputs":[{"internalType":"uint256","name":"newBatchID","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]')
    address=web3.toChecksumAddress("0x28Dc729E17dEB0cF442B2Cf1AC7A6f3836aD6117")
    contract = web3.eth.contract(address=address,abi=abi)
    prevID=dbTransactions.getPrevBatchID()
    id=contract.functions.sendNewBatch(prevID).call()
    tx_hash=web3.toHex(contract.functions.sendNewBatch(1000).transact())
    dbTransactions.newBatch(id,tx_hash)








