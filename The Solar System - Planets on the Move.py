def move_planets(dm):
    dm1 = list(dm)
    dm_small = {"Mercury", "Venus", "Mars", "Earth"}
    dm_gas = {"Jupiter", "Saturn", "Uranus", "Neptune"}
    """
    ****  *   * 
    *   * ** ** 
    *   * * * * 
    *   * *   * 
    ****  *   *   
    """
    while True:
        dm2 = -1
        dm3 = None
        dm4 = 0
        dm5 = ""

        for dm6, dm7 in enumerate(dm1):
            if dm7.startswith('<'):
                dm2 = dm6
                dm3 = '<'
                dm4 = dm7.count('<')
                dm5 = dm7.lstrip('<')
                break
            elif dm7.endswith('>'):
                dm2 = dm6
                dm3 = '>'
                dm4 = dm7.count('>')
                dm5 = dm7.rstrip('>')
                break

        if dm2 == -1:
            break

        dm8 = dm2
        dm9 = False

        for dm10 in range(dm4):
            dm11 = dm8 + (-1 if dm3 == '<' else 1)
            if dm11 < 0 or dm11 >= len(dm1):
                dm1.pop(dm8)
                dm9 = True
                break

            dm12 = dm1[dm11]
            if dm12 == "Blackhole":
                dm1.pop(dm8)
                dm9 = True
                break

            if dm12.startswith('<'):
                dm13 = dm12.lstrip('<')
            elif dm12.endswith('>'):
                dm13 = dm12.rstrip('>')
            else:
                dm13 = dm12

            if dm5 == "Asteroid":
                if dm13 == "Asteroid":
                    dm1[dm11] = dm5
                    dm1.pop(dm8)
                    dm8 = dm11 if dm3 == '<' else dm11 - 1
                elif dm13 in dm_small:
                    dm_indices = sorted([dm8, dm11], reverse=True)
                    dm1.pop(dm_indices[0])
                    dm1.pop(dm_indices[1])
                    dm9 = True
                    break
                elif dm13 in dm_gas:
                    dm1.pop(dm8)
                    dm9 = True
                    break
            elif dm5 in dm_small:
                if dm13 == "Asteroid":
                    dm1[dm11] = dm5
                    dm1.pop(dm8)
                    dm8 = dm11 if dm3 == '<' else dm11 - 1
                elif dm13 in dm_small:
                    dm1[dm11] = dm5
                    dm1.pop(dm8)
                    dm8 = dm11 if dm3 == '<' else dm11 - 1
                elif dm13 in dm_gas:
                    dm1.pop(dm8)
                    dm9 = True
                    break
            elif dm5 in dm_gas:
                if dm13 == "Asteroid" or dm13 in dm_small or dm13 in dm_gas:
                    dm1[dm11] = dm5
                    dm1.pop(dm8)
                    dm8 = dm11 if dm3 == '<' else dm11 - 1

        if not dm9 and dm8 < len(dm1):
            dm1[dm8] = dm5

    return dm1
