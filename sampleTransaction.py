from web3 import Web3

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
#Send 1 eth from Acc1 to Acc2
acc_1 = "0x4EA37346e29cF0092ec5C8Ed7792Efa4288fE669"
pvt_key = "86527a13d1574691f579f56f90b083944061a5bafbd472dff505db5c04fe5ad4"

acc_2 = "0xCc72f0be4E2699a2C7b7b97150d97F04D278698f"

nonce = web3.eth.getTransactionCount(acc_1)

tx = {
    'nonce' : nonce,
    'to' : acc_2, 
    'from' : acc_1,
    'value' : web3.toWei(1,'ether'),
    'gas' : 2000000,
    'gasPrice' : web3.toWei(50,'gwei')
}

signed_tx = web3.eth.account.signTransaction(tx,pvt_key)
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(web3.toHex(tx_hash))