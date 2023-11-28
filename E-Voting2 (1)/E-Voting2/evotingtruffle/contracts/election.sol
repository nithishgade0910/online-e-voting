// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Election {
    struct Candidate {
        string name;
        uint voteCount;
    }
    
    struct Ballot {
        string title;
        mapping(uint => bool) voted; // Mapping to keep track of who voted
        uint[] candidateIds; // List of candidate IDs
    }

    address public admin;
    Ballot[] public ballots;
    Candidate[] public candidates;
    mapping(uint => mapping(address => bool)) public hasVoted;

    event Voted(address indexed voter, uint ballotId, uint candidateId);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only the admin can perform this action");
        _;
    }

    constructor() {
        admin = msg.sender;
    }
    
    function createBallot(string memory title, string[] memory candidateNames) public onlyAdmin {
    uint[] memory candidateIds = new uint[](candidateNames.length);
    // uint ballotId = ballots.length; // Get the index of the new ballot

    for (uint i = 0; i < candidateNames.length; i++) {
        uint candidateId = candidates.length;
        candidates.push(Candidate(candidateNames[i], 0));
        candidateIds[i] = candidateId;
    }

    // Create a new ballot and associate candidate IDs with the ballot
    Ballot storage newBallot = ballots.push();
    newBallot.title = title;
    
    for (uint i = 0; i < candidateNames.length; i++) {
        newBallot.candidateIds.push(candidateIds[i]);
    }
}


    function vote(uint ballotId, uint candidateId) public {
        Ballot storage ballot = ballots[ballotId];
        require(!hasVoted[ballotId][msg.sender], "You have already voted in this ballot.");
        require(candidateId < ballot.candidateIds.length, "Invalid candidate ID");
        
        hasVoted[ballotId][msg.sender] = true;
        candidates[ballot.candidateIds[candidateId]].voteCount++;
        emit Voted(msg.sender, ballotId, candidateId);
    }
    
    function getBallotCount() public view returns (uint) {
        return ballots.length;
    }
    
    function getCandidateCount() public view returns (uint) {
        return candidates.length;
    }
    
    function getBallotTitle(uint ballotId) public view returns (string memory) {
        return ballots[ballotId].title;
    }
    
    function getCandidateName(uint candidateId) public view returns (string memory) {
        return candidates[candidateId].name;
    }
    
    function getVoteCount(uint candidateId) public view returns (uint) {
        return candidates[candidateId].voteCount;
    }
}
