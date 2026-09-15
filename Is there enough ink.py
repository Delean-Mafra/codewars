def enough_ink(dm_image, *dm_args, **dm_kwargs):
    dm_total_r = 0
    dm_total_g = 0
    dm_total_b = 0
    for dm_row in dm_image:
        for dm_p in dm_row:
            dm_total_r += 255 - int(dm_p[0:2], 16)
            dm_total_g += 255 - int(dm_p[2:4], 16)
            dm_total_b += 255 - int(dm_p[4:6], 16)
    
    if len(dm_args) == 3:
        dm_r_tank, dm_g_tank, dm_b_tank = dm_args
    elif len(dm_args) == 1 and isinstance(dm_args[0], dict):
        dm_tank = dm_args[0]
        dm_r_tank = dm_tank.get('r', 0)
        dm_g_tank = dm_tank.get('g', 0)
        dm_b_tank = dm_tank.get('b', 0)
    elif 'r' in dm_kwargs and 'g' in dm_kwargs and 'b' in dm_kwargs:
        dm_r_tank = dm_kwargs['r']
        dm_g_tank = dm_kwargs['g']
        dm_b_tank = dm_kwargs['b']
    elif 'ink_tank' in dm_kwargs and isinstance(dm_kwargs['ink_tank'], dict):
        dm_tank = dm_kwargs['ink_tank']
        dm_r_tank = dm_tank.get('r', 0)
        dm_g_tank = dm_tank.get('g', 0)
        dm_b_tank = dm_tank.get('b', 0)
    else:
        return True
        
    return dm_total_r <= dm_r_tank and dm_total_g <= dm_g_tank and dm_total_b <= dm_b_tank
