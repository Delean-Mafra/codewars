# https://www.codewars.com/kata/556021360863a1708900007b/train/python
def check_valid_tr_number(number):
    dm_s=str(number) if not isinstance(number,str) else number
    if not dm_s.isdigit() or len(dm_s)!=11 or dm_s[0]=='0':
        return False
    dm_d=[int(dm_c) for dm_c in dm_s]
    dm_impar=dm_d[0]+dm_d[2]+dm_d[4]+dm_d[6]+dm_d[8]
    dm_par=dm_d[1]+dm_d[3]+dm_d[5]+dm_d[7]
    if (dm_impar*7-dm_par)%10!=dm_d[9]:
        return False
    if sum(dm_d[:10])%10!=dm_d[10]:
        return False
    return True
