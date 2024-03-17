// SHARED CODE START

using test2 as B;

// Contract A (currentContract) state model
ghost mapping(uint => uint) contractAState;
// State of contract A (currentContract) that has been written to already, so we don't track its reads anymore
ghost mapping(uint => bool) killedFlagA;

// Contract B state model
ghost mapping(uint => uint) contractBState;
// State of contract B that has been written to already, so we don't track its reads anymore
ghost mapping(uint => bool) killedFlagB;

// update first-time reads
hook ALL_SLOAD(uint loc) uint value {
    uint dummy = require_uint256(to_mathint(loc));
	assert dummy >= 0;
   if(executingContract == currentContract && !killedFlagA[loc]) {
       require contractAState[loc] == value;
   } else if(executingContract == B && !killedFlagB[loc]) {
       require contractBState[loc] == value;
   }
}

// update writes
hook ALL_SSTORE(uint loc, uint value) {
    uint dummy = require_uint256(to_mathint(loc));
	assert dummy >= 0;
   if(executingContract == currentContract) {
      killedFlagA[loc] = true;
   } else if(executingContract == B) {
      killedFlagB[loc] = true;
   }
}

// assume the two contracts have the same state and address
function assume_equivalent_states() {
    // no slot has been read yet
    require forall uint i. !killedFlagA[i];
    require forall uint i. !killedFlagB[i];
    // same state
    require forall uint i. contractAState[i] == contractBState[i];
    // same address
    require currentContract == B;
}

// sets everything but the callee the same in two environments
function e_equivalence(env e1, env e2) {
    require e1.msg.sender == e2.msg.sender;
    require e1.block.timestamp == e2.block.timestamp;
    require e1.msg.value == e2.msg.value;
    require e1.block.number == e2.block.number;
    // require e1.msg.data == e2.msg.data;
}
// SHARED CODE END

// RULES START
rule equivalence_of_revert_conditions()
{
    storage init = lastStorage;
    assume_equivalent_states();
    bool remove_liquidity_test_revert;
    bool remove_liquidity_test2_revert;
    // using this as opposed to generating input parameters is experimental
    env e_remove_liquidity_test; calldataarg args;
    env e_remove_liquidity_test2;
    e_equivalence(e_remove_liquidity_test, e_remove_liquidity_test2);

    remove_liquidity@withrevert(e_remove_liquidity_test, args);
    remove_liquidity_test_revert = lastReverted;

    B.remove_liquidity@withrevert(e_remove_liquidity_test2, args) at init;
    remove_liquidity_test2_revert = lastReverted;

    assert(remove_liquidity_test_revert == remove_liquidity_test2_revert);
}

rule equivalnce_of_storage()
{
    env e;
    calldataarg args;
    storage init = lastStorage;
    assume_equivalent_states();

    remove_liquidity(e, args) at init;
    storage s1 = lastStorage;

    remove_liquidity(e, args) at init;
    storage s2 = lastStorage;

    assert s1 == s2;
}
