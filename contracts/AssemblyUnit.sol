pragma solidity ^0.5.0;

contract assembly_unit {
    uint batch_id;
    

    event newBatch(string timestamp, address supplier, address assembler, uint batch_id);

    function orderNewBatch(string memory timestamp, address supplier, address assembler, uint batchID) public returns (uint){
        batchID=batchID+1;
        emit newBatch(timestamp, supplier, assembler, batchID);
        return batchID;
    }

    event manufacture(string timestamp, address assembler, address inventory, uint product_id, uint batch_id);


    function sendToInventory(string memory timestamp, address assembler, address inventory, uint product_id, address supplier) public{
        /*product_id: 1001 01 --> 1001:batch_id*/
        batch_id = product_id/100;
        if (product_id%100==21){
            batch_id=orderNewBatch(timestamp, supplier, assembler, batch_id);
            product_id=batch_id*100 + 1;
        }
        
        emit manufacture(timestamp, assembler, inventory, product_id, batch_id);
    }
    
}