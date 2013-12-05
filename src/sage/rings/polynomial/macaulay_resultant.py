"""
Macaulay Resultant of Multivariate Polynomials

This is an implementation of the Macaulay Resultant. It computes
the resultant of universal polynomials as well as polynomials
with constant coefficients. This is a project done in
sage days 55. It's based on the implementation in Maple by
Manfred Minimair, which in turn is based on the following:

-Using Algebraic Geometry by Cox, Little, O'Shea
-Canny, J., "Generalised characteristic polynomials", p.241--250,
           J. Symbolic Comput. Vol. 9, No. 3, 1990
-The algebraic theory of modular systems by Macaulay


AUTHORS:

- Hao Chen <chenh123@uw.edu>
- Solomon Vishkautsan <wishcow@gmail.com>

"""

from sage.combinat.integer_vector_weighted import WeightedIntegerVectors
from sage.misc.misc_c import prod
from sage.matrix.constructor import matrix
from sage.rings.integer_ring import ZZ
from sage.rings.arith import binomial
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing

def getS(mon_deg_tuple,dlist):
    r"""
    In the MR algorithm the list of all monomials of the total degree is partitioned into sets S_i.
    This function returns the index i for the set S_i for the inputted given monomial.

    INPUT:

    - `mon_deg_tuple` -- a list representing a monomial of a degree d
    - `dlist` -- a list of degrees d_i of the polynomials in question, where
    d =  sum(dlist) - len(dlist) + 1

    OUTPUT:

    - the index i such that the input monomial lives in S_i

    EXAMPLES::

        sage: from sage.rings.polynomial.macaulay_resultant import getS
        sage: getS([1,1,0],[2,1,1]) # the monomial xy where the total degree = 2
        1

        sage: getS([29,21,8],[10,20,30])
        0

        sage: getS(range(0,9)+[10],range(1,11))
        9
    """
    for i in xrange(len(dlist)):
        if mon_deg_tuple[i] - dlist[i] >= 0:
            return i


def monomials(d,R):
    r"""
    returns all the monomials of degree d with variables a list of
    generators of the ring R

    INPUT:

    -`d` -- a positive integer
    -`R` -- a polynoimal ring

    OUTPUT:

    - a list of all monomials of degree d.

    EXAMPLES::

        sage: from sage.rings.polynomial.macaulay_resultant import monomials
        sage: monomials(3, PolynomialRing(QQ,3,'x'))
        [x0^3, x0^2*x1, x0^2*x2, x0*x1^2, x0*x1*x2, x0*x2^2, x1^3, x1^2*x2, x1*x2^2, x2^3]

    It's OK if the coefficients of R live in some polynomial ring::

        sage: U = PolynomialRing(QQ,20,'u')
        sage: monomials(2, PolynomialRing(U,5,'x'))
        [x0^2, x0*x1, x0*x2, x0*x3, x0*x4, x1^2, x1*x2, x1*x3, x1*x4, x2^2, x2*x3, x2*x4, x3^2, x3*x4, x4^2]

    """
    xlist = R.gens()
    n = len(xlist) -1
    one_list = [1 for i in xrange(0,n+1)]
    degs = WeightedIntegerVectors(d, one_list)
    return [prod([xlist[i]**(deg[n-i]) for i in xrange(0,len(deg))])
             for deg in degs]

def is_reduced(mon_degs,dlist):
    r"""
    A monomial in the variables x_0,...,x_n is called reduced with respect to the list of degrees d_0,...,d_n
    if the degree of x_i in the monomial is >= d_i for exactly one i. This function checks this property for an inputted monomial.

    INPUT:

    - mon -- a monomial in the variables listed in xlist
    - dlist -- a list of degrees with respect to which we check reducedness
    - xlist -- a list of variables in some Polynomial ring.

    OUTPUT:

    - True/False

    EXAMPLES::

        sage: from sage.rings.polynomial.macaulay_resultant import is_reduced
        sage: R.<x,y,z> = PolynomialRing(QQ,3)
        sage: is_reduced([2,3,1],[2,3,3]) # the monomial x^2*y^3*z is not reduced w.r.t. degrees vector [2,3,3]
        False

        sage: R.<x,y,z> = PolynomialRing(QQ,3)
        sage: is_reduced([1,3,2],[2,3,3]) # the monomial x*y^3*z^2 is not reduced w.r.t. degrees vector [2,3,3]
        True
    """
    #TODO fix comments to reflect change in input parameters 
    #RRR deg = [mon.degree(xi) for xi in xlist]
    diff = [mon_degs[i] - dlist[i] for i in xrange(0,len(dlist))]
    return len([1 for d in diff if d >= 0]) == 1

def construct_universal_polynomial(dlist):
    r"""
    Given a list of degrees, this function returns a list of len(dlist) polynomials with len(dlist) variables,
    with generic coefficients. This is useful for generating polynomials for tests,
    and for getting the general resultant for the given degrees.

    INPUT:

    - dlist -- a list of degrees.

    OUTPUT:

    - a list of polynomials of the given degrees with general coefficients.
    - a polynomial ring over ZZ generated by the coefficients of the output polynomials.

    EXAMPLES::

        sage: from sage.rings.polynomial.macaulay_resultant import construct_universal_polynomial
        sage: construct_universal_polynomial([1,1,2])
        ([u0*x0 + u1*x1 + u2*x2, u3*x0 + u4*x1 + u5*x2, u6*x0^2 + u7*x0*x1 + u9*x1^2 + u8*x0*x2 + u10*x1*x2 + u11*x2^2],
            Multivariate Polynomial Ring in u0, u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11 over Integer Ring)
    """

    n  = len(dlist) - 1
    number_of_coeffs = sum([binomial(n+di,di) for di in dlist])
    U = PolynomialRing(ZZ,'u',number_of_coeffs)
    d = sum(dlist) - len(dlist) + 1
    flist = []
    R = PolynomialRing(U,'x',n+1)
    #TODO remove ugly prints
    #print R
    ulist  = U.gens()
    for d in dlist:
        # construct a universal polynomial of degree d
        # suppose we already have mon_d
        mon_d = monomials(d,R)
        #print mon_d
        f = sum([mon_d[i]*ulist[i] for i in xrange(0,len(mon_d))])
        flist.append (f)
        #print f
        ulist = ulist[len(mon_d):]
    return flist, U

def macaulay_resultant(flist):
    r"""
    This is an implementation of the Macaulay Resultant. It computes
    the resultant of universal polynomials as well as polynomials
    with constant coefficients. This is a project done in
    sage days 55. It's based on the implementation in Maple by
    Manfred Minimair, which in turn is based on the following:

    -Using Algebraic Geometry by Cox, Little, O'Shea
    -Canny, J., "Generalised characteristic polynomials", p.241--250,
               J. Symbolic Comput. Vol. 9, No. 3, 1990
    -The algebraic theory of modular systems by Macaulay

    It calculates the Macaulay resultant for a list of Polynomials,
    up to sign!

    AUTHORS:

    - Hao Chen <chenh123@uw.edu>
    - Solomon Vishkautsan <wishcow@gmail.com>


    INPUT:

    - flist -- a list of n homogeneous polynomials in n variables

    OUTPUT:

    - the resultant

    EXAMPLES:


    The number of polynomials has to match the number of variables::

        sage: R.<x,y,z> = PolynomialRing(QQ,3)
        sage: macaulay_resultant([y,x+z])
        Traceback (most recent call last):
        ...
        AssertionError: number of polynomials(= 2) must equal number of variables (= 3)

    The polynomials need to be all homogeneous::

        sage: from sage.rings.polynomial.macaulay_resultant import *
        sage: R.<x,y,z> = PolynomialRing(QQ,3)
        sage: macaulay_resultant([y, x+z, z+x^3])
        Traceback (most recent call last):
        ...
        AssertionError: resultant for non-homogeneous polynomials is not supported

    The following example recreates Proposition 2.10 in Ch.3 of Using Algebraic Geometry::

        sage: flist,_ = construct_universal_polynomial([1,1,2])
        sage: macaulay_resultant(flist)
        u2^2*u4^2*u6 - 2*u1*u2*u4*u5*u6 + u1^2*u5^2*u6 - u2^2*u3*u4*u7 + u1*u2*u3*u5*u7 + u0*u2*u4*u5*u7 - u0*u1*u5^2*u7 + u1*u2*u3*u4*u8 - u0*u2*u4^2*u8 - u1^2*u3*u5*u8 + u0*u1*u4*u5*u8 + u2^2*u3^2*u9 - 2*u0*u2*u3*u5*u9 + u0^2*u5^2*u9 - u1*u2*u3^2*u10 + u0*u2*u3*u4*u10 + u0*u1*u3*u5*u10 - u0^2*u4*u5*u10 + u1^2*u3^2*u11 - 2*u0*u1*u3*u4*u11 + u0^2*u4^2*u11

    The following example degenerates into the determinant of a 3*3 matrix::

        sage: flist,_ = construct_universal_polynomial([1,1,1])
        sage: macaulay_resultant(flist)
        -u2*u4*u6 + u1*u5*u6 + u2*u3*u7 - u0*u5*u7 - u1*u3*u8 + u0*u4*u8

    The following example is by Patrick Ingram(arxiv:1310.4114)::

        sage: U = PolynomialRing(ZZ,'y',2); y0,y1 = U.gens()
        sage: R = PolynomialRing(U,'x',3); x0,x1,x2 = R.gens()
        sage: f0 = y0*x2^2 - x0^2 + 2*x1*x2
        sage: f1 = y1*x2^2 - x1^2 + 2*x0*x2
        sage: f2 = x0*x1 - x2^2
        sage: flist = [f0,f1,f2]
        sage: macaulay_resultant([f0,f1,f2])
        y0^2*y1^2 - 4*y0^3 - 4*y1^3 + 18*y0*y1 - 27

    a simple example with constant rational coefficients::

        sage: R.<x,y,z,w> = PolynomialRing(QQ,4)
        sage: macaulay_resultant([w,z,y,x])
        1

    an example where the resultant vanishes::

        sage: R.<x,y,z> = PolynomialRing(QQ,3)
        sage: macaulay_resultant([x+y,y^2,x])
        0

    an example of bad reduction at a prime p = 5::

        sage: R.<x,y,z> = PolynomialRing(QQ,3)
        sage: macaulay_resultant([y,x^3+25*y^2*x,5*z])
        125

    an example when the coefficients live in a finite field::

        sage: F = FiniteField(11)
        sage: R.<x,y,z,w> = PolynomialRing(F,4)
        sage: macaulay_resultant([z,x^3,5*y,w])
        4


    example when the denominator in the algorithm vanishes(in this case
    the resultant is the constant term of the quotient of
    char polynomials of numerator/denominator)::

        sage: R.<x,y,z> = PolynomialRing(QQ,3)
        sage: macaulay_resultant([y, x+z, z^2])
        -1

    when there are only 2 functions, macaulay resultant degenerates to the traditional resultant::

        sage: R.<x> = PolynomialRing(QQ,1)
        sage: f =  x^2+1; g = x^5+1
        sage: f.resultant(g) == macaulay_resultant([f.homogenize(),g.homogenize()])
        True
    """
    #TODO add test that checks that the output of the function is a polynomial
    assert len(flist) > 0, 'you have to input least 1 polynomial in the list'
    assert all([f.is_homogeneous() for f in flist]), 'resultant for non-homogeneous polynomials is not supported'
    R  = flist[0].parent()
    dlist = [f.degree() for f in flist]
    xlist = R.gens()
    assert len(xlist) == len(dlist), 'number of polynomials(= %d) must equal number of variables (= %d)'%(len(dlist),len(xlist))
    n  = len(dlist) - 1
    d = sum(dlist) - len(dlist) + 1
    one_list = [1 for i in xrange(0,len(dlist))]
    mons = WeightedIntegerVectors(d, one_list)  # list of exponent-vectors(/lists) of monomials of degree d
    #mon_d = [prod([xlist[i]**(deg[i]) for i in xrange(0,len(deg))]) for deg in mons]
    mons_num = len(mons)
    mons_to_keep = []
    newflist = []
    result = []

    for j in xrange(0,mons_num):
        if not is_reduced(mons[j],dlist):
            mons_to_keep.append(j)
        si_mon = getS(mons[j], dlist)
        # Monomial is in S_i under the partition, now we reduce the i'th degree of the monomial
        new_mon = list(mons[j])
        new_mon[si_mon] -= dlist[si_mon]
        quo = prod([xlist[k]**(new_mon[k]) for k in xrange(0,n+1)]) # this produces the actual reduced monomial
        new_f = flist[si_mon]*quo
        # we strip the coefficients of the new polynomial:
        result.append([new_f[mon] for mon in mons])

    numer_matrix = matrix(result)
    denom_matrix = numer_matrix.matrix_from_rows_and_columns(mons_to_keep,mons_to_keep)
    if denom_matrix.dimensions()[0] == 0: # here we choose the determinant of an empty matrix to be 1
        return numer_matrix.det()
    denom_det = denom_matrix.det()
    if denom_det != 0:
        return numer_matrix.det()/denom_det
    # if we get to this point, the determinant of the denominator was 0, and we get the resultant
    # by taking the free coefficient of the quotient of two characteristic polynomials
    poly_num  = numer_matrix.characteristic_polynomial('T')
    poly_denom  = denom_matrix.characteristic_polynomial('T')
    poly_quo  = poly_num.quo_rem(poly_denom)[0]
    return poly_quo(0)


def macaulay_general_resultant(dlist):
    r"""
    this is just a wrapper function of macaulay_resultant, where
    it takes a list of degrees as input and returns the resultant of
    a list of generic polynomials with coefficients in a polynomial ring.

    INPUT:

    - dlist -- a list of degrees

    OUTPUT:

    - the general resultant

    EXAMPLES::

        sage: from sage.rings.polynomial.macaulay_resultant import macaulay_general_resultant
        sage: macaulay_general_resultant([1,1,2])
        u2^2*u4^2*u6 - 2*u1*u2*u4*u5*u6 + u1^2*u5^2*u6 - u2^2*u3*u4*u7 + u1*u2*u3*u5*u7 + u0*u2*u4*u5*u7 - u0*u1*u5^2*u7 + u1*u2*u3*u4*u8 - u0*u2*u4^2*u8 - u1^2*u3*u5*u8 + u0*u1*u4*u5*u8 + u2^2*u3^2*u9 - 2*u0*u2*u3*u5*u9 + u0^2*u5^2*u9 - u1*u2*u3^2*u10 + u0*u2*u3*u4*u10 + u0*u1*u3*u5*u10 - u0^2*u4*u5*u10 + u1^2*u3^2*u11 - 2*u0*u1*u3*u4*u11 + u0^2*u4^2*u11
    """
    assert all([d >=0 for d in dlist]), 'degrees must be non-negative'
    flist, U = construct_universal_polynomial(dlist)
    return U(macaulay_resultant(flist))
