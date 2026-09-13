import re

def pseudo_sort(dm_sentence):
    dm_words = re.findall(r"[A-Za-z]+", dm_sentence)
    if not dm_words:
        return ""
    dm_lower = [dm_w for dm_w in dm_words if dm_w[0].islower()]
    dm_upper = [dm_w for dm_w in dm_words if dm_w[0].isupper()]
    
    dm_lower.sort()
    dm_upper.sort(reverse=True)
    
    return " ".join(dm_lower + dm_upper)
