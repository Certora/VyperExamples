# Curve Compiler Reentrancy Bug

## Specification
The specification for this bug is outlined in the file: `CurveBugExample/add_liquidity_test_to_add_liquidity_test2_equivalence.spec`

## Contracts
There are two contracts involved, both with the same code but compiled using different versions of the Vyper compiler:
- `CurveBugExample/test.vy`: Compiled with Vyper 0.3.0
- `CurveBugExample/test2.vy`: Compiled with Vyper 0.3.1

## Job Link
Check the detailed analysis and counterexample at [Certora Prover](https://prover.certora.com/output/30078/57f600951e3443ca9dd5ac4bfaf16193?anonymousKey=856c55364b6b350d2199c9cbeb0c14517dd1d72a)

The counterexample reveals that a revert for reentrancy occurs in the Vyper 0.3.1 version, while it does not happen in the Vyper 0.3.0 version.