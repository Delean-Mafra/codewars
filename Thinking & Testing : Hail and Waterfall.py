def test_it(dm):
    dm1 = []
    for dm2 in dm:
        dm3 = [dm2 % 10]
        dm4 = dm2
        while True:
            if dm4 == 1 or dm4 == 2:
                break
            if dm4 % 2 == 0:
                dm4 = dm4 // 2
            else:
                dm4 = 3 * dm4 + 1
            dm3.append(dm4 % 10)
        dm1.append(dm3)
    
    dm5 = max(len(dm6) for dm6 in dm1)
    dm7 = []
    for dm8 in range(dm5 + 1):
        dm9 = []
        for dm6 in dm1:
            if dm8 < len(dm6):
                dm9.append(str(dm6[dm8]))
            else:
                dm9.append('.')
        dm7.append("|".join(dm9))
    return "\n".join(dm7)
