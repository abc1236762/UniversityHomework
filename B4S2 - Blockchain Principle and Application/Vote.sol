// SPDX-License-Identifier: MIT
pragma solidity >=0.6;

/// @title 選舉投票
contract Vote {

    // 投票者
    struct Voter {
        string id; // 身分證字號
        bool canVote; // 是否能投票
        bool isVoted; // 是否已經投票了
        uint votedCandidateIndex; // 投給候選人的編號
    }

    // 候選人
    struct Candidate {
        string id; // 身分證字號
        string name; // 姓名
        uint voteCount; // 獲得票數
    }

    address public owner; // 擁有者
    mapping(address => Voter) voters; // 所有投票者
    Candidate[] public candidates; // 所有候選人
    string[] voterIDs; // 所有投票者的身分證字號
    bool isVoteFinished; // 投票是否結束

    constructor() public {
        owner = msg.sender;
        isVoteFinished = false;
    }

    // 將字串轉成非負整數陣列
    function stringToUIntArray(string memory str) private pure returns (uint[] memory) {
        bytes memory strBytes = bytes(str);
        uint[] memory uintArray = new uint[](strBytes.length);
        for (uint i = 0; i < strBytes.length; i++)
            uintArray[i] = uint(uint8(strBytes[i]));
        return uintArray;
    }

    // 驗證身分證字號
    function verifyID(string memory id) public pure returns (bool) {
        uint[] memory ida = stringToUIntArray(id);
        if (ida.length != 10) // 身分證字號必須是10位字元
            return false;
        uint[26] memory numberOfAlphabets = [
            uint(10), 11, 12, 13, 14, 15, 16, 17, 34, 18, 19, 20,
            21, 22, 35, 23, 24, 25, 26, 27, 28, 29, 32, 30, 31, 33
        ];
        uint iA = uint(uint8(bytes('A')[0]));
        uint i0 = uint(uint8(bytes('0')[0]));
        uint n0 = numberOfAlphabets[ida[0] - iA] / 10;
        uint n1 = numberOfAlphabets[ida[0] - iA] % 10;
        uint n = n0 * 1 + n1 * 9;
        for (uint i = 1; i < 9; i++)
            n += (ida[i] - i0) * (9 - i);
        n += (ida[9] - i0) * 1;
        return n % 10 == 0;
    }

    // 新增投票者，須包含地址和身分證字號，但匿名
    function addVoter(address addr, string memory id) public {
        require(msg.sender == owner); // 投票者須透過擁有者新增
        require(!isVoteFinished); // 投票完成後不能再新增投票者
        for (uint i = 0; i < voterIDs.length; i++) // 檢查投票者的身分證字號有無被新增過
            require(keccak256(bytes(id)) != keccak256(bytes(voterIDs[i])));
        require(verifyID(id)); // 驗證身分證字號是否有效
        voters[addr] = Voter({ id: id, canVote: true, isVoted: false, votedCandidateIndex: 0 });
        voterIDs.push(id);
    }

    // 新增候選人，須包含身分證字號和姓名，不需持有地址
    function addCandidate(string memory id, string memory name) public {
        require(msg.sender == owner); // 候選人須透過擁有者新增
        require(!isVoteFinished); // 投票完成後不能再新增候選人
        for (uint i = 0; i < candidates.length; i++) // 檢查候選人的身分證字號有無被新增過
            require(keccak256(bytes(id)) != keccak256(bytes(candidates[i].id)));
        require(verifyID(id)); // 驗證身分證字號是否有效
        candidates.push(Candidate({ id: id, name: name, voteCount: 0 }));
    }

    // 投票，須包含投票人自己的身分證字號和候選人的編號
    function vote(string memory voterID, uint candidateIndex) public {
        require(!isVoteFinished); // 投票完成後不能再投票
        Voter storage voter = voters[msg.sender]; // 取得投票人
        require(voter.canVote && !voter.isVoted); // 檢查投票人是否能投票（被擁有者新增過）和是否投過票
        require(keccak256(bytes(voterID)) == keccak256(bytes(voter.id))); // 檢查身分證字號是否一致
        require(candidateIndex < candidates.length); // 檢查候選人的編號是否有效
        voter.isVoted = true;
        voter.votedCandidateIndex = candidateIndex;
        candidates[candidateIndex].voteCount += 1;
    }

    // 完成投票
    function finishVote() public {
        require(msg.sender == owner); // 須由擁有者決定是否完成投票
        isVoteFinished = true;
    }

    // 勝選的候選人的編號
    function winningCandidateIndex() public view returns (uint winningCandidateIndex_) {
        require(isVoteFinished); // 投票結束之前不能公布避免棄保效應
        uint winningVoteCount = 0;
        for (uint i = 0; i < candidates.length; i++) {
            if (candidates[i].voteCount > winningVoteCount) {
                winningVoteCount = candidates[i].voteCount;
                winningCandidateIndex_ = i;
            }
        }
    }

    // 勝選的候選人的姓名
    function winningCandidateName() public view returns (string memory winningCandidateName_) {
        require(isVoteFinished); // 投票結束之前不能公布避免棄保效應
        winningCandidateName_ = candidates[winningCandidateIndex()].name;
    }

}
