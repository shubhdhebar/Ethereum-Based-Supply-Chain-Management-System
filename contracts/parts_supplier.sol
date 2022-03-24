pragma solidity ^0.5.0;

contract automobile_parts_batch {
    function sendNewBatch(uint prevBatchID) public pure returns(uint newBatchID){
        newBatchID = prevBatchID+1;      
    }
}