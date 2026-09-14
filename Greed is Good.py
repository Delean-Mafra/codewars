def score(dm_dice):
    dm_score = 0
    dm_counts = {dm_x: dm_dice.count(dm_x) for dm_x in range(1, 7)}
    
    dm_score += (dm_counts[1] // 3) * 1000 + (dm_counts[1] % 3) * 100
    dm_score += (dm_counts[2] // 3) * 200
    dm_score += (dm_counts[3] // 3) * 300
    dm_score += (dm_counts[4] // 3) * 400
    dm_score += (dm_counts[5] // 3) * 500 + (dm_counts[5] % 3) * 50
    dm_score += (dm_counts[6] // 3) * 600
    
    return dm_score
