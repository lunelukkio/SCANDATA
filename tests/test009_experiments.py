# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:05:53 2022

lunelukkio@gmail.com
"""

def key_num_checker(controller_dict):
    numeric_keys = [key for key in controller_dict.keys() if any(char.isdigit() for char in key)]
    numeric_values = [int(''.join(filter(str.isdigit, key))) for key in numeric_keys]

    # sort from a small number
    sorted_keys = [x for _, x in sorted(zip(numeric_values, numeric_keys))]

    # find unexsisting number
    min_missing_number = None
    for i in range(1, len(sorted_keys) + 2):
        if i not in numeric_values:
            min_missing_number = i
            break

    # new key
    return f"key{min_missing_number}"

dicta = {"Roi1":1, "Roi4":2}
print(key_num_checker(dicta))