def only_duplicates(dm):
    return "".join(dm1 for dm1 in dm if dm.count(dm1) > 1)
