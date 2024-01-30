userBalances: public(HashMap[address, uint256])

@external
@nonreentrant("lock")
def add_liquidity() -> bool:
    return True

@external
@nonreentrant("lock")
def remove_liquidity(amount: uint256):
    assert self.userBalances[msg.sender] >= amount, "Insufficient balance"
    send(msg.sender, amount)
    self.userBalances[msg.sender] -= amount
