def testit(dm, dm1):
    dm2 = []
    for dm3 in range(len(dm)):
        dm4 = dm[dm3]
        dm5 = dm1[dm3]
        if dm4 == "run":
            dm2.append("_" if dm5 == "_" else "/")
        else:
            dm2.append("x" if dm5 == "_" else "|")
    return "".join(dm2)
