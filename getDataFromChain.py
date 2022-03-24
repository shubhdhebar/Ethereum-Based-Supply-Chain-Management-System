from web3 import Web3
import json

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

address=web3.toChecksumAddress("0x4D952851a4b59300ee1A1b83b5B2C74959587505")
abi= json.loads('[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"assembler","type":"address"},{"indexed":false,"internalType":"address","name":"inventory","type":"address"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"},{"indexed":false,"internalType":"string","name":"message","type":"string"}],"name":"manufacture","type":"event"},{"constant":false,"inputs":[{"internalType":"address","name":"assembler","type":"address"},{"internalType":"address","name":"inventory","type":"address"},{"internalType":"uint256","name":"product_id","type":"uint256"},{"internalType":"uint256","name":"batch_id","type":"uint256"}],"name":"sendToInventory","outputs":[],"payable":true,"stateMutability":"payable","type":"function"}]')


contract = web3.eth.contract(address=address,abi=abi)

filter=contract.events.manufacture.createFilter(fromBlock=1)
for event in filter.get_all_entries():
    print(event['args']['product_id']," ",event['args']['message'])
    

