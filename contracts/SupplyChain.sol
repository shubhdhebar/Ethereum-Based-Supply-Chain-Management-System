pragma solidity ^0.5.0;

contract supplyChain {

    event supplyChainEvent(uint processID, string timestamp, address from, address to, uint batch_id, uint product_id, uint qc_update, string optionalStrArg, uint lastProductAssembled, uint[20] QCQueue);

    function orderNewBatch(string memory timestamp, address supplier, address assembler, uint batchID, uint lastProductAssembled, uint[20] memory QCQueue) public returns (uint){
        batchID=batchID+1;
        emit supplyChainEvent(0, timestamp, supplier, assembler, batchID, 0,0,"",lastProductAssembled, QCQueue);
        return batchID;
    }


    function sendToInventory(string memory timestamp, address assembler, address inventory, uint product_id, address supplier, uint lastProductAssembled, uint[20] memory QCQueue) public{
        /*product_id: 1001 01 --> 1001:batch_id*/
        product_id=lastProductAssembled+1;
        uint batch_id = product_id/100;
        if (product_id%100==21){
            batch_id=orderNewBatch(timestamp, supplier, assembler, batch_id, lastProductAssembled, QCQueue);
            product_id=batch_id*100 + 1;
        }
        for(uint i=19;i>=1;i--){
            QCQueue[i]=QCQueue[i-1];
        }
        lastProductAssembled=product_id;
        QCQueue[0]=product_id;
        emit supplyChainEvent(1,timestamp, assembler, inventory, batch_id, product_id, 0," ",lastProductAssembled, QCQueue);
    }

    function qualityCheck(string memory timestamp, address qualityControl, address inventory, uint batch_id, uint product_id, string memory message, uint grade, uint lastProductAssembled, uint[20] memory QCQueue) public{
        uint index=0;
        for(uint i=0;i<20;i++){
            if(QCQueue[i]==product_id){
                index=i;
                break;
            }
        }

        if (grade==1){
            delete QCQueue[index];
            for (uint256 i = index; i < QCQueue.length - 1; i++) {
                QCQueue[i] = QCQueue[i+1];
            }
            
        }
        emit supplyChainEvent(2,timestamp, qualityControl, inventory, batch_id, product_id, grade, message, lastProductAssembled, QCQueue);
    
    }

    
}