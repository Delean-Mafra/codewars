# https://www.codewars.com/kata/6a5b869384e6bea2681dbb5d/train/python
import sys
import decimal
try:
    sys.set_int_max_str_digits(0)
except:
    pass
try:
    import gmpy2
    dm_tem_gmpy=True
except ImportError:
    dm_tem_gmpy=False
def previous_fib(n:int)->int|None:
    if n==0:
        return None
    if n==1:
        return 0
    if dm_tem_gmpy:
        dm_n_gmp=gmpy2.mpz(n)
        dm_5n2=5*dm_n_gmp*dm_n_gmp
        dm_c1=dm_5n2+4
        if gmpy2.is_square(dm_c1):
            return int((gmpy2.isqrt(dm_c1)-dm_n_gmp)//2)
        dm_c2=dm_5n2-4
        if gmpy2.is_square(dm_c2):
            return int((gmpy2.isqrt(dm_c2)-dm_n_gmp)//2)
        return None
    dm_bits=n.bit_length()
    dm_prec_base=int(dm_bits*0.30103)+20
    decimal.getcontext().prec=dm_prec_base
    dm_dec_n=decimal.Decimal(n)
    dm_dec_5=decimal.Decimal(5)
    dm_inv_fi=(dm_dec_5.sqrt()-decimal.Decimal(1))/decimal.Decimal(2)
    dm_anterior=dm_dec_n*dm_inv_fi
    dm_ans=dm_anterior.to_integral_value(rounding=decimal.ROUND_HALF_UP)
    decimal.getcontext().prec=dm_prec_base*2+10
    dm_verif=dm_ans*(dm_dec_n+dm_ans)-dm_dec_n*dm_dec_n
    if abs(dm_verif)==1:
        return int(dm_ans)
    return None
