def search_names(dm_logins):
    return list(filter(lambda dm_x: dm_x[0].endswith("_"), dm_logins))
