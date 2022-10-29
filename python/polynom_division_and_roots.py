import sys
import numpy as np
import matplotlib.pyplot as plt
from util import divisorsandnumdivisors, primefactors

def prep_poly(poly):
    poly = poly.split(",")
    poly = np.asarray(poly, dtype=float)
    return poly

def rational_root_theorem(poly):
    an = poly[0]
    a0 = poly[-1]
    ps = divisorsandnumdivisors(a0)[0]
    qs = divisorsandnumdivisors(an)[0]
    rat_roots = []
    for p in ps:
        for q in qs:
            ans = p/q
            if ans not in rat_roots:
                rat_roots.append(ans)
                rat_roots.append(-ans)

    rat_roots = list(set(rat_roots))
    
    rat_roots.sort()

    return rat_roots

def poly_div(big_poly, small_poly):
    if len(small_poly) > len(big_poly):
        return 'ERR'
    
    return None



big_poly = input("Enter coefficients of polynomial to be divided:  ")
big_poly = prep_poly(big_poly)

rrts = rational_root_theorem(big_poly)

print(f'possible roots exist at the following rational values {rrts}.')

test_rat_roots = input('Would you like to test all of them? [Y/n]')

test_rat_roots = test_rat_roots.lower()

if test_rat_roots[0] != 'y' and test_rat_roots[0] != '':
    small_poly = input("Enter coefficients of polynomial to divide into first polynomial.  Leave blank to exit: ")
    if small_poly == '':
        sys.exit()
    
    sys.exit()

solns = []
for rrt in rrts:
    ans = poly_div(big_poly, [1, rrt])
    solns.append(ans)



