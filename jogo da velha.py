import math

# Função para exibir o tabuleiro
def display_board(board):
    # Percorre cada linha do tabuleiro e imprime suas células separadas por " | "
    for row in board:
        print(" | ".join(row))
        # Imprime uma linha de separação após cada linha do tabuleiro
        print("-" * 9)

# Função para verificar se há um vencedor
def check_winner(board, player):
    # Verifica se o jogador ganhou em alguma linha
    for i in range(3):
        if all([cell == player for cell in board[i]]):  # Todas as células da linha pertencem ao mesmo jogador
            return True
        # Verifica se o jogador ganhou em alguma coluna
        if all([board[j][i] == player for j in range(3)]):  # Todas as células da coluna pertencem ao mesmo jogador
            return True
    # Verifica se o jogador ganhou em uma das diagonais
    if board[0][0] == board[1][1] == board[2][2] == player:  # Diagonal principal
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:  # Diagonal secundária
        return True
    return False  # Retorna False se não encontrou um vencedor

# Função para verificar se houve empate (nenhuma célula está vazia)
def check_draw(board):
    # Retorna True se todas as células estiverem preenchidas (não há " ")
    return all(cell != " " for row in board for cell in row)

# Função de avaliação para o algoritmo Minimax
def evaluate(board):
    # Retorna um valor positivo se o computador (O) venceu
    if check_winner(board, "O"):
        return 1  # Vitória do computador
    # Retorna um valor negativo se o jogador humano (X) venceu
    elif check_winner(board, "X"):
        return -1  # Vitória do jogador humano
    return 0  # Empate ou jogo continua

# Função Minimax para encontrar a melhor jogada
def minimax(board, depth, is_maximizing):
    # Avalia o estado atual do tabuleiro
    score = evaluate(board)
    
    # Se houver um vencedor, retorna o valor da pontuação
    if score == 1 or score == -1:
        return score
    # Se o jogo terminar em empate, retorna 0
    if check_draw(board):
        return 0

    # Se for a vez do jogador "maximizador" (computador - O)
    if is_maximizing:
        best_score = -math.inf  # Define a melhor pontuação inicial como negativa infinita
        for i in range(3):
            for j in range(3):
                # Verifica células vazias para simular movimentos
                if board[i][j] == " ":
                    board[i][j] = "O"  # Faz um movimento hipotético
                    score = minimax(board, depth + 1, False)  # Chamada recursiva para o adversário
                    board[i][j] = " "  # Desfaz o movimento
                    best_score = max(best_score, score)  # Atualiza a melhor pontuação
        return best_score
    else:
        # Se for a vez do jogador "minimizador" (humano - X)
        best_score = math.inf  # Define a melhor pontuação inicial como infinita
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"  # Faz um movimento hipotético
                    score = minimax(board, depth + 1, True)  # Chamada recursiva para o adversário
                    board[i][j] = " "  # Desfaz o movimento
                    best_score = min(best_score, score)  # Atualiza a melhor pontuação
        return best_score

# Função para encontrar a melhor jogada para o computador
def best_move(board):
    best_score = -math.inf  # Inicializa a melhor pontuação com negativa infinita
    move = None  # Armazena a melhor jogada encontrada

    # Verifica todas as células do tabuleiro
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"  # Faz um movimento hipotético
                score = minimax(board, 0, False)  # Avalia o tabuleiro resultante
                board[i][j] = " "  # Desfaz o movimento
                # Se a pontuação desse movimento for melhor que a melhor pontuação encontrada, atualiza
                if score > best_score:
                    best_score = score
                    move = (i, j)  # Guarda a posição da melhor jogada
    return move

# Função principal do jogo
def tic_tac_toe():
    # Inicializa o tabuleiro como uma matriz 3x3 cheia de espaços em branco
    board = [[" " for _ in range(3)] for _ in range(3)]
    
    # Loop principal do jogo
    while True:
        display_board(board)  # Exibe o tabuleiro

        # Turno do jogador humano
        print("Sua vez! (Jogador X)")
        row = int(input("Escolha a linha (0, 1, 2): "))
        col = int(input("Escolha a coluna (0, 1, 2): "))
        
        # Verifica se a entrada do jogador é válida
        if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == " ":
            board[row][col] = "X"  # Marca o movimento do jogador no tabuleiro
        else:
            print("Posição inválida, tente novamente.")
            continue  # Pede nova entrada se a posição for inválida

        # Verifica se o jogador humano venceu
        if check_winner(board, "X"):
            display_board(board)
            print("Você venceu!")
            break

        # Verifica empate
        if check_draw(board):
            display_board(board)
            print("Empate!")
            break

        # Turno do computador
        print("Vez do computador! (Jogador O)")
        move = best_move(board)  # Encontra a melhor jogada para o computador
        if move:
            board[move[0]][move[1]] = "O"  # Executa a jogada no tabuleiro

        # Verifica se o computador venceu
        if check_winner(board, "O"):
            display_board(board)
            print("O computador venceu!")
            break

        # Verifica empate
        if check_draw(board):
            display_board(board)
            print("Empate!")
            break

# Executa o jogo
tic_tac_toe()

"""Descrição e Regras do Jogo da Velha
O Jogo da Velha é um jogo de tabuleiro de dois jogadores que disputam em um tabuleiro 3x3. Os jogadores alternam turnos e devem marcar as células do tabuleiro com um símbolo, sendo "X" para o jogador humano e "O" para o computador. O objetivo é ser o primeiro a alinhar três símbolos (na horizontal, vertical ou diagonal). O jogo termina quando um jogador vence ou quando não há mais jogadas possíveis (empate).

Regras:

O tabuleiro começa vazio, com 9 células.
O jogador "X" e o computador "O" alternam turnos.
O jogador "X" escolhe uma célula para colocar seu símbolo, digitando a linha e a coluna desejada.
O computador faz sua jogada com base no algoritmo Minimax.
O jogo termina quando um dos jogadores ganha ou se todas as células forem preenchidas, resultando em empate.
Formulação do Problema de Busca
No contexto do algoritmo Minimax, o problema de busca pode ser formulado como uma árvore de busca, onde:

Estado: O estado é o tabuleiro de 3x3, onde as células podem estar vazias, preenchidas com "X" ou com "O".
Ação: Uma ação é a escolha de uma célula vazia para marcar o símbolo do jogador atual ("X" ou "O").
Função de Transição: A função de transição transforma um estado para outro, após a execução de uma jogada de um dos jogadores.
Objetivo: O objetivo é alcançar um estado onde o jogador "X" ou "O" tenha alinhado três símbolos em uma linha, coluna ou diagonal.
Função de Avaliação: A função de avaliação é usada para determinar o valor de um estado terminal (vitória, derrota ou empate). Ela atribui valores como:
1 para vitória do computador ("O").
-1 para vitória do jogador ("X").
0 para empate ou jogo em andamento.
O problema de busca é buscar o melhor movimento para o computador, com base na minimização ou maximização da pontuação, dependendo do turno.

Tipo de Jogo
Tipo de Jogo: Determinístico

O jogo da velha é um jogo determinístico porque o resultado de qualquer movimento depende exclusivamente do estado atual do tabuleiro, e não envolve nenhum elemento de aleatoriedade ou incerteza. Ou seja, para um dado estado do tabuleiro, sempre existe uma única sequência de jogadas possíveis, sem chance de eventos imprevisíveis (como rolar um dado ou embaralhar cartas).

O comportamento de ambos os jogadores (o humano e o computador) é completamente previsível com base nas regras do jogo, não havendo elementos estocásticos (aleatórios) que alterem o curso do jogo.

Solução Escolhida
A solução escolhida para resolver o problema de busca é o algoritmo Minimax, que é um algoritmo de busca em árvores usado para jogos de soma zero, como o Jogo da Velha. O Minimax funciona da seguinte maneira:

Avaliação de Todos os Estados Finais: O algoritmo calcula todos os possíveis estados do jogo (movimentos futuros), avaliando-os de acordo com uma função de avaliação que determina se o estado final é uma vitória, derrota ou empate.

Recursão e Maximização: O Minimax explora todas as jogadas possíveis a partir do estado atual, recursivamente. Para o computador (jogador "O"), o algoritmo tenta maximizar a pontuação (preferindo estados em que ele vence), e para o jogador humano (jogador "X"), ele tenta minimizar a pontuação (evitando que o computador vença).

Backtracking: O algoritmo utiliza uma técnica chamada backtracking, onde ele explora todas as possibilidades de jogadas, simula cada movimento, e, caso chegue a um estado final (vitória ou empate), retorna o valor correspondente (1, -1 ou 0). Depois, ele "volta atrás" e simula a próxima jogada, repetindo esse processo até que o melhor movimento seja encontrado.

Implementação da Solução
A implementação do Minimax está presente nas funções minimax e best_move. A função minimax é chamada recursivamente para avaliar todos os estados possíveis do tabuleiro, enquanto a função best_move escolhe a jogada ideal para o computador com base na avaliação de todos os estados possíveis.

A profundidade da busca (ou seja, o número de jogadas futuras que o algoritmo deve simular) não é limitada explicitamente, mas no caso do Jogo da Velha, ela é limitada pelo tamanho do tabuleiro (3x3), o que significa que o algoritmo irá explorar todos os possíveis estados até encontrar uma solução.

Resumo da Solução:
Algoritmo: Minimax, que explora as possibilidades futuras e calcula a melhor jogada.
Tipo de Jogo: Determinístico (não envolve aleatoriedade).
Estratégia: Maximizar a pontuação para o computador e minimizar para o jogador humano, escolhendo a jogada ótima."""
