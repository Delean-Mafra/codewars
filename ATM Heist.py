def maximum_thrill(atms):
    if not atms:
        return 0
    
    dm_ans = 0
    for dm_val in atms:
        dm_ans = max(dm_ans, 2 * dm_val)
        
    dm_max_diff = float('-inf')
    for dm_j, dm_val in enumerate(atms):
        if dm_max_diff != float('-inf'):
            dm_ans = max(dm_ans, dm_max_diff + dm_val + dm_j)
        dm_max_diff = max(dm_max_diff, dm_val - dm_j)
        
    dm_max_sum = float('-inf')
    for dm_j in range(len(atms) - 1, -1, -1):
        dm_val = atms[dm_j]
        if dm_max_sum != float('-inf'):
            dm_ans = max(dm_ans, dm_max_sum + dm_val - dm_j)
        dm_max_sum = max(dm_max_sum, dm_val + dm_j)
        
    return dm_ans



####  #   # 
#   # ## ## 
#   # # # # 
#   # #   # 
####  #   # 
