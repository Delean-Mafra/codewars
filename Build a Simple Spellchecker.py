def dl_distance(dm_s1, dm_s2):
    dm_len1, dm_len2 = len(dm_s1), len(dm_s2)
    if abs(dm_len1 - dm_len2) > 2:
        return 3
    if dm_s1 == dm_s2:
        return 0
        
    dm_da = {}
    dm_maxdist = dm_len1 + dm_len2
    
    dm_d = [[0] * (dm_len2 + 2) for _ in range(dm_len1 + 2)]
    
    dm_d[0][0] = dm_maxdist
    for dm_i in range(dm_len1 + 1):
        dm_d[dm_i+1][0] = dm_maxdist
        dm_d[dm_i+1][1] = dm_i
    for dm_j in range(dm_len2 + 1):
        dm_d[0][dm_j+1] = dm_maxdist
        dm_d[1][dm_j+1] = dm_j
        
    for dm_i in range(1, dm_len1 + 1):
        dm_db = 0
        dm_char_a = dm_s1[dm_i-1]
        for dm_j in range(1, dm_len2 + 1):
            dm_char_b = dm_s2[dm_j-1]
            dm_k = dm_da.get(dm_char_b, 0)
            dm_l = dm_db
            
            if dm_char_a == dm_char_b:
                dm_cost = 0
                dm_db = dm_j
            else:
                dm_cost = 1
                
            dm_d[dm_i+1][dm_j+1] = min(
                dm_d[dm_i][dm_j] + dm_cost,
                dm_d[dm_i+1][dm_j] + 1,
                dm_d[dm_i][dm_j+1] + 1,
                dm_d[dm_k][dm_l] + (dm_i - dm_k - 1) + 1 + (dm_j - dm_l - 1)
            )
        dm_da[dm_char_a] = dm_i
        
    return dm_d[dm_len1+1][dm_len2+1]

def dm_apply_case(dm_missp, dm_corr):
    dm_letters = [dm_c for dm_c in dm_missp if dm_c.isalpha()]
    dm_is_all_upper = (len(dm_letters) > 0) and all(dm_c.isupper() for dm_c in dm_letters)
    
    if dm_is_all_upper and len(dm_missp) > 1:
        return dm_corr.upper()
        
    if len(dm_missp) == 1:
        if dm_missp[0].isupper():
            return dm_corr[0].upper() + dm_corr[1:].lower()
        else:
            return dm_corr.lower()
            
    dm_res = []
    for dm_i, dm_c in enumerate(dm_corr):
        if dm_i < len(dm_missp) and dm_missp[dm_i].lower() == dm_c.lower():
            if dm_missp[dm_i].isupper():
                dm_res.append(dm_c.upper())
            else:
                dm_res.append(dm_c.lower())
        else:
            dm_res.append(dm_c.lower())
            
    return "".join(dm_res)

def correct_spelling(text, word_list):
    dm_word_set = set(word_list)
    dm_tokens = text.split()
    dm_results = {}
    
    for dm_token in dm_tokens:
        dm_start = 0
        while dm_start < len(dm_token) and not dm_token[dm_start].isalpha():
            dm_start += 1
        dm_end = len(dm_token) - 1
        while dm_end >= dm_start and not dm_token[dm_end].isalpha():
            dm_end -= 1
            
        if dm_start > dm_end:
            continue
            
        dm_core = dm_token[dm_start:dm_end+1]
        
        if dm_core.lower() in dm_word_set:
            continue
            
        if dm_core not in dm_results:
            dm_dist1 = []
            dm_dist2 = []
            
            dm_core_lower = dm_core.lower()
            
            for dm_w in dm_word_set:
                dm_dist = dl_distance(dm_core_lower, dm_w)
                if dm_dist == 1:
                    dm_dist1.append(dm_w)
                elif dm_dist == 2:
                    dm_dist2.append(dm_w)
                    
            dm_chosen = dm_dist1 if dm_dist1 else dm_dist2
            dm_cased = sorted(list(set(dm_apply_case(dm_core, dm_w) for dm_w in dm_chosen)))
            dm_results[dm_core] = dm_cased
            
    return dm_results


"""
████  █████ █     █████  ███  █   █    █   █  ███  █████ ████   ███             ████  █   █   
█░░░█ █░░░░░█░    █░░░░░█ ░░█ ██  █░   ██ ██░█ ░░█ █░░░░░█░░░█ █ ░░█            █░░░█ ██ ██░  
█░░░█░████░░█░░   ████░░█████░█░█ █░░  █░█ █░█████░████░░████░░█████░   ████    █░░░█░█░█ █░░ 
█░░ █░█░░░░ █░░   █░░░░ █░░░█░█░░██░░  █░░░█░█░░░█░█░░░░ █░░█░ █░░░█░░   ░░░░   █░░ █░█░░░█░░ 
████ ░█████░█████ █████░█░░░█░█░░ █░░  █░░ █░█░░░█░█░░░░░█░░░█░█░░░█░░    ░░░░  ████ ░█░░ █░░ 
 ░░░░ ░░░░░░ ░░░░░ ░░░░░ ░░  ░░░░  ░░   ░░  ░░░░  ░░░░    ░░  ░ ░░  ░░           ░░░░ ░░░  ░░ 
  ░░░░  ░░░░░ ░░░░░ ░░░░░ ░   ░ ░   ░    ░   ░ ░   ░ ░     ░   ░ ░   ░            ░░░░  ░   ░ 
"""

