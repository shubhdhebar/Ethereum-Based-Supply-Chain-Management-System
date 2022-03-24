from web3 import Web3
import json

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

web3.eth.defaultAccount=web3.eth.accounts[1]

assembler = "0x9c9Cc5Fdaf14e3D3Dcdb0E640448ddEBBF686720"
pvt_key="7c2790573e92e126d27652a55ee54112dc33accb6b3a206b95f6343ccad4ad07"

inventory = "0x04750f8664c32208CC80C4c60bDD2871467c7dc5"

product_id=1002

address=web3.toChecksumAddress("0x4D952851a4b59300ee1A1b83b5B2C74959587505")
abi= json.loads('[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"assembler","type":"address"},{"indexed":false,"internalType":"address","name":"inventory","type":"address"},{"indexed":false,"internalType":"uint256","name":"product_id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"batch_id","type":"uint256"},{"indexed":false,"internalType":"string","name":"message","type":"string"}],"name":"manufacture","type":"event"},{"constant":false,"inputs":[{"internalType":"address","name":"assembler","type":"address"},{"internalType":"address","name":"inventory","type":"address"},{"internalType":"uint256","name":"product_id","type":"uint256"},{"internalType":"uint256","name":"batch_id","type":"uint256"}],"name":"sendToInventory","outputs":[],"payable":true,"stateMutability":"payable","type":"function"}]')

contract = web3.eth.contract(address=address,abi=abi)

a=(contract.functions.sendToInventory(assembler,inventory,product_id,1).transact())


