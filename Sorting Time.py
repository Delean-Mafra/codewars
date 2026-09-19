def sort_time(dm):
    def dm1(dm2):
        dm3, dm4 = map(int, dm2.split(':'))
        return dm3 * 60 + dm4

    dm5 = list(dm)
    dm6 = []
    dm7 = 0

    while dm5:
        dm8 = [dm9 for dm9 in dm5 if dm1(dm9[0]) >= dm7]
        if not dm8:
            dm8 = dm5
        
        dm10 = min(dm8, key=lambda dm11: dm1(dm11[0]))
        dm6.append(dm10)
        dm5.remove(dm10)
        dm7 = dm1(dm10[1])

    return dm6

"""
@@@@@@@@    @@      @@  
@@@@@@@@    @@      @@  
@@      @@  @@@@  @@@@  
@@      @@  @@@@  @@@@  
@@      @@  @@  @@  @@  
@@      @@  @@  @@  @@  
@@      @@  @@      @@  
@@      @@  @@      @@  
@@@@@@@@    @@      @@  
@@@@@@@@    @@      @@  
"""
