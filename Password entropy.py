import math

def entropy(password: str) -> float:
    dm_r = 0
    if any('a' <= dm_c <= 'z' for dm_c in password):
        dm_r += 26
    if any('A' <= dm_c <= 'Z' for dm_c in password):
        dm_r += 26
    if any('0' <= dm_c <= '9' for dm_c in password):
        dm_r += 10
    if any(dm_c in '''!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~''' for dm_c in password):
        dm_r += 32
        
    return len(password) * math.log2(dm_r)
