import re

def find_glasses(dm):
    dm1 = re.compile(r"O-+O")
    for dm2, dm3 in enumerate(dm):
        if dm1.search(dm3):
            return dm2
    return -1
