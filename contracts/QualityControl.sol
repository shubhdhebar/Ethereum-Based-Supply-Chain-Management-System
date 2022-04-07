pragma solidity ^0.5.0;

contract QualityControl{
    event qualityControl(string timestamp,uint product_id,string officer,string message,uint grade);

    function qualityCheck(string memory timestamp,uint product_id,string memory officer,string memory message,uint grade) public{
        emit qualityControl(timestamp, product_id, officer, message, grade);
    }

}
