def is_sator_square(tablet):
    dm = len(tablet)
    for dm1 in range(dm):
        for dm2 in range(dm):
            dm3 = tablet[dm1][dm2]
            if (dm3 != tablet[dm2][dm1] or 
                dm3 != tablet[dm - 1 - dm1][dm - 1 - dm2] or 
                dm3 != tablet[dm - 1 - dm2][dm - 1 - dm1]):
                return False
    return True
