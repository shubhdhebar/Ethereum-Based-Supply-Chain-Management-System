from web3 import Web3
import json

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

address = web3.toChecksumAddress("0xF824df33762D06243A34e6724629E6c4393E593b")
abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"process_id","type":"uint256"},{"indexed":false,"internalType":"address","name":"assembler","type":"address"},{"indexed":false,"internalType":"address","name":"inventory","type":"address"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"}],"name":"manufacture","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"process_id","type":"uint256"},{"indexed":false,"internalType":"address","name":"supplier","type":"address"},{"indexed":false,"internalType":"address","name":"assembler","type":"address"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"}],"name":"newBatch","type":"event"},{"constant":false,"inputs":[{"internalType":"address","name":"supplier","type":"address"},{"internalType":"address","name":"assembler","type":"address"},{"internalType":"uint256","name":"batchID","type":"uint256"}],"name":"orderNewBatch","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"assembler","type":"address"},{"internalType":"address","name":"inventory","type":"address"},{"internalType":"uint256","name":"product_id","type":"uint256"},{"internalType":"address","name":"supplier","type":"address"}],"name":"sendToInventory","outputs":[],"payable":true,"stateMutability":"payable","type":"function"}]')
    

contract = web3.eth.contract(address=address,abi=abi)

filter=contract.events.manufacture.createFilter(fromBlock='latest')
for event in filter.get_all_entries():
    print(event['args']['product_id'])
    

