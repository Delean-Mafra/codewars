def regex_divisible_by(n):
    # Inicializa as transições do DFA para os estados de 0 a n-1
    transitions = {i: {j: [] for j in range(n)} for i in range(n)}
    for s in range(n):
        transitions[s][(2 * s) % n].append('0')
        transitions[s][(2 * s + 1) % n].append('1')
        
    for i in range(n):
        for j in range(n):
            if transitions[i][j]:
                if len(transitions[i][j]) > 1:
                    transitions[i][j] = '(?:' + '|'.join(transitions[i][j]) + ')'
                else:
                    transitions[i][j] = transitions[i][j][0]
            else:
                transitions[i][j] = ''

    # Elimina os estados de 1 até n-1 um por um
    for k in range(1, n):
        kk = transitions[k][k]
        kk_star = f"(?:{kk})*" if kk else ""
        for i in range(n):
            if i == k: continue
            ik = transitions[i][k]
            if not ik: continue
            for j in range(n):
                if j == k: continue
                kj = transitions[k][j]
                if not kj: continue
                
                path = ik + kk_star + kj
                if transitions[i][j]:
                    transitions[i][j] = f"(?:{transitions[i][j]}|{path})"
                else:
                    transitions[i][j] = path
                    
        for i in range(n):
            transitions[i][k] = ''
            transitions[k][i] = ''

    # Constrói o loop final do estado 0 para ele mesmo
    r00 = transitions[0][0]
    regex = f"(?:{r00})+" if r00 else ""
    
    # Retorna a expressão regular ancorada
    return f"^{regex}$"
