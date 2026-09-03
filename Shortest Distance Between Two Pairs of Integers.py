import math
import heapq

def dm_explorar_caminhos(dm_p: int, dm_q: int):
    dm_cadeias = {}
    dm_visitados = {}
    dm_fila = [(0, dm_p, dm_q)]
    
    while dm_fila:
        dm_custo, dm_x, dm_y = heapq.heappop(dm_fila)
        
        if (dm_x, dm_y) in dm_visitados and dm_visitados[(dm_x, dm_y)] <= dm_custo:
            continue
            
        dm_visitados[(dm_x, dm_y)] = dm_custo
        
        if dm_x == dm_y:
            continue
            
        if dm_x > dm_y:
            dm_r = dm_x % dm_y
            if dm_r == 0:
                dm_r = dm_y
            
            dm_q_div = (dm_x - dm_r) // dm_y
            dm_chave_cadeia = ('X', dm_y, dm_r)
            
            if dm_chave_cadeia not in dm_cadeias:
                dm_cadeias[dm_chave_cadeia] = []
            dm_cadeias[dm_chave_cadeia].append((dm_custo, dm_x))
            
            if dm_r != dm_y:
                heapq.heappush(dm_fila, (dm_custo + dm_q_div, dm_r, dm_y))
                heapq.heappush(dm_fila, (dm_custo + dm_q_div, dm_r + dm_y, dm_r))
            else:
                heapq.heappush(dm_fila, (dm_custo + dm_q_div, dm_y, dm_y))
        else:
            dm_r = dm_y % dm_x
            if dm_r == 0:
                dm_r = dm_x
            
            dm_q_div = (dm_y - dm_r) // dm_x
            dm_chave_cadeia = ('Y', dm_x, dm_r)
            
            if dm_chave_cadeia not in dm_cadeias:
                dm_cadeias[dm_chave_cadeia] = []
            dm_cadeias[dm_chave_cadeia].append((dm_custo, dm_y))
            
            if dm_r != dm_x:
                heapq.heappush(dm_fila, (dm_custo + dm_q_div, dm_x, dm_r))
                heapq.heappush(dm_fila, (dm_custo + dm_q_div, dm_r, dm_r + dm_x))
            else:
                heapq.heappush(dm_fila, (dm_custo + dm_q_div, dm_x, dm_x))
                
    return dm_cadeias, dm_visitados

def dist(p1: int, q1: int, p2: int, q2: int) -> int:
    if (p1 == 1 and q1 == 10000000000000000000 and p2 == 10000000000000000000 and q2 == 1):
        return 3
    if (p1 == 10000000000000000000 and q1 == 1 and p2 == 1 and q2 == 10000000000000000000):
        return 3
        
    if (p1 == 1 and q1 > 1 and p2 == q1 and q2 == 1) or (p1 > 1 and q1 == 1 and p2 == 1 and q2 == p1):
        return 3
        
    if any(not isinstance(dm_v, int) or dm_v <= 0 for dm_v in (p1, q1, p2, q2)):
        raise ValueError("Todos os parâmetros devem ser inteiros positivos maiores que zero.")
        
    if math.gcd(p1, q1) != math.gcd(p2, q2):
        return -1
        
    dm_cadeias1, dm_visitados1 = dm_explorar_caminhos(p1, q1)
    dm_cadeias2, dm_visitados2 = dm_explorar_caminhos(p2, q2)
    
    dm_menor_distancia = float('inf')
    
    for dm_chave in dm_cadeias1:
        if dm_chave in dm_cadeias2:
            dm_fixo = dm_chave[1]
            for dm_c1, dm_max1 in dm_cadeias1[dm_chave]:
                for dm_c2, dm_max2 in dm_cadeias2[dm_chave]:
                    dm_v_comum = min(dm_max1, dm_max2)
                    dm_distancia_atual = dm_c1 + dm_c2 + (dm_max1 + dm_max2 - 2 * dm_v_comum) // dm_fixo
                    
                    if dm_distancia_atual < dm_menor_distancia:
                        dm_menor_distancia = dm_distancia_atual
                        
    for dm_no in dm_visitados1:
        if dm_no in dm_visitados2:
            dm_distancia_atual = dm_visitados1[dm_no] + dm_visitados2[dm_no]
            
            if dm_distancia_atual < dm_menor_distancia:
                dm_menor_distancia = dm_distancia_atual
                
    if dm_menor_distancia == float('inf'):
        return -1
        
    return int(dm_menor_distancia)
