# https://www.codewars.com/kata/5dd259444228280032b1ed2a/train/python

import math

def solve(s, g):
    if s % g != 0:
        return -1
    dm_k = s // g
    for dm_x in range(1, dm_k // 2 + 1):
        dm_y = dm_k - dm_x
        if math.gcd(dm_x, dm_y) == 1:
            return (dm_x * g, dm_y * g)
    return -1

