import numpy as np

import csv

import math

from datetime import datetime

from scipy.io.matlab.miobase import arr_dtype_number

from collections import Counter

import importlib

import copy

def solveQuadratic(a, b, c, posOnly = True):

    pos_n = (-b + math.sqrt(b**2 - 4*a*c))/(2*a)

    ans = [pos_n]

    if not posOnly:
        neg_n = (-b - math.sqrt(b**2 - 4*a*c))/(2*a)
        ans.append(neg_n)
    
    return ans


def isTriangular(ans):

    ans = abs(ans)

    #ans = n(n+1)/2

    a = 1
    b = 1
    c = -2 * ans

    pos_n = solveQuadratic(a, b, c)[0]
    
    return pos_n % 1 == 0

def isSquare(ans):

    ans = abs(ans)

    return math.sqrt(ans) % 1 == 0

def isPentagonal(ans):

    #ans = n(3n-1)/2

    a = 3
    b = -1
    c = -2*ans

    pos_n = solveQuadratic(a, b, c)[0]
    
    return pos_n % 1 == 0

def isHexagonal(ans):

    # these are a subset of triangulars.  will need to figure how to leverage this.

    #ans = n(2n-1)

    a = 2
    b = -1
    c = -ans

    pos_n = solveQuadratic(a, b, c)[0]
    
    return pos_n % 1 == 0

def isHeptagonal(ans):

    #ans = n(5n-3)/2

    a = 5
    b = -3
    c = -2*ans

    pos_n = solveQuadratic(a, b, c)[0]
    
    return pos_n % 1 == 0

def isOctagonal(ans):

    #ans = n(3n-2)

    a = 3
    b = -2
    c = -ans

    pos_n = solveQuadratic(a, b, c)[0]
    
    return pos_n % 1 == 0

def csv_to_np_array_multi_line(file_nm_with_path):

    with open(file_nm_with_path, newline='') as f:
        reader = csv.reader(f)
        data = [tuple(row) for row in reader]
    
    return data


def csv_to_np_array(file_nm_with_path, delim = ','):

    return np.genfromtxt(file_nm_with_path, delimiter=delim)


def isPrime(n):
    
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def append_primes_up_to_n(n, primes):

    # "primes" is a dictionary with the primes in the keys

    upper_lim = int(math.sqrt(n))+1

    p = max(primes.keys()) + 2

    if p % 2 == 0:
        p -= 1

    if p < 2:
        p = 2

    numisprime = True

    # find next prime above current list, up to n

    while p <= n:

        numisprime = True

        for prime in primes.keys():

            if p % prime == 0:
                numisprime = False
                break

            if prime > math.sqrt(p):
                break

        if numisprime:
            break

        p += 2

    if not numisprime:
        return primes

    primesnew = np.arange(p,n,2)

    for prime in primes.keys():
        if prime > upper_lim:
            break
        primesnew = primesnew[primesnew[:] % prime != 0]
    
    while primesnew.shape[0] > 0:

        primes[primesnew[0]] = None
        primesnew = primesnew[primesnew[:] % primesnew[0] != 0]

        if primesnew.shape[0] > 0:
            if primesnew[0] > upper_lim:
                arr_dict = dict.fromkeys(primesnew)
                primes = {**primes, **arr_dict}
                break

    return primes

def numDenom(n):

    x = abs(n)

    tol = 1e-8
    
    maxiter = 1e6

    wholeNumPart = int(x)
    
    x %= 1
    
    a = 0
    b = 1
    c = 1
    d = 1
    
    p = a + c
    q = b + d
    
    t = p / q
    
    counter = 0
    
    while abs(x - t) / x > tol and counter < maxiter:
        
        counter += 1
        
        t = p / q

        if x == t:
            break

        if x > t:
        
            a = p
            b = q

        else:
            c = p
            d = q
        
        p = a + c
        q = b + d

    p += q * wholeNumPart
    
    return  {

            'num': p, 
            'denom': q,
            'iter':  counter
            }

def get_integer_reverse(n):

    n = int(n)
    n_str = str(n)
    n_rev = n_str[::-1]

    return int(n_rev)

def isPalindrome(n):

    n = int(n)
    n_str = str(n)
    n_rev = n_str[::-1]

    n_rev = int(n_rev)
    
    return n == n_rev 

def int_from_array_of_digits(arr):
    p = len(arr)
    num = 0
    for a in arr:
        p -= 1
        num += a * 10 ** p
    return int(num)

def array_of_digits_from_int(num):

    # arr = np.asarray([num])
    # arr = arr.astype(float)
    # b = 10                                                   # Base, in our case 10, for 1, 10, 100, 1000, ...
    # n = np.ceil(np.max(np.log(arr) / np.log(b))).astype(float)   # Number of digits
    # d = np.arange(n)                                         # Divisor base b, b ** 2, b ** 3, ...
    # d.shape = d.shape + (1,) * (arr.ndim)                      # Add dimensions to divisor for broadcasting
    # arr = arr // b ** d % b

    # arr = arr.T
    # arr = np.flip(arr, axis = 1)

    digs = int(math.log10(num))+1

    arr = np.zeros(digs)

    for i in range(digs-1,-1,-1):
        arr[i] = num % (10)
        num = int(num / 10)
        

    return arr

def array_of_digits_from_array_of_ints(arr = [], dict_keys = {}, truncate_extra_row_at_bottom = False):

    if len(arr) == 0:
        arr = np.asarray(list(dict_keys))

    if truncate_extra_row_at_bottom:
        arr = arr[:-1]

    b = 10                                                   # Base, in our case 10, for 1, 10, 100, 1000, ...
    n = np.ceil(np.max(np.log(arr) / np.log(b))).astype(int)   # Number of digits
    d = np.arange(n)                                         # Divisor base b, b ** 2, b ** 3, ...
    d.shape = d.shape + (1,) * (arr.ndim)                      # Add dimensions to divisor for broadcasting
    arr = arr // b ** d % b

    arr = arr.T
    arr = np.flip(arr, axis = 1)

    return arr

def quadrat_pos_neg(a, b, c):

    pos = (-b + math.sqrt(b**2 - 4*a*c)) / 2 / a
    neg = (-b - math.sqrt(b**2 - 4*a*c)) / 2 / a

    return pos, neg

def isPrime_on_the_go(n):

    n = int(n)

    if n % 2 == 0:
        return False

    primes = {}
    prime_test = 1
    while prime_test + 2 <= math.sqrt(n):
        prime_test += 2
        pr_test_list = [prime_test % prime != 0 for prime in primes.keys()]
        if all(pr_test_list):
            primes[prime_test] = None
        else:
            continue
        if n % prime_test == 0:
            return False
        
    
    return True

def get_binary_representation_default_as_string_optional_as_array(n, get_array = False):
    numdigs = int(math.log2(n))+1

    binarr = np.zeros(numdigs)
    binarr = binarr.astype(int)

    while n >= 1:
        digplc = int(math.log2(n))
        binarr[digplc] = 1
        n -= 2**digplc
    
    bin_ans = np.flip(binarr)

    if not get_array:
        bin_ans = ''.join(map(str,bin_ans))

    return bin_ans


def primefactorization_on_the_go(n):

    #find primes and factors at same time:

    n = int(n)

    factors = []
    primes = {}
    sz = n / 2
    if sz % 1 != 0:
        sz += 1
    sz = int(sz)
    arr = np.zeros(sz)
    arr[0] = 2
    arr[1:] = np.arange(3, n + 1, 2)
    arr = arr.astype(int)

    i = 0
    
    while n > 1 and arr[i] <= n:
        if n % arr[i] != 0:
            i += 1
        isPrime = True
        for prime in primes.keys():
            if arr[i] % prime == 0 and arr[i] != prime:
                isPrime = False
                break
        if isPrime and n % arr[i] == 0:
            factors.append(arr[i])
            primes[arr[i]] = None
            n /= arr[i]

    return factors
        
def primes_up_to_n_primesindictkeys(n, val = None):

    #iterate over primes with 'iter in your_variable.keys()'

    n = int(n)

    upper_lim = int(math.sqrt(n))+1

    primes = {}
    # primes = []
    sz = n / 2
    if sz % 1 != 0:
        sz += 1

    sz = int(sz)

    arr = np.zeros(sz)

    arr[0] = 2

    arr[1:] = np.arange(3, n + 1, 2)

    arr = arr.astype(int)

    while arr.shape[0] > 0:

        primes[arr[0]] = val
        # primes.append(arr[0])
        arr = arr[arr[:] % arr[0] != 0]

        if arr.shape[0] > 0:

            if arr[0] > upper_lim:
                arr_dict = dict.fromkeys(arr)
                primes = {**primes, **arr_dict}
                break

    
    # delete = [key for key in primes if key > n]

    # for key in delete: 
    #     del primes[key] 

    return primes


def numberofprimesbelown(n):

    return n / math.log(n)


def firstnprimes(n):

    primes = []

    primes.append(2)

    p = 3

    count = 1

    while count < n:

        numisprime = False

        while not numisprime:

            numisprime = True

            for prime in primes:

                if p % prime == 0:

                    numisprime = False

                    break

            if numisprime:

                primes.append(p)

                count += 1

            p += 2

    return primes

def getnextprime(primes = {}):

    # "primes" is a dictionary with the primes in the keys

    if len(primes) == 0 or max(primes.keys()) == 1:
        return 2

    if max(primes.keys()) == 2:
        return 3

    p = max(primes.keys()) + 2

    if p % 2 == 0:
        p += 1

    numisprime = False

    while not numisprime:

        numisprime = True

        for prime in primes.keys():

            if p % prime == 0:

                numisprime = False

                break

        if numisprime:
            break

        p += 2

    return p


def ncr(n, r):

    return math.factorial(n) / math.factorial(n - r) / math.factorial(r)


def numberwithpprimesbelowit(p):

    y1 = 30

    x1 = numberofprimesbelown(y1)

    y2 = 100

    x2 = numberofprimesbelown(y2)

    m = (y2 - y1) / (x2 - x1)

    b = y1 - m * x1

    initguess = m * p + b

    value = numberofprimesbelown(initguess) - p

    x0 = initguess

    x1 = x0 + 1

    while abs(value) > 0.01:

        y0 = numberofprimesbelown(x0) - p

        y1 = numberofprimesbelown(x1) - p

        x2 = x1 - y1 * (x1 - x0) / (y1 - y0)

        x0 = x1

        x1 = x2

        value = numberofprimesbelown(x2) - p

    return x2


def nfromsn(sn):

    n = (-1 + math.sqrt(1 + 8 * sn)) / 2

    return n


def istriangular(sn):
    n = (-1 + math.sqrt(1 + 8 * sn)) / 2
    return n % 1 == 0


def npnfromsn(sn):

    n = (-1 + np.sqrt(1 + 8 * sn)) / 2

    return n


def nfromsnisinteger(sn):

    if nfromsn(sn) % 1 == 0:

        return True

    return False


def sumofnatnumsbelown(n):

    return n * (n + 1) / 2


def npr(n, r):

    return math.factorial(n) / math.factorial(n - r)


def permuteutil(sstr, count, result, level, resultlist=[]):

    if (level == len(result)):

        resultlist.append(result[:])

        return None

    for i in range(len(sstr)):

        if (count[i] == 0):

            continue

        result[level] = sstr[i]

        count[i] -= 1

        permuteutil(sstr, count, result, level + 1, resultlist)

        count[i] += 1


def permute(sstr, count, result, level, resultlist=[]):

    if (level == len(result)):

        resultlist.append(result[:])

#         print(count, result[:])

        return resultlist

    for i in range(len(sstr)):

        if (count[i] == 0):

            continue

        result[level] = sstr[i]

        count[i] -= 1

        resultlist = permute(sstr, count, result, level + 1, resultlist)

        count[i] += 1

    return resultlist

# sstr = '117649'
# count = [1,1,1,1,1,1]
# result = [0,0,0,0,0,0]
# level = 0

# print(permute(sstr, count, result, level, []))


def permute_dict_keys(sstr, iter = 0, count = [], result = [], level=0,  result_dict = {}, mod_dot_fxn_to_call = ""):

    if iter == 0:
        # having issues with arguments called by reference.  
        sstr = str(sstr)
        count = []
        result = []
        for _ in range(len(sstr)):
            count.append(1)
            result.append(0)

    if (level == len(result)):

        key = ''.join(result)

#         print(count, result[:])

        result_dict[key] = result

        if len(mod_dot_fxn_to_call) > 0:
            mod_name, func_name = mod_dot_fxn_to_call.rsplit('.',1)
            mod = importlib.import_module(mod_name)
            func = getattr(mod, func_name)
            if not func(key):
                result_dict.pop(key)
            
        return copy.deepcopy(result_dict)

    for i in range(len(sstr)):

        if (count[i] == 0):

            continue

        result[level] = sstr[i]

        count[i] -= 1

        result_dict = permute_dict_keys(sstr, iter + 1, count[:], result[:], level + 1, copy.deepcopy(result_dict), mod_dot_fxn_to_call)

        count[i] += 1

    return result_dict

# notes - info below was the original method to launch a permutation.  
# it has been absorbed into the function such that only the string/number to be permuted 
# is needed (this can be an int or a string).

# sstr = str('123456')
# count = []
# result = []
# level = 0
# for _ in range(len(sstr)):
#     count.append(1)
#     result.append(0)

# perms = permute_dict_keys(sstr, count, result, level)

# print(perms)

# a = permute_dict_keys(410636254)

# print(a)

def permuteandtest(sstr, count, result, level, primes, r, resultlist=[], minanswer=-1, summer=[], allresults=[]):

    if (level == len(result)):

        #         print(result)

        thesum = np.sum(np.array(result))

        summer.append(thesum)

        if thesum == r:

            answer = np.power(primes, result)

            answer = np.prod(answer)

            nval = nfromsn(answer)

            if nval % 1 == 0:

                alltheprimes = []
                prime = -1
                for r in result:
                    prime += 1
                    for rin in range(r):
                        alltheprimes.append(primes[prime])

                numdivs = numdivisors(primes=alltheprimes)

                if numdivs > 500:

                    if minanswer == -1:

                        minanswer = answer

                    if answer < minanswer:

                        minanswer = answer

                    allresults.append(result[:])

                    print("answer:  ", answer, "minanswer:  ", minanswer)

        return resultlist

    for i in range(len(sstr)):

        if (count[i] == 0):

            continue

        result[level] = sstr[i]

        count[i] -= 1

        resultlist = permuteandtest(
            sstr, count, result, level + 1, primes, r, resultlist, minanswer, summer, allresults)

        count[i] += 1

    return resultlist


def printallrows(arr):

    for row in arr:

        print(row)

    return None


def writetocsv(arr, name=''):

    arr = np.array(arr)

    name += '_' + str(datetime.now())

    name = name.replace(':', '_')

    name = name.replace('-', '_')

    name = name.replace(' ', '_')

    if name[-4:] != '.csv':

        name = name.replace('.', '_')

        name = name + '.csv'

    if name[:5] != 'data/':

        name = 'data/' + name

    np.savetxt(name, arr, delimiter=',')

    return None


def allpermutsoflist(sstr):

    count = []

    result = []

    for i in range(len(sstr)):

        count.append(1)

    prods = []

    for i in range(1, len(sstr) + 1):

        result = []

        for n in range(1, i + 1):

            result.append(0)

        resultlist = permute(sstr, count, result, 0)

        for currset in resultlist:

            prod = 1

#             print(currset)

            for num in currset:

                prod *= num

            prods.append(prod)

    return np.unique(prods)


def primefactors(n):

    primes = primes_up_to_n_primesindictkeys(n)

    primes = [*primes]

    orig = n

    primefacts = []

    i = 0
    while i < len(primes):
        
        if n % primes[i] == 0:

            primefacts.append(primes[i])

            n /= primes[i]

            i -= 1
        
        i += 1

    return primefacts

def divisorsandnumdivisors(n=-1, primes=[], r=-1):

    # provide either n or primes

    if len(primes) == 0:

        primes = primefactors(n)

    divs = []

    divs.append(1)

    for prime in primes:

        divs.append(prime)

    if n > 0:

        divs.append(n)

    divs = allcombos(divs, r)

    divs = np.array(divs)

    maxval = n

    if maxval < 0:

        maxval = 1

        for prime in primes:

            maxval *= prime

    divs = divs[divs[:] <= maxval]

    return divs, divs.shape[0]


def numdivisors(n=-1, primes=[], r=-1):

    divs, numdivs = divisorsandnumdivisors(n, primes, r)

    return numdivs


def divisorsonly(n=-1, primes=[], r=-1):

    divs, numdivs = divisorsandnumdivisors(n, primes, r)

    return divs


#     arr[]  ---> Input Array

#    data[] ---> Temporary array to store current combination

#    start & end ---> Starting and Ending indexes in arr[]

#    index  ---> Current index in data[]

#    r ---> Size of a combination to be printed


def combinations(arr, data, start, end, index, r, combos=[]):

    #      Current combination is ready to be printed, print it

    if (index == r):

        combos.append(data[:])

#         print("combo: ", data)

        return combos[:]


#     replace index with all possible elements. The condition

# end-i+1 >= r-index" makes sure that including one element

# at index will make a combination with remaining elements

# at remaining positions

    for i in range(start, end):

        if end - i + 1 >= r - index:

            data[index] = arr[i]

            combos = combinations(

                arr, data, i + 1, end, index + 1, r, combos[:])

    return combos


def allcombos(sstr, r=-1):

    rmaxnoti = True

    if r == -1:

        rmaxnoti = False

    result = []

    prods = []

    for i in range(1, len(sstr) + 1):

        result = []

        for n in range(1, i + 1):

            if rmaxnoti and n > r:

                break

            result = []

            for m in range(n):

                result.append(0)

            resultlist = combinations(sstr, result, 0, i, 0, n)

            for currset in resultlist:

                prod = 1

#                 print(currset)

                for num in currset:

                    prod *= num

                prods.append(prod)

    return np.unique(prods)


def findhightrinum():

    maxdivs = 0

    divparams = []

    writeheader = True

    n = 2079

    looping = True

    t0 = datetime.now()

    while looping:

        sn = sumofnatnumsbelown(n)

        _, numdivs = divisorsandnumdivisors(sn)

    #     print(numdivs)

        if numdivs > maxdivs:

            if numdivs > 500:

                looping = False

                print(datetime.now() - t0)

            maxdivs = numdivs

            divparams.append([n, sn, numdivs, maxdivs])

            with open('data/nvsnumdivs.csv', mode='a') as csv_file:

                fieldnames = ['n', 'sn', 'numdivs', 'maxdivs']

                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                if writeheader:

                    writer.writeheader()

                    writeheader = False

                writer.writerow({'n': n,

                                 'sn': sn,

                                 'numdivs': numdivs,

                                 'maxdivs': maxdivs})

        print(n, sn, numdivs, maxdivs)

        n += 1

    print("end")

    return None


# Print all members of ar[] that have given

def findNumbers(ar, sum, i, res=[], r=[]):

    # If  current sum becomes negative

    if sum < 0:

        return None

    # if we get exact answer

    if sum == 0:

        res.append(r[:])

        return res

    # Recur for all remaining elements that

    # have value smaller than sum.

    while (i < len(ar) and sum - ar[i] >= 0):

         # Till every element in the array starting

         # from i which can contribute to the sum

        r.append(ar[i])

        # recur for next numbers

        res = findNumbers(ar, sum - ar[i], i, res, r)

        i += 1

        # remove number from list (backtracking)

        r.pop()

    return res


# Returns all combinations of ar[] that have given

# sum.

def combinationSum(ar, sum):

    # sort input array

    ar.sort

    # remove duplicates

    ar = list(dict.fromkeys(ar))

    res = findNumbers(ar, sum, 0)

    return res


def gettotalsofeachnum(ar, sum):

    res = []

    res = combinationSum(ar, sum)

    counts = []

    for r in res:

        countdict = Counter(r)

        count = []

        for i in range(len(ar) + 1):
            count.append(0)

        for key, value in countdict.items():
            if key <= sum:
                count[key] = value
            else:
                print("stopper")

#         print(count)

        counts.append(count)

    return counts


def tester():

    ar = [1, 2, 3, 4, 5]

    # for i in range(ar):

    #    n.append(0)

    sum = 5  # set value of sum

    res = combinationSum(ar, sum)

    return res


def usencrtofindhightri():

    n = 0

    keeplooping = True

    answers = []

    while keeplooping:

        n += 1

        primes = np.array(firstnprimes(n))

        primes= np.flip(primes)

        result = []

        for i in range(n):

            result.append(0)

        for r in range(1, n + 1):

            #             if ncr(n, r) > 500:

            if ncr(n, r) > 500:

                print("npr: ", npr(n, r))

                print("ncr: ", ncr(n, r))

                if ncr(n, r) == 715.0:
                    print("stopper")

                inputnums = np.arange(r + 1)
                inputnumsnozero = np.arange(1, r + 1)
                counts = gettotalsofeachnum(inputnumsnozero, r)

                for count in counts:

                    count[0] = n - r + count.count(0) - 1

                    exponentpermutations = np.array(permuteandtest(
                        inputnums, count, result, 0, primes, r, [], -1,))

                    if exponentpermutations.shape[0] > 0:

                        print("primes: ", primes)

                        print("exponents: ", exponentpermutations)

                        primeraisedtopermutation = np.power(
                            primes, exponentpermutations)

                        print("primeraisedtopermutation: ",
                              primeraisedtopermutation)

                        prods = np.prod(primeraisedtopermutation, axis=1)

                        nsfromsn = npnfromsn(prods)

                        nsfromsn = nsfromsn[nsfromsn[:] % 1 == 0]

                        if nsfromsn.shape[0] > 0:

                            divs = np.apply_along_axis(
                                func1d=numdivisors, axis=0, arr=prods)

                            if divs.shape != ():

                                prods = prods[divs[:] > 500]

                                answers.append(np.min(prods))

    return None


def incrementprimecombinations(primes=[2], exponents=[1]):
    primes = [2]
    exponents = [1]

    currval = np.prod(np.power(primes, exponents))

    if istriangular(currval):
        expincr = np.array(exponents) + 1
        if np.prod(expincr) > 500:
            return currval

    keeplooping = True

    while keeplooping:

        newvals = []
        for i in range(len(exponents)):
            exponents[i] += 1
            a = np.prod(np.power(primes, exponents))
            newvals.append([i, a])
            exponents[i] -= 1
            minval = newvals[0]
            for newval in newvals:
                if newval[1] < minval[1]:
                    minval = newval
            newval1 = minval

        a = getnextprime(primes)
        primes.append(a)
        exponents.append(1)

        newval2 = np.prod(np.power(primes, exponents))

        newval = -1
        if newval1[1] < newval2:
            exponents[newval1[0]] += 1
            newval = newval1[1]
            primes.pop()
            exponents.pop()
        else:
            newval = newval2

        if istriangular(newval):
            expincr = np.array(exponents) + 1
            if np.prod(expincr) > 500:
                return newval


# incrementprimecombinations()

def testingdivs():

    keeplooping = True
    primes = [2]
    answers = []
    while keeplooping:
        expprod = 1
        for prime in primes:
            prod = prime
            for exponent in range(len(primes)):
                expprod *= exponent
                a = math.pow(prime, exponent)
                prod *= a
                print("prime: ", prime, "exponent: ", exponent,
                      "prime**exponent: ", a, "prod: ", prod, "expprod: ", expprod)

                if expprod > 500:
                    if istriangular(prod):
                        print(prod, " works!")
                        answers.append(prod)

        primes.append(getnextprime(primes))

    return answers


# testingdivs()


def integersqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def useintegersqrttodetermineifnumistriangular(sn):
    discriminant = integersqrt(1 + 8 * sn)
    n = (-1 + discriminant) / 2

    return n * (n + 1) / 2 == sn


def testingdivs2():

    n = 500

    primes = primefactors(n)

    print("primes:  ", primes)

    divs1, numdivs1 = divisorsandnumdivisors(n=n)

    divs2, numdivs2 = divisorsandnumdivisors(primes=primes)

    print("n-based:  ", divs1, numdivs1)

    print("primes-based:  ", divs2, numdivs2)

    return None


def testingdivs3():

    # all numbers can be written as composites of primes, each to a given exponent
    # number of divisors = products of each (exponent + 1)
    # add a prime.
    # try all permutations of the primes and powers up to that number of primes
    # check which value is triangular and has divisors > 500
    # this took ~2 min to find a matching result, so it doesn't technically qualify
    # also, I don't know a way to definitively say that this answer is the best.
    # only by entering each returned value until one of them was correct was I
    # able to consider this solved

    minval = -1

    keeplooping = True

    primes = []

    answers = []

    while keeplooping:

        primes.append(getnextprime(primes))

        sstr = []

        count = []

        result = []

        for i in range(len(primes)):
            sstr.append(i)

            count.append(len(primes))

            result.append(0)

        exponentslist = permute(sstr, count, result, 0, [])

        for exponents in exponentslist:
            ans = np.prod(np.power(primes, exponents))

            numdivs = 1

            for exponent in exponents:
                numdivs *= (exponent + 1)

#             print(ans, numdivs)

            if ans > 0 and numdivs > 500 and useintegersqrttodetermineifnumistriangular(ans):
                if minval == -1:
                    minval = ans
                    answers.append(ans)
                    print(ans)
                else:
                    if ans < minval:
                        minval = ans
                        print(ans)
                        answers.append(ans)
                        if len(answers) % 10 == 0:
                            print(answers)
                            print()

    return None
