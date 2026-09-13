def pattern(dm_n: int) -> str:
    if dm_n <= 0:
        return ""
    dm_nums = [str(dm_i) for dm_i in range(1, dm_n + 1)]
    dm_lens = [len(dm_s) for dm_s in dm_nums]
    dm_full_str = "".join(dm_nums)
    dm_full_lens = [len(str(dm_i)) for dm_i in range(1, dm_n + 1)]
    
    dm_rows = []
    for dm_i in range(dm_n):
        dm_rotated_nums = dm_nums[dm_i:] + dm_nums[:dm_i]
        dm_rows.append("".join(dm_rotated_nums))
    return "\n".join(dm_rows)
