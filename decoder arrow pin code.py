import re

def dec_arrow_pin_code(dm_arrow_str):
    dm_pos = {
        '1': (0, 0), '2': (1, 0), '3': (2, 0),
        '4': (0, 1), '5': (1, 1), '6': (2, 1),
        '7': (0, 2), '8': (1, 2), '9': (2, 2),
        '0': (0, -1)
    }
    dm_rev = {dm_v: dm_k for dm_k, dm_v in dm_pos.items()}
    dm_moves = {
        '↑': (0, 1),
        '↓': (0, -1),
        '→': (1, 0),
        '←': (-1, 0)
    }

    if not dm_arrow_str or not dm_arrow_str[0].isdigit():
        return []

    dm_start_char = dm_arrow_str[0]
    if dm_start_char not in dm_pos:
        return []

    dm_curr_coord = dm_pos[dm_start_char]
    dm_result = [int(dm_start_char)]

    dm_tokens = re.findall(r'[↑↓→←]|\*[1-9]', dm_arrow_str[1:])
    dm_reconstructed = "".join(dm_tokens)
    if dm_reconstructed != dm_arrow_str[1:]:
        return []
    
########    ##########  ##          ##########    ######    ##      ##        ##      ##    ######    ##########  ########      ######    
########    ##########  ##          ##########    ######    ##      ##        ##      ##    ######    ##########  ########      ######    
##      ##  ##          ##          ##          ##      ##  ####    ##        ####  ####  ##      ##  ##          ##      ##  ##      ##  
##      ##  ##          ##          ##          ##      ##  ####    ##        ####  ####  ##      ##  ##          ##      ##  ##      ##  
##      ##  ########    ##          ########    ##########  ##  ##  ##        ##  ##  ##  ##########  ########    ########    ##########  
##      ##  ########    ##          ########    ##########  ##  ##  ##        ##  ##  ##  ##########  ########    ########    ##########  
##      ##  ##          ##          ##          ##      ##  ##    ####        ##      ##  ##      ##  ##          ##    ##    ##      ##  
##      ##  ##          ##          ##          ##      ##  ##    ####        ##      ##  ##      ##  ##          ##    ##    ##      ##  
########    ##########  ##########  ##########  ##      ##  ##      ##        ##      ##  ##      ##  ##          ##      ##  ##      ##  
########    ##########  ##########  ##########  ##      ##  ##      ##        ##      ##  ##      ##  ##          ##      ##  ##      ##  

    for dm_token in dm_tokens:
        if dm_token.startswith('*'):
            dm_count = int(dm_token[1])
            dm_digit = int(dm_rev[dm_curr_coord])
            for _ in range(dm_count):
                dm_result.append(dm_digit)
        else:
            dm_move = dm_moves[dm_token]
            dm_curr_coord = (dm_curr_coord[0] + dm_move[0], dm_curr_coord[1] + dm_move[1])
            if dm_curr_coord not in dm_rev:
                return []
            dm_digit = int(dm_rev[dm_curr_coord])
            dm_result.append(dm_digit)

    return dm_result
