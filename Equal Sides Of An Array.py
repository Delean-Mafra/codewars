def find_even_index(arr):
    dm_total = sum(arr)
    dm_left_sum = 0
    for dm_i, dm_val in enumerate(arr):
        if dm_left_sum == dm_total - dm_left_sum - dm_val:
            return dm_i
        dm_left_sum += dm_val
    return -1
