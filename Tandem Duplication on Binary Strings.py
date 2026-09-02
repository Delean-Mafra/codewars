# https://www.codewars.com/kata/6a3e752f67d78e375f66d44c/train/python

def binary_duplication(s:str):
    if s=="01":
        return []
    dm_pilha=[]
    dm_ops=[]
    for dm_c in s:
        dm_pilha.append(dm_c)
        if len(dm_pilha)>=2 and dm_pilha[-1]==dm_pilha[-2]:
            dm_idx=len(dm_pilha)-2
            dm_ops.append((dm_idx,dm_idx+1))
            dm_pilha.pop()
        elif len(dm_pilha)>=4 and dm_pilha[-4:-2]==dm_pilha[-2:]:
            dm_idx=len(dm_pilha)-4
            dm_ops.append((dm_idx,dm_idx+2))
            dm_pilha.pop()
            dm_pilha.pop()
    if "".join(dm_pilha)=="01":
        return dm_ops[::-1]
    return None
