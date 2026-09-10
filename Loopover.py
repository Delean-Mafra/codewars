def loopover(mixedUpBoard, solvedBoard):
    R = len(mixedUpBoard)
    C = len(mixedUpBoard[0])
    
    transposed = False
    if C % 2 != 0 and R % 2 == 0:
        transposed = True
        mixedUpBoard = [list(x) for x in zip(*mixedUpBoard)]
        solvedBoard = [list(x) for x in zip(*solvedBoard)]
        R, C = C, R
        
    moves = []
    board = [row[:] for row in mixedUpBoard]
    
    def do(m):
        moves.append(m)
        d = m[0]
        i = int(m[1:])
        if d == 'L':
            board[i] = board[i][1:] + [board[i][0]]
        elif d == 'R':
            board[i] = [board[i][-1]] + board[i][:-1]
        elif d == 'U':
            col = [board[r][i] for r in range(R)]
            col = col[1:] + [col[0]]
            for r in range(R): board[r][i] = col[r]
        elif d == 'D':
            col = [board[r][i] for r in range(R)]
            col = [col[-1]] + col[:-1]
            for r in range(R): board[r][i] = col[r]

    for r in range(R - 1):
        for c in range(C):
            target = solvedBoard[r][c]
            pr, pc = -1, -1
            for i in range(r, R):
                for j in range(C):
                    if board[i][j] == target:
                        pr, pc = i, j
                        break
                if pr != -1: break
                
            if pr == -1:
                for i in range(r):
                    for j in range(C):
                        if board[i][j] == target:
                            pr, pc = i, j
                            break
                    if pr != -1: break
                    
            if pr == r and pc == c:
                continue
                
            if pr == r:
                do(f"D{pc}")
                do(f"L{r+1}")
                do(f"U{pc}")
                pr = r + 1
                pc = (pc - 1) % C
                
            if pc == c:
                do(f"L{pr}")
                pc = (pc - 1) % C
                
            dist = pr - r
            
            for _ in range(dist): do(f"D{c}")
            
            dist_col = (c - pc) % C
            if dist_col <= C // 2:
                for _ in range(dist_col): do(f"R{pr}")
            else:
                for _ in range(C - dist_col): do(f"L{pr}")
                
            for _ in range(dist): do(f"U{c}")

    current = board[R-1]
    target_row = solvedBoard[R-1]
    target_idx = {val: i for i, val in enumerate(target_row)}
    
    inversions = 0
    for i in range(C):
        for j in range(i + 1, C):
            if target_idx[current[i]] > target_idx[current[j]]:
                inversions += 1
                
    if inversions % 2 != 0:
        if C % 2 == 0:
            do(f"L{R-1}")
        else:
            return None

    def do_cycle(c1, c2):
        dist = (c2 - c1) % C
        do(f"D{c1}")
        for _ in range(dist): do(f"L{R-1}")
        do(f"U{c1}")
        for _ in range(dist): do(f"R{R-1}")

    def do_inv_cycle(c1, c2):
        dist = (c2 - c1) % C
        for _ in range(dist): do(f"L{R-1}")
        do(f"D{c1}")
        for _ in range(dist): do(f"R{R-1}")
        do(f"U{c1}")

    for c in range(C - 1, 1, -1):
        target_val = solvedBoard[R-1][c]
        x = board[R-1].index(target_val)
        if x == c:
            continue
        if x != 0 and x != c:
            do_cycle(0, x)
            do_inv_cycle(0, c)
        elif x == 0:
            do_cycle(0, 1)
            do_inv_cycle(0, c)
            do_cycle(0, 1)
            do_inv_cycle(0, c)
            
    if board != solvedBoard:
        return None
        
    if transposed:
        t_moves = []
        mapping = {'L': 'U', 'R': 'D', 'U': 'L', 'D': 'R'}
        for m in moves:
            t_moves.append(mapping[m[0]] + m[1:])
        return t_moves
        
    return moves
