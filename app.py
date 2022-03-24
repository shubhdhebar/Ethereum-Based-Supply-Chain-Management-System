from web3 import Web3
import json

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

web3.eth.defaultAccount=web3.eth.accounts[0]

abi = json.loads('[{"constant":true,"inputs":[{"internalType":"uint256","name":"prevBatchID","type":"uint256"}],"name":"sendNewBatch","outputs":[{"internalType":"uint256","name":"newBatchID","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]')
address=web3.toChecksumAddress("0x28Dc729E17dEB0cF442B2Cf1AC7A6f3836aD6117")

contract = web3.eth.contract(address=address,abi=abi)

a=contract.functions.sendNewBatch(1000).call()
tx_hash=web3.toHex(contract.functions.sendNewBatch(1000).transact())
