import numpy as np

dig_op = {}

equals_spot = {}
equals_spot[-2] = 0
equals_spot[-3] = 0
equals_spot[-4] = 0
equals_spot['dont care'] = 0

def increm_dig_op_key(key, eq_spot):
    global dig_op
    if key in dig_op.keys():
        dig_op[key] += 1
    else:
        dig_op[key] = 1
    equals_spot[eq_spot] += 1
    
    


#3 numbers (max of one digit each.  equals falls at -3 -> 2 dig answer only)
for i in range(1,10):
    for j in range(i,10):
        for k in range(1,10):
            if i + j + k >= 10:
                increm_dig_op_key('111++', -3)
            if i + j - k >= 10:
                increm_dig_op_key('111++', -3)
            if i + j * k >= 10:
                increm_dig_op_key('111+*', -3)
            if i + j / k >= 10 and i + j / k == int(i + j / k):
                increm_dig_op_key('111+/', -3)
            

#2 numbers:  2 dig operating on 1 dig.  (equals falls at -4 -> 3 dig answer only.  valid for + and *)
for i in range(10,100):
    for j in range(1,10):
        if i + j >= 100:
            increm_dig_op_key('21+', -4)
        if i * j >= 100 and i * j < 1000:
            increm_dig_op_key('21*', -4)

#2 numbers:  2 dig operating on 2 dig.  (equals falls at -3 -> 2 dig answer only.  valid for + and -)
    for j in range(i,100):
        if i + j < 100:
            increm_dig_op_key('22+', -3)
        if i * j < 100:
            increm_dig_op_key('22*', -3)
 

#2 numbers:  3 dig operating on 1 dig.  (equals falls at -3 -> 2 dig answer only.  valid for - and /)
for i in range(100,1000):
    for j in range(1,10):
        if i - j < 100 and i - j >= 10:
            increm_dig_op_key('31-', -3)
        if i / j < 100 and i / j >= 10 and i / j == int(i / j):
            increm_dig_op_key('31/', -3)

#2 numbers:  3 dig operating on 2 dig.  (equals falls at -2 -> 1 dig answer only.  valid for - and /)
    for j in range(10,100):
        if i - j < 10:
            increm_dig_op_key('32-', -2)
        if i / j < 10 and i / j == int(i / j):
            increm_dig_op_key('32/', -2)

dig_op = {k: v for k, v in sorted(dig_op.items(), key=lambda item: item[1])}

tot = sum(dig_op.values())
dig_op_freq = {k: v / tot for k, v in dig_op.items()}

tot = sum(equals_spot.values())
equals_spot_freq = {k: v / tot for k, v in equals_spot.items()}

for k, v in dig_op_freq.items():
    print(k, '{:.1%}'.format(v))

for k, v in equals_spot_freq.items():
    print(k, '{:.1%}'.format(v))
    