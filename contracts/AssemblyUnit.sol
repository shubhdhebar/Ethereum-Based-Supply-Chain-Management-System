pragma solidity ^0.5.0;

contract assembly_unit {
    uint batch_id;
    
    event newBatch(uint process_id, address supplier, address assembler, uint batch_id);

    function orderNewBatch(address supplier, address assembler, uint batchID) public payable{
        batchID=batchID+1;
        emit newBatch(0, supplier, assembler, batchID);
    }

    event manufacture(uint process_id, address assembler, address inventory, uint product_id, uint batch_id);


    function sendToInventory(address assembler, address inventory, uint product_id, address supplier) public payable{
        /*product_id: 1001 01 --> 1001:batch_id*/
        batch_id = product_id/100;
        if (product_id%100==21){
            orderNewBatch(supplier, assembler, batch_id);
            product_id=batch_id*100 + 1;
        }
        
        emit manufacture(1, assembler, inventory, product_id, batch_id);
    }

    
}