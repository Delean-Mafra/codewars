def wave_sort(xs: list[int]) -> None:
    if not xs:
        return
        
    dm_tamanho = len(xs)
    for dm_i in range(dm_tamanho - 1):
        if dm_i % 2 == 0:
            if xs[dm_i] < xs[dm_i + 1]:
                xs[dm_i], xs[dm_i + 1] = xs[dm_i + 1], xs[dm_i]
        else:
            if xs[dm_i] > xs[dm_i + 1]:
                xs[dm_i], xs[dm_i + 1] = xs[dm_i + 1], xs[dm_i]
