import numpy as np
import pandas as pd
from itertools import permutations
from random import randint

# testing that the first x characters of the set of all permutations contain all possible permutations of the
# characters given the shorter length
# 
# this started as a test of a 4-character string and a 2-character subset.  
# abstracted now such that "perms_2" reflects a subset and "perms_4" reflects a whole set  

sstr = '123456789'

for i in range(1,len(sstr)+1):
    for j in range(1, i):
        small_cols = list(np.arange(j))
        bigger_cols = list(np.arange(i))
        
        perms_2 = permutations(sstr,j)
        perms_2_list = []
        for perm in perms_2:
            perms_2_list.append(perm)
        perms_2_df = pd.DataFrame(list(perms_2_list), columns = small_cols)
        perms_2_df[small_cols] = np.sort(perms_2_df[small_cols].values)
        perms_2_df = perms_2_df.sort_values(small_cols)
        perms_2_df = perms_2_df.drop_duplicates()
        perms_2_np = perms_2_df.to_numpy()

        perms_4 = permutations(sstr, i)
        perms_4_list = []
        for perm in perms_4:
            perms_4_list.append(perm)
        perms_4_df = pd.DataFrame(list(perms_4_list), columns = bigger_cols)
        perms_4_arr_first_2_cols_df = pd.DataFrame(perms_4_df, columns = small_cols)
        perms_4_arr_first_2_cols_df[small_cols] = np.sort(perms_4_arr_first_2_cols_df[small_cols].values)
        perms_4_arr_first_2_cols_df = perms_4_arr_first_2_cols_df.sort_values(small_cols)
        perms_4_arr_first_2_cols_df = perms_4_arr_first_2_cols_df.drop_duplicates()
        perms_4_arr_first_2_cols_np = perms_4_arr_first_2_cols_df.to_numpy()

        try:
            if not np.array_equal(perms_2_np, perms_4_arr_first_2_cols_np):
                if len(perms_4_arr_first_2_cols_np) != len(perms_2_np):
                    a = 1
                for i in len(perms_2_np.shape[0]):
                    print(f'2: {perms_2_np[i]}. 4: {perms_4_arr_first_2_cols_np[i]}.')
        except Exception as e:
            print(i, e.__cause__)
            break