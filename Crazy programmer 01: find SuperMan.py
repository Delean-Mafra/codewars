def find_super_man(dm):
    dm1 = dm.lower()
    def dm2(dm3):
        dm4 = -2
        for dm5 in dm3:
            dm6 = dm1.find(dm5, dm4 + 2)
            if dm6 == -1:
                return False
            dm4 = dm6
        return True
    if dm2("superman") or dm2("namrepus"):
        return "Hi, SuperMan!"
    return "Are you crazy?"
"""
####  #   # 
#   # ## ## 
#   # # # # 
#   # #   # 
####  #   # 
"""
