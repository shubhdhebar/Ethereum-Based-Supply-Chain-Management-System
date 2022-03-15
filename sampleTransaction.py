from web3 import Web3

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
#Send 1 eth from Acc1 to Acc2
acc_1 = "0x201d4f0E4BD39930Aa905B6A2A2803616dCfaA03"
pvt_key = "3d1b9180b8c26e2024a4f27ed80c72e9861597a7364b0053f57a511e2d2137e4"

acc_2 = "0x9c9Cc5Fdaf14e3D3Dcdb0E640448ddEBBF686720"

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