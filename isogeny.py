
__all__ = ['TwoIsogeny', 'IsogenyChain']

from curve import Curve, KummerPoint

class TwoIsogeny:
    def __init__(self, K):
        if not isinstance(K, KummerPoint):
            raise ValueError('not a point')
        self.K = K
        self.domain = K.E
        self._compute()

    def _compute(self):
        self.K._normalize()
        A = self.K.E.A
        xK = self.K.x
        if not self.K or xK * (1 + xK * (A + xK)):
            raise ValueError('not a point of order 2')
        if xK:      # when the point is (alpha, 0) for alpha a root of x^2 + Ax + 1
            # TODO: implement a 2-isogeny here!
            self.codomain = ???

            ## TODO: make sure you can also push points through
            self._eval = lambda x,z: self.codomain(???)
        else:      # when the point is (0,0)  
            # TODO: implement a 2-isogeny here!
            self.codomain = ???

            ## TODO: make sure you can also push points through
            self._eval = lambda x,z: self.codomain(???)

    def __repr__(self):
        return f'{self.domain} —⟶ {self.codomain}'

    def __call__(self, P):
        return self._eval(P.x, P.z)

class IsogenyChain:
    def __init__(self, K, n):
        assert n >= 1

        self.steps = IsogenyChain._compute(K, n)

        self.domain = K.E
        self.codomain = self.steps[-1].codomain

    @staticmethod
    def _compute(K, n):
        # TODO: implement a chain of isogenies here!
        # tip: first implement the naive strategy, only later the balanced one.
        return ## returns a chain of isogenies in the right format

    def __repr__(self):
        return f'{self.domain} ——{len(self.steps)}—⟶ {self.codomain}'

    def __call__(self, P):
        for step in self.steps:
            P = step(P)
        return P

################################################################

import pytest
import random

from field import Field

class Test:
    @staticmethod
    def test_twoisogeny():
        gf = Field(2**31 - 1)
        E = Curve(gf(42))
        P = E(1058574377, 1)
        Q = E(1, 1058574377)
        R = E(0, 1)
        assert not E.xDBL(P)
        assert not E.xDBL(Q)
        assert not E.xDBL(R)

        phi = TwoIsogeny(P)
        psi = TwoIsogeny(Q)
        chi = TwoIsogeny(R)

        T = E(123, 1)
        n = 268427273
        assert n * T == R

        u = random.randrange(2**99)
        assert phi(u*T) == u*phi(T)
        assert psi(u*T) == u*psi(T)
        assert chi(u*T) == u*chi(T)

        assert phi(T) * 268427273 == phi.codomain(0, 1)
        assert psi(T) * 268427273 == psi.codomain(0, 1)
        assert chi(T) * 268427273 == chi.codomain(1, 0)

    @staticmethod
    def test_isogenychain():
        gf = Field(2**31 - 1)
        E = Curve(gf(0))
        K = E(23, 1)
        assert 2**28 * K and not 2**29*K
        phi = IsogenyChain(K, 29)
        assert len(phi.steps) == 29
        assert not phi(K)
        assert phi(E(7, 1)) == phi.codomain(920069272, 1)

