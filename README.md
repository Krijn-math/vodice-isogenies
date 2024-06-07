# Implementing cutting-edge isogeny-based cryptography

This folder contains the materials you need to complete the tutorial
    Implementing cutting-edge isogeny-based cryptography
given by Lorenz Panny and Krijn Reijnders for the Croatia Summer School 2024.

### Schedule

The tutorial consists of four parts:
1. (09:00 - 10:30) A lecture on elliptic curves and isogenies, and in particular 2-isogenies.
2. (11:00 - 12:30) A block to work on implementing curve arithmetic and computing 2-isogenies.
3. (14:00 - 15:30) A lecture on 2^n-isogenies and their role in SQIsign verification.
4. (16:00 - 17:30) A block to work on implementing chains of 2-isogenies and (un)compressed SQIsign verification.

Note that, whoever achieves the fastest verification at the end of block 4 earns a prize!

### Implementation

To make your implementation work run smoothly, we have provided you with a number of files:
* the file `field.py` gives you a class to work with finite field arithmetic. You never need to edit anything in this file
    but it might be convenient to have a look so you know how things work.
* the file `curve.py` gives you a class to work with elliptic curves and points on elliptic curves, using x-only arithmetic.
    In this file, you will need to implement several algorithms.
* the file `isogeny.py` gives you the tools to do (chains of) 2-isogenies between supersingular elliptic curves, using x-only arithmetic.
    In this file, you will need to implement several algorithms.
* the file `sqisign.py` combines many of the above tools to run SQIsign verification for both compressed and uncompressed signatures.
    In this file, you will need to complete several functions to verify the signatures given in `good_signatures.py`
* the file `magic.py` contains a few small things that are annoying to implement, so we took care of this for you. You never need to
    look into this file, and you can just import the magic function `get_kernel_point(P, Q, s)` at the appropriate moment in `sqisign.py`

### Work in block 2

For block 2, the following needs to be implemented
* in `curve.py`, implement 
    * `xDBL`,
    * `xADD`, 
    * `__mul__`. 
    
    Then run `pytest curve.py` to verify your work is running smoothly.
* in `isogeny.py`, implement 
    * `_compute` in `TwoIsogeny`. 
    * Ignore `IsogenyChain` for now.
    
    Eventhough the isogeny chain tests will still fail, just run `pytest isogeny.py` to verify your 2-isogenies are running smoothly.

### Work in block 4

For block 4, the following needs to be implemented
* in `isogeny.py`, implement the remaining parts in `IsogenyChain`, namely `_compute`. We advise implement this first using the simple strategies given on the slides, and only later implementing the balanced strategy. Then run `pytest isogeny.py` to verify your work is running smoothly.
* in `sqisign.py`, first try to implement uncompressed SQIsign.
    * Implement `hash_message` and `recompute_challenge` to recompute E1 --> E2.
    * Then implement `compute_uncompressed_response` and see if you can verify the
    signatures in `good_signatures.py` by simply running `python3 isogeny.py`
    * For compressed SQIsign, implement `deterministic_basis_two_torsion`, which
    you can test with `test_deterministic_basis_two_torstion`. 
    * If you have finished
    uncompressed verification, `hash_message` and `recompute_challenge` should work
    already. So finish `compute_compressed_response` only.
    * Then run `isogeny.py` to verify your compressed signatures are running smoothly.
* To be complete, you can run `pytest *` to verify everything is done correctly.
* Celebrate! You have implemented SQIsign verification! Tell us your speed results.

Happy coding :-)
