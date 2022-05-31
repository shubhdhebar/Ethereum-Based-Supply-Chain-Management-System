import json
from web3 import Web3

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

print(web3.isConnected())
x=web3.eth.get_block_number()
print(web3.eth.get_block_number())
block=web3.eth.get_block(x-1)
print(Web3.toHex(block['transactions'][0]))
#infura_link = "https://mainnet.infura.io/v3/5b3035512c0641ac97400a817409c3e1"
#web3 = web3 = Web3(Web3.HTTPProvider(infura_link))
#balance = web3.eth.getBalance("0x0554a4d869Bc5aAAc849f142D4859e642884E876")
#print(balance)
