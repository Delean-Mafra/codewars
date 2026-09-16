def testit(dm_s):
    if not dm_s:
        return None
    dm_mapping = {'a': '1', 'b': '-', 'c': '*', 'd': '*'}
    dm_res = []
    for dm_i, dm_char in enumerate(dm_s):
        if dm_i > 0 and dm_s[dm_i - 1] == 'a' and dm_char == 'a':
            dm_res.append('+')
        dm_res.append(dm_mapping.get(dm_char, dm_char))
    dm_val = eval("".join(dm_res))
    if dm_val <= 0:
        return dm_val
    return (dm_val + 1) // 2
