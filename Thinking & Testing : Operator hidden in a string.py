def testit(dm_s):
    if not dm_s or len(dm_s) % 2 == 0:
        return None
    
    dm_expr = []
    for dm_i, dm_char in enumerate(dm_s):
        dm_val = ord(dm_char) - 96
        if dm_i % 2 == 0:
            dm_expr.append(str(dm_val))
        else:
            dm_op = dm_val % 4
            if dm_op == 1:
                dm_expr.append('+')
            elif dm_op == 2:
                dm_expr.append('-')
            elif dm_op == 3:
                dm_expr.append('*')
            else:
                dm_expr.append('/')
                
    dm_res = eval("".join(dm_expr))
    return int(dm_res) if isinstance(dm_res, float) and dm_res.is_integer() else dm_res
