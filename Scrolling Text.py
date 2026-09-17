def scrolling_text(dm):
    
    """
    ████  █   █ 
    █   █ ██ ██ 
    █   █ █ █ █ 
    █   █ █   █ 
    ████  █   █ 
    """    

    d = dm.upper()
    return [d[m:] + d[:m] for m in range(len(d))]
