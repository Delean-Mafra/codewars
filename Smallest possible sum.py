# https://www.codewars.com/kata/52f677797c461daaf7000740
import math

def solution(lst):
    return len(lst)*math.gcd(*lst)
