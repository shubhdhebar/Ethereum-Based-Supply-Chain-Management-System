from web3 import Web3
import json

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

address = web3.toChecksumAddress("0x21A18D70B596190E153358B2E87CeDF5dF4e3706")
abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"}],"name":"manufacture","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"}],"name":"newBatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"timestamp","type":"string"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"grade","type":"uint256"},{"indexed":false,"internalType":"string","name":"comment","type":"string"}],"name":"qualityControl","type":"event"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"batchID","type":"uint256"}],"name":"orderNewBatch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"},{"internalType":"uint256","name":"grade","type":"uint256"},{"internalType":"string","name":"comment","type":"string"}],"name":"qualityCheck","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"timestamp","type":"string"},{"internalType":"uint256","name":"product_id","type":"uint256"}],"name":"sendToInventory","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
        
contract = web3.eth.contract(address=address,abi=abi)

filter=contract.events.manufacture.createFilter(fromBlock='latest')
entry = filter.get_all_entries()
print(entry)


