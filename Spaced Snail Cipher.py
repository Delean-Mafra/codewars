# https://www.codewars.com/kata/6a37e118ef0c62f1772b6c6d/train/python

def dm_gerar_coordenadas(dm_tamanho:int, dm_chave:int):
    dm_vetores={
        1:[(0,1),(-1,0),(0,-1),(1,0)],
        2:[(0,1),(1,0),(0,-1),(-1,0)],
        3:[(1,0),(0,1),(-1,0),(0,-1)],
        4:[(1,0),(0,-1),(-1,0),(0,1)],
        5:[(0,-1),(1,0),(0,1),(-1,0)],
        6:[(0,-1),(-1,0),(0,1),(1,0)],
        7:[(-1,0),(0,-1),(1,0),(0,1)],
        8:[(-1,0),(0,1),(1,0),(0,-1)]}
    dm_sinal=1 if dm_chave>=0 else -1
    dm_chave_abs=abs(dm_chave)
    dm_orientacao=dm_chave_abs//10
    dm_espaco=dm_chave_abs %10
    dm_direcoes=dm_vetores[dm_orientacao]
    dm_coords=[(0,0)]
    dm_x,dm_y=0,0
    dm_indice_dir=0
    dm_fator_passo=dm_espaco+1
    dm_multiplicador=1
    dm_passos_dados=0
    while len(dm_coords)<dm_tamanho:
        dm_dx,dm_dy=dm_direcoes[dm_indice_dir]
        dm_passos_alvo=dm_multiplicador*dm_fator_passo
        for dm_passo in range(dm_passos_alvo):
            dm_x +=dm_dx
            dm_y +=dm_dy
            dm_coords.append((dm_x,dm_y))
            if len(dm_coords)==dm_tamanho:
                break 
        dm_indice_dir=(dm_indice_dir+ 1) % 4
        dm_passos_dados+=1
        if dm_passos_dados % 2==0:
            dm_multiplicador +=1            
    return dm_coords,dm_sinal
def encode(plaintext:str, key:int)->str:
    if not plaintext:
        return ''        
    dm_coords, dm_sinal=dm_gerar_coordenadas(len(plaintext), key)
    dm_mapa_coords=[]
    for dm_i, (dm_x, dm_y) in enumerate(dm_coords):
        dm_indice_char=dm_i if dm_sinal==1 else len(plaintext) - 1 - dm_i
        dm_char=plaintext[dm_indice_char]
        dm_mapa_coords.append((dm_y, dm_x, dm_char))
    dm_mapa_coords.sort()
    return ''.join(dm_item[2] for dm_item in dm_mapa_coords)
def decode(cipher:str, key:int) -> str:
    if not cipher:
        return ''
    dm_tamanho=len(cipher)
    dm_coords, dm_sinal=dm_gerar_coordenadas(dm_tamanho, key)
    dm_coords_com_indice=[(dm_y, dm_x, dm_i) for dm_i, (dm_x, dm_y) in enumerate(dm_coords)]
    dm_coords_com_indice.sort()
    dm_plaintext=[''] * dm_tamanho
    for dm_idx_cipher, (dm_y, dm_x, dm_idx_original) in enumerate(dm_coords_com_indice):
        dm_char=cipher[dm_idx_cipher]
        dm_indice_real=dm_idx_original if dm_sinal==1 else dm_tamanho - 1 - dm_idx_original
        dm_plaintext[dm_indice_real]=dm_char
    return ''.join(dm_plaintext)
