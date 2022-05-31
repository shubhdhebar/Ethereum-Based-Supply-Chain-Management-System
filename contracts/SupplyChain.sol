pragma solidity ^0.5.0;

contract supplyChain {
    event newBatch(string timestamp,uint batch_id);
    event manufacture(string timestamp, uint batch_id, uint product_id);
    event qualityControl(string timestamp, uint product_id, uint grade, string comment);
    event newOrder(string timestamp,uint order_id,uint retailer,uint qty);
    event dispatch(string timestamp,uint product_id,uint order_id,uint retailer);

    function orderNewBatch(string memory timestamp, uint batchID) public returns (uint){
        batchID=batchID+1;
        emit newBatch(timestamp, batchID);
        return batchID;
    }

    function sendToInventory(string memory timestamp, uint product_id) public{
        /*product_id: 1001 01 --> 1001:batch_id*/
        uint batch_id = product_id/100;
        if (product_id%100==21){
            batch_id=orderNewBatch(timestamp, batch_id);
            product_id=batch_id*100 + 1;
        }
        emit manufacture(timestamp, batch_id, product_id);
    }

    function qualityCheck(string memory timestamp, uint product_id, uint grade, string memory comment) public{

        emit qualityControl(timestamp, product_id, grade, comment);
    
    }

    function generateOrder(string memory timestamp,uint order_id,uint retailer,uint qty) public{
        emit newOrder(timestamp,order_id,retailer,qty);
    }

    function assignRetailer(string memory timestamp,uint product_id,uint order_id,uint retailer) public{
        emit dispatch(timestamp,product_id,order_id,retailer);
    }
}