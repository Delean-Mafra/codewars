def find_it(seq: list[int]) -> int:
    dm_res = 0
    for dm_x in seq:
        dm_res ^= dm_x
    return dm_res
