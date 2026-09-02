# https://www.codewars.com/kata/6a92adf37a5942e596d3e89f/train/python

import math
def surjections(n:int,k:int)->int:
    dm_total_sobrejecoes=0
    
    for dm_indice in range(k+1):
        dm_sinal=(-1)**(k-dm_indice)
        dm_combinacoes=math.comb(k,dm_indice)
        dm_potencia=dm_indice**n
        dm_total_sobrejecoes+=dm_sinal*dm_combinacoes*dm_potencia
        
    return dm_total_sobrejecoes
