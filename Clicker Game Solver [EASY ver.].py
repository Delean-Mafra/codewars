# https://www.codewars.com/users/Delean-Mafra/completed_solutions#:~:text=Clicker%20Game%20Solver%20%5BEASY%20ver.%5D

def clicker_solver(up: int, goal: int) -> int:
    if goal == 0:
        return 0
    if up == 0:
        return -1

    dm_cpc_atual = up
    dm_total_cliques_upgrades = 0
    dm_minimo_cliques_total = float('inf')

    while True:
        dm_cliques_para_meta = (goal + dm_cpc_atual - 1) // dm_cpc_atual
        dm_total_cliques_simulados = dm_total_cliques_upgrades + dm_cliques_para_meta
        
        if dm_total_cliques_simulados < dm_minimo_cliques_total:
            dm_minimo_cliques_total = dm_total_cliques_simulados

        dm_custo_proximo_up_cliques = dm_cpc_atual**2 + 1

        if dm_total_cliques_upgrades + dm_custo_proximo_up_cliques >= dm_minimo_cliques_total:
            break

        dm_total_cliques_upgrades += dm_custo_proximo_up_cliques
        dm_cpc_atual += up

    return dm_minimo_cliques_total
