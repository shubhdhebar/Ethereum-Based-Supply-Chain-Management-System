import json 
import pymongo

client = pymongo.MongoClient("mongodb+srv://shubhdhebar:tiger@cluster0.dja6u.mongodb.net/test")
db = client["AutomobileSupplyChain"]
coll=db["Product"]

data = {
    "name:":"iphone11",
    "type":"phone"
}
x=coll.insert_one(data)
print(x)


