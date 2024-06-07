#!/usr/bin/env python3

import random
from field import Field
from curve import Curve
from isogeny import IsogenyChain

f = 1 << 7
cof = 0xb34281e63cfdf2985b9f1f5de85f0f51
p = (cof << f) - 1

################################################################

def deterministic_basis_two_torsion(E):
    F = E.A.gf

    # TODO: this one is tricky. good luck :^)

    return xP, xQ

def test_deterministic_basis_two_torsion():
    gf = Field(p)
    E = Curve(gf(6))
    P,Q = deterministic_basis_two_torsion(E)
    assert (P,Q) == deterministic_basis_two_torsion(E) # deterministic
    assert not 2**f * P
    assert not 2**f * Q
    assert 2**(f-1) * P
    assert 2**(f-1) * Q
    assert 2**(f-1) * P != 2**(f-1) * Q


from magic import three_point_ladder, get_kernel_point


from hashlib import sha256
def hash_to_integer(message):
    s = sha256(message).digest()
    s = int.from_bytes(s, 'big') % 2**f
    return s

def hash_message(E, message):

    xP, xQ = deterministic_basis_two_torsion(E)
    s = hash_to_integer(message)

    return get_kernel_point(xP, xQ, s)


def compute_uncompressed_response(E, blocks):
    for xK in blocks:
        K = E(xK)
        phi = IsogenyChain(K, f)
        E = phi.codomain
    
    return E

def compute_compressed_response(E, blocks):
    for swap,s in blocks:
        P, Q = deterministic_basis_two_torsion(E)
        if swap:
            P,Q = Q,P
        K = get_kernel_point(P, Q, s)
        phi = IsogenyChain(K, f)
        E = phi.codomain
    
    return E

def recompute_challenge(curve, message):
     K = hash_message(curve, message)
     return IsogenyChain(K, 128).codomain

def verify_uncompressed_signature(pk, signature, message):
    EA = Curve(pk)

    # assume signature = [ [K_i], E_1]
    blocks = signature[0]
    E1 = Curve(signature[1])

    E2_resp = compute_uncompressed_response(EA, blocks)
    E2_chall = recompute_challenge(E1, message)

    return E2_resp == E2_chall

def verify_compressed_signature(pk, signature, message):
    EA = Curve(pk)

    # assume signature = [ [swap_i,s_i], E_1]
    blocks = signature[0]
    E1 = Curve(signature[1])

    E2_resp = compute_compressed_response(EA, blocks)
    E2_chall = recompute_challenge(E1, message)

    return E2_resp == E2_chall

################################################################

msg = b'Hello, world!'

if __name__ == '__main__':
    from good_signatures import get_signatures

    gf = Field(p)
    sigs = get_signatures(gf.i())

    for j,(pk,sig,_) in enumerate(sigs):

        print()
        print(f'\x1b[33muncompressed signature #{j+1}\x1b[0m')

        if verify_uncompressed_signature(pk, sig, msg):
            print(f'    \x1b[32muncompressed verification succeeded. :^)\x1b[0m')
        else:
            print(f'    \x1b[31mUNCOMPRESSED VERIFICATION FAILED! BAD!!\x1b[0m')

    print()
    print(f'\x1b[35mAVERAGE COST: {gf.cost() / len(sigs)}\x1b[0m')

    gf = Field(p)
    sigs = get_signatures(gf.i())

    for j,(pk,_,compressed) in enumerate(sigs):

        print()
        print(f'\x1b[33mcompressed signature #{j+1}\x1b[0m')

        if verify_compressed_signature(pk, compressed, msg):
            print(f'    \x1b[32mcompressed verification succeeded. :^)\x1b[0m')
        else:
            print(f'    \x1b[31mCOMPRESSED VERIFICATION FAILED! BAD!!\x1b[0m')

    print()
    print(f'\x1b[35mAVERAGE COST: {gf.cost() / len(sigs)}\x1b[0m')

