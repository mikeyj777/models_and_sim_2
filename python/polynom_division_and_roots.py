import sys
import copy
import numpy as np
import matplotlib.pyplot as plt
from util import divisorsandnumdivisors, primefactors

def prep_poly(poly):
    poly = poly.split(',')
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
    
    working_poly = copy.deepcopy(big_poly)
    working_poly = np.asarray(working_poly)
    s = np.asarray(small_poly)
    s_num_consts = np.count_nonzero(s)
    c = []

    while np.count_nonzero(working_poly) >= s_num_consts:
        if working_poly[0] == 0:
            c.append(0)
        else:
            c.append(working_poly[0] / s[0])
        carry_poly = c[-1] * s
        diff = len(working_poly) - len(s)
        if diff > 0:
            carry_poly = np.pad(carry_poly, (0,diff), 'constant', constant_values=(0))
        working_poly -= carry_poly
        working_poly = working_poly[1:]

    if working_poly.sum() > 0:
        return 'ERR'

    return c

def poly_in_text(p):
    curr_pow = len(p)
    poly_str = ''
    put_an_operator = False
    for val in p:
        if val == 0:
            continue
        oper = ''
        if put_an_operator:
            oper = '+ '
            if val < 0:
                oper = '- '
        else:
            put_an_operator = True
        curr_pow -= 1
        val_txt = f'{oper}{abs(val)}'

        x_txt = f' * x ^ {curr_pow}'
        if curr_pow == 0:
            x_txt = ''
        poly_str += f'{val_txt}{x_txt} '
    
    return f'({poly_str[:-1]})'
    
def print_result(big_poly, small_poly, poly_div_output):
    big_poly_txt = poly_in_text(big_poly)
    small_poly_txt = poly_in_text(small_poly)
    v = poly_div_output
    if v != 'ERR':
        output = poly_in_text(v)
        print(f'the result of polynomial {big_poly_txt} divided by {small_poly_txt} is {output}.')
    else:
        print(f'the polynomial {big_poly_txt} cannot be evenly divided by {small_poly_txt}.')

big_poly = input("Enter coefficients of polynomial to be divided:  ")
big_poly = prep_poly(big_poly)

rrts = rational_root_theorem(big_poly)

print(f'possible roots exist at the following rational values {rrts}.')

test_rat_roots = input('Would you like to test all of them? [Y/n] ')

test_rat_roots = test_rat_roots.split()

if len(test_rat_roots) != 0 and test_rat_roots[0] != 'y':
    small_poly = input("Enter coefficients of polynomial to divide into first polynomial.  Leave blank to exit: ")
    if small_poly == '':
        sys.exit()
    small_poly = prep_poly(small_poly)
    ans = poly_div(big_poly, small_poly)
    print_result(big_poly, small_poly, ans)

    sys.exit()

solns = {}
for rrt in rrts:
    ans = poly_div(big_poly, [1, -rrt])
    solns[rrt] = ans

for k,v in solns.items():
    divisor_txt = poly_in_text([1, -k])
    print_result(big_poly, [1, -k], v)

