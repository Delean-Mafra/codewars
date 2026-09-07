def calculate(rectangles):
    if not rectangles:
        return 0
        
    dm_eventos = []
    dm_ys_set = set()
    
    for dm_r in rectangles:
        dm_x0, dm_y0, dm_x1, dm_y1 = dm_r
        if dm_x0 >= dm_x1 or dm_y0 >= dm_y1:
            continue
        dm_eventos.append((dm_x0, 1, dm_y0, dm_y1))
        dm_eventos.append((dm_x1, -1, dm_y0, dm_y1))
        dm_ys_set.add(dm_y0)
        dm_ys_set.add(dm_y1)
        
    if not dm_eventos:
        return 0
        
    dm_ys = sorted(list(dm_ys_set))
    dm_y_idx = {dm_y: dm_i for dm_i, dm_y in enumerate(dm_ys)}
    dm_m = len(dm_ys) - 1
    
    dm_count = [0] * (4 * dm_m + 1)
    dm_length = [0] * (4 * dm_m + 1)
    
    def dm_atualizar(dm_no, dm_esq, dm_dir, dm_q_esq, dm_q_dir, dm_valor):
        if dm_q_esq > dm_dir or dm_q_dir < dm_esq:
            return
            
        if dm_q_esq <= dm_esq and dm_dir <= dm_q_dir:
            dm_count[dm_no] += dm_valor
        else:
            dm_meio = (dm_esq + dm_dir) // 2
            dm_atualizar(dm_no * 2, dm_esq, dm_meio, dm_q_esq, dm_q_dir, dm_valor)
            dm_atualizar(dm_no * 2 + 1, dm_meio + 1, dm_dir, dm_q_esq, dm_q_dir, dm_valor)
            
        if dm_count[dm_no] > 0:
            dm_length[dm_no] = dm_ys[dm_dir + 1] - dm_ys[dm_esq]
        elif dm_esq != dm_dir:
            dm_length[dm_no] = dm_length[dm_no * 2] + dm_length[dm_no * 2 + 1]
        else:
            dm_length[dm_no] = 0

    dm_eventos.sort(key=lambda dm_e: dm_e[0])
    
    dm_area_total = 0
    dm_x_anterior = dm_eventos[0][0]
    
    for dm_x, dm_tipo, dm_y0, dm_y1 in dm_eventos:
        dm_area_total += (dm_x - dm_x_anterior) * dm_length[1]
        dm_atualizar(1, 0, dm_m - 1, dm_y_idx[dm_y0], dm_y_idx[dm_y1] - 1, dm_tipo)
        dm_x_anterior = dm_x
        
    return dm_area_total
