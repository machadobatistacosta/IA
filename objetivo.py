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
def adicionar_sujeira(matriz, num_sujeiras=4):
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

# Inicializa o ambiente e adiciona sujeira
matriz = inicializar_ambiente()
adicionar_sujeira(matriz)
posAPAx, posAPAy = 1, 1  # Posição inicial do aspirador

# Exibe o ambiente inicial
exibir(matriz, posAPAx, posAPAy)

# Função para o agente baseado em objetivos
def agenteBaseadoEmObjetivo(matriz, visitados, posAPAx, posAPAy):
    if matriz[posAPAx][posAPAy] == 2:  # Se a célula está suja
        return 'aspirar'

    # Marca a posição atual como visitada
    visitados.add((posAPAx, posAPAy))

    # Verifica células ao redor para determinar próxima ação
    movimentos_possiveis = [
        ('acima', (posAPAx - 1, posAPAy)),
        ('abaixo', (posAPAx + 1, posAPAy)),
        ('esquerda', (posAPAx, posAPAy - 1)),
        ('direita', (posAPAx, posAPAy + 1))
    ]

    # Prioriza movimentos que levam a sujeira
    for direcao, (nx, ny) in movimentos_possiveis:
        if (1 <= nx <= 4 and 1 <= ny <= 4 and  # Dentro dos limites
            matriz[nx][ny] == 2):  # Sujeira encontrada
            return direcao

    # Se não há sujeira adjacente, mova-se para a próxima célula não visitada
    for direcao, (nx, ny) in movimentos_possiveis:
        if (1 <= nx <= 4 and 1 <= ny <= 4 and  # Dentro dos limites
            (nx, ny) not in visitados):  # Não visitada
            return direcao

    # Se todas as células ao redor foram visitadas e estão limpas, continue buscando
    return random.choice(['acima', 'abaixo', 'esquerda', 'direita'])

# Função para executar a ação do agente
def executar_acao(acao):
    global posAPAx, posAPAy, pontos
    pontos += 1  # Cada ação conta 1 ponto
    if acao == 'aspirar':
        matriz[posAPAx][posAPAy] = 0
        pontos += 1  # Aspirar sujeira adiciona mais 1 ponto
        print(f"Sujeira aspirada! Pontos: {pontos}")
    elif acao == 'direita' and posAPAy < 4:
        posAPAy += 1
    elif acao == 'abaixo' and posAPAx < 4:
        posAPAx += 1
    elif acao == 'esquerda' and posAPAy > 1:
        posAPAy -= 1
    elif acao == 'acima' and posAPAx > 1:
        posAPAx -= 1

# Função para verificar se o ambiente está totalmente limpo
def ambiente_limpo(matriz):
    for i in range(1, 5):
        for j in range(1, 5):
            if matriz[i][j] == 2:  # Se encontrar sujeira, retorna False
                return False
    return True

# Loop principal para o agente operar com base em objetivos
visitados = set()  # Mantém registro de células visitadas
pontos = 0  # Inicializa o contador de pontos

while True:
    if ambiente_limpo(matriz):  # Verifica se o ambiente está limpo
        print(f"Ambiente totalmente limpo! Pontuação final: {pontos}")
        break
    acao = agenteBaseadoEmObjetivo(matriz, visitados, posAPAx, posAPAy)
    executar_acao(acao)
    exibir(matriz, posAPAx, posAPAy)
