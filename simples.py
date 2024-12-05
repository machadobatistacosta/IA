import numpy as np
import matplotlib.pyplot as plt
import random

# Inicializa o ambiente 6x6
def inicializar_ambiente():
    matriz = np.ones((6, 6))  # Inicia com tudo como parede (1)
    for i in range(1, 5):  # Preenche o espaço 4x4 com limpo (0)
        for j in range(1, 5):
            matriz[i][j] = 0
    return matriz

# Posiciona a sujeira aleatoriamente no ambiente 4x4
def adicionar_sujeira(matriz, num_sujeiras=3):
    count = 0
    while count < num_sujeiras:
        x = random.randint(1, 4)
        y = random.randint(1, 4)
        if matriz[x][y] == 0:  # Apenas adicionar sujeira em células limpas
            matriz[x][y] = 2
            count += 1

# Função para exibir o ambiente usando matplotlib
def exibir(matriz, posAPAx, posAPAy):
    plt.imshow(matriz, cmap='nipy_spectral', origin='upper')
    plt.plot([posAPAy], [posAPAx], marker='o', color='r', ls='')  # Agente em vermelho
    plt.show(block=False)
    plt.pause(0.5)
    plt.clf()

# Função do agente reativo simples com varredura em ziguezague
def agenteReativoSimples(percepcao, direcao):
    x, y, status = percepcao
    if status == 2:  # Se a célula está suja
        return 'aspirar', direcao
    else:
        if direcao == 'direita':
            if y < 4:  # Pode se mover para a direita
                return 'direita', direcao
            else:  # Se não pode mais ir para a direita, desce e inverte a direção
                if x < 4:
                    return 'abaixo', 'esquerda'
                else:
                    return 'esperar', direcao
        elif direcao == 'esquerda':
            if y > 1:  # Pode se mover para a esquerda
                return 'esquerda', direcao
            else:  # Se não pode mais ir para a esquerda, desce e inverte a direção
                if x < 4:
                    return 'abaixo', 'direita'
                else:
                    return 'esperar', direcao

# Função para executar a ação do agente
def executar_acao(acao):
    global posAPAx, posAPAy
    if acao == 'aspirar':
        matriz[posAPAx][posAPAy] = 0
    elif acao == 'direita' and posAPAy < 4:
        posAPAy += 1
    elif acao == 'abaixo' and posAPAx < 4:
        posAPAx += 1
    elif acao == 'esquerda' and posAPAy > 1:
        posAPAy -= 1
    elif acao == 'acima' and posAPAx > 1:
        posAPAx -= 1

# Função para o agente percorrer o ambiente e registrar o caminho
def varredura_e_registrar_caminho(max_varreduras=3):
    global posAPAx, posAPAy, direcao
    caminho = []
    varreduras = 0

    while varreduras < max_varreduras:
        percepcao = (posAPAx, posAPAy, matriz[posAPAx][posAPAy])
        acao, direcao = agenteReativoSimples(percepcao, direcao)
        if acao == 'esperar':  # Se o agente já percorreu toda a linha
            varreduras += 1
            if varreduras < max_varreduras:
                # Move para baixo para iniciar uma nova varredura
                if direcao == 'direita':
                    if posAPAx < 4:
                        executar_acao('abaixo')
                        exibir(matriz, posAPAx, posAPAy)
                elif direcao == 'esquerda':
                    if posAPAx < 4:
                        executar_acao('abaixo')
                        exibir(matriz, posAPAx, posAPAy)
                direcao = 'esquerda' if direcao == 'direita' else 'direita'
        else:
            caminho.append((posAPAx, posAPAy))  # Registra a posição visitada
            executar_acao(acao)
            exibir(matriz, posAPAx, posAPAy)
            caminho.append((posAPAx, posAPAy))  # Registra a posição após ação

    return caminho

# Função para o agente retornar à posição inicial
def caminho_volta(caminho):
    global posAPAx, posAPAy
    for (x, y) in reversed(caminho):
        while posAPAx != x or posAPAy != y:
            if posAPAx < x:
                executar_acao('abaixo')
            elif posAPAx > x:
                executar_acao('acima')
            elif posAPAy < y:
                executar_acao('direita')
            elif posAPAy > y:
                executar_acao('esquerda')
            exibir(matriz, posAPAx, posAPAy)

# Inicializa o ambiente e adiciona sujeira
matriz = inicializar_ambiente()
adicionar_sujeira(matriz)
posAPAx, posAPAy = 1, 1  # Posição inicial do aspirador

# Exibe o ambiente inicial
exibir(matriz, posAPAx, posAPAy)

# Varre o ambiente e registra o caminho
caminho = varredura_e_registrar_caminho()

print("Varredura concluída.")
print("Iniciando o caminho de volta...")
caminho_volta(caminho)
print("Retorno concluído.")
