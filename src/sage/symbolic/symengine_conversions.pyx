from cython.operator cimport dereference as deref
from sage.rings.integer cimport Integer
from sage.rings.rational cimport Rational
from sage.rings.real_mpfr cimport RealNumber, RealField_class
from sage.rings.complex_mpc cimport MPComplexNumber, MPComplexField_class
from sage.libs.mpfr cimport mpfr_set, MPFR_RNDN
from sage.libs.mpc cimport mpc_set, MPC_RNDNN
from symengine.lib.symengine_wrapper cimport (Integer as _Integer, Rational as _Rational,
    RealMPFR as _RealMPFR, ComplexMPC as _ComplexMPC, Basic)
from symengine.lib.symengine cimport mpz_class, mpq_class, mpfr_class, mpc_class, RCP

cimport symengine.lib.symengine as symengine

def convert_to_integer(_Integer i):
    cdef Integer z = Integer()
    z.set_from_mpz(deref(symengine.rcp_static_cast_Integer(i.thisptr)).as_mpz().get_mpz_t())
    return z

def convert_to_rational(_Rational i):
    cdef Rational z = Rational()
    z.set_from_mpq(deref(symengine.rcp_static_cast_Rational(i.thisptr)).as_mpq().get_mpq_t())
    return z

def convert_to_real_number(_RealMPFR i):
    cdef RealField_class parent = RealField_class(deref(symengine.rcp_static_cast_RealMPFR(i.thisptr)).get_prec())
    cdef RealNumber z = RealNumber(parent)
    mpfr_set(z.value, deref(symengine.rcp_static_cast_RealMPFR(i.thisptr)).as_mpfr().get_mpfr_t(), MPFR_RNDN)
    return z

def convert_to_mpcomplex_number(_ComplexMPC i):
    cdef MPComplexField_class parent = MPComplexField_class(deref(symengine.rcp_static_cast_ComplexMPC(i.thisptr)).get_prec())
    cdef MPComplexNumber z = parent._new()
    mpc_set(z.value, deref(symengine.rcp_static_cast_ComplexMPC(i.thisptr)).as_mpc().get_mpc_t(), MPC_RNDNN)
    return z

def convert_from_integer(Integer i):
    cdef mpz_class c = mpz_class(i.value)
    cdef _Integer z = _Integer()
    z.thisptr = <RCP[const symengine.Basic]>(symengine.integer(c))
    return z

def convert_from_rational(Rational i):
    cdef mpq_class c = mpq_class(i.value)
    cdef Basic r
    cdef RCP[const symengine.Basic] o = <RCP[const symengine.Basic]>(symengine.from_mpq(c))
    if symengine.is_a_Integer(deref(o)):
        r = _Integer.__new__(_Integer)
    else:
        r = _Rational.__new__(_Rational)
    r.thisptr = o
    return r

def convert_from_real_number(RealNumber i):
    cdef mpfr_class c = mpfr_class(i.value)
    cdef _RealMPFR z = _RealMPFR()
    z.thisptr = <RCP[const symengine.Basic]>(symengine.real_mpfr(c))
    return z

def convert_from_mpcomplex_number(MPComplexNumber i):
    cdef mpc_class c = mpc_class(i.value)
    cdef _ComplexMPC z = _ComplexMPC()
    z.thisptr = <RCP[const symengine.Basic]>(symengine.complex_mpc(c))
    return z
