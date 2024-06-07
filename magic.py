
def three_point_ladder(P, Q, PmQ, s):
    assert P.z == 1
    assert Q.z == 1
    assert PmQ.z == 1

    binary = lambda n: n>0 and [n&1]+binary(n>>1) or []
    bits = binary(s)

    P0 = Q
    P1 = P
    P2 = PmQ
    E = P.E

    for i in range(len(bits)):
        if bits[i] == 1:
            # this can be done by one function xDBLADD
            # to be faster and more elegant
            P1 = E.xADD(P0, P1, P2)
            P0 = E.xDBL(P0)
            # P0, P1 = xDBLADD(P0, P1, P2)
        else:
            P2 = E.xADD(P0, P2, P1)
            P0 = E.xDBL(P0)
            # P0, P2 = xDBLADD(P0, P2, P1)

    return P1


import random
from field import Field
from curve import Curve

def test_three_point_ladder():
    from sqisign import p, f
    from sqisign import deterministic_basis_two_torsion
    gf = Field(p)
    E = Curve(gf(6))
    P,Q = deterministic_basis_two_torsion(E)
    P._normalize()
    Q._normalize()
    assert E.is_x_coordinate(P.x)
    assert E.is_x_coordinate(Q.x)
    PmQ = point_difference(P, Q)
    assert E.is_x_coordinate(PmQ.x / PmQ.z)
    s = random.randrange(1, 2**99, 2)  # odd
    R = three_point_ladder(P, Q, PmQ, s)
    assert E.is_x_coordinate(R.x / R.z)
    assert not 2**f * R
    assert 2**(f-1) * R


def point_difference(xP, xQ):
    #we assume xP, xQ and A are affine
    assert xP.z == 1
    assert xQ.z == 1

    assert xP.E == xQ.E
    E = xP.E

    A = E.A
    F = E.A.gf

    PmQZ = xP.x - xQ.x
    t2 = xP.x * xQ.x
    t3 = t2 - F.one()
    t0 = PmQZ * t3
    PmQZ = PmQZ**2
    t0 = t0**2
    t1 = t2 + F.one()
    t3 = xP.x + xQ.x
    t1 = t1 * t3
    t2 = t2 * A
    t2 = t2 + t2
    t1 = t1 + t2
    t2 = t1**2
    t0 = t2 - t0

    assert t0.is_square()
    t0 = t0.sqrt()
    PmQX = t0 + t1

    PmQ = PmQX / PmQZ

    return E(PmQ)

def test_point_difference():
    from sqisign import p
    from sqisign import deterministic_basis_two_torsion
    gf = Field(p)
    E = Curve(gf(6))
    P,Q = deterministic_basis_two_torsion(E)
    a = random.randrange(2**99)
    b = random.randrange(2**99)
    Q = a * P; Q._normalize()
    R = b * P; R._normalize()
    T = point_difference(Q, R)
    assert T in ((a-b)*P, (a+b)*P)


def get_kernel_point(xP, xQ, s):
    # should get diff of xP and xQ
    # then performs three point ladder
    # returns K = xP + s*xQ

    xP._normalize()
    xQ._normalize()
    PmQ = point_difference(xP, xQ)
    K = three_point_ladder(xP, xQ, PmQ, s)

    return K


