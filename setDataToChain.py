from web3 import Web3
import json
import datetime 
import pytz #timezone
import numpy as np

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

web3.eth.defaultAccount=web3.eth.accounts[1]

assembler = "0x9c9Cc5Fdaf14e3D3Dcdb0E640448ddEBBF686720"
pvt_key="7c2790573e92e126d27652a55ee54112dc33accb6b3a206b95f6343ccad4ad07"

inventory = "0x04750f8664c32208CC80C4c60bDD2871467c7dc5"
supplier= "0x201d4f0E4BD39930Aa905B6A2A2803616dCfaA03"


address = web3.toChecksumAddress("0x508239a98b2b7a333d03d1f6522d238b76795E67")
abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"}],"name":"manufacture","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"}],"name":"newBatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"order_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"retailer","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"qty","type":"uint256"}],"name":"newOrder","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"grade","type":"uint256"},{"indexed":false,"internalType":"string","name":"comment","type":"string"}],"name":"qualityControl","type":"event"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"order_id","type":"uint256"},{"internalType":"uint256","name":"retailer","type":"uint256"},{"internalType":"uint256","name":"qty","type":"uint256"}],"name":"generateOrder","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"batchID","type":"uint256"}],"name":"orderNewBatch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"},{"internalType":"uint256","name":"grade","type":"uint256"},{"internalType":"string","name":"comment","type":"string"}],"name":"qualityCheck","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"}],"name":"sendToInventory","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
                   
contract = web3.eth.contract(address=address,abi=abi)
timestamp = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

a=(contract.functions.sendToInventory(str(timestamp), 100100).transact())


