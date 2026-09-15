def solution(dm_number):
    if dm_number < 0:
        return 0
    return sum(dm_i for dm_i in range(dm_number) if dm_i % 3 == 0 or dm_i % 5 == 0)
