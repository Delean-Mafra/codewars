dm_q = [1, 1]

def hofstadter_q(dm_n):
    while len(dm_q) < dm_n:
        dm_i = len(dm_q)
        dm_q.append(dm_q[dm_i - dm_q[dm_i - 1]] + dm_q[dm_i - dm_q[dm_i - 2]])
    return dm_q[dm_n - 1]
