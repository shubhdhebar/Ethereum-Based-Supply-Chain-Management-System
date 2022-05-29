import json
import datetime 
import pytz #timezone
from fastapi import FastAPI
import uvicorn


import sys
sys.path.append('/home/shubhdhebar/Documents/Blockchain/Automobile Supply Chain Management/')
import DatabaseQueries.dbQueries as dbQueries

app=FastAPI()

supplier = "0x201d4f0E4BD39930Aa905B6A2A2803616dCfaA03"
assembler = "0x9c9Cc5Fdaf14e3D3Dcdb0E640448ddEBBF686720"
inventory = "0x04750f8664c32208CC80C4c60bDD2871467c7dc5"
pid=0

@app.post("/insertBatch")
def insertBatch(batch_id,timestamp,tx):
    dbQueries.addBatch(batch_id,timestamp,tx)


@app.post("/assembler")
def assemble(batch_id,product_id,timestamp,tx):
    dbQueries.addProduct(batch_id,product_id,timestamp,tx)
   
@app.post("/qualityControl")
def checkQuality(product_id,tx,message,grade):
    timestamp = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    dbQueries.addQC(product_id,str(timestamp),tx,message,grade)
    
@app.get("/track")
def trackProduct(product_id):
    data=dbQueries.fetchProduct(product_id)
    return {
        'ProductID':data[0],
        'BatchID':data[8],
        'Product Assembled on':data[1],
        'Transaction hash for assembly':data[2],
        'Quality assessment done on':data[3],
        'Grade assigned':data[7],
        'Comment(s) by Quality Control':data[6],
        'Transaction hash for Quality Control':data[4]
    }

    
    
    






    








