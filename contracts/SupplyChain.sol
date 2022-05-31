pragma solidity ^0.5.0;

contract supplyChain {
    event newBatch(string timestamp,uint batch_id);
    event manufacture(string timestamp, uint batch_id, uint product_id);
    event qualityControl(string timestamp, uint product_id, uint grade, string comment);

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

    
}