import numpy as np
import matplotlib.pyplot as plt

# Função para calcular a distância euclidiana total de um caminho representado por um cromossomo.
def distancia_total(cromossomo, cidades):
    distancia = 0  # Inicializa a distância total acumulada
    # Itera sobre cada par de cidades no cromossomo, exceto o último
    for i in range(len(cromossomo) - 1):
        # Obtém as coordenadas da cidade atual e da próxima cidade
        x1, y1 = cidades[cromossomo[i]]  # Cidade atual
        x2, y2 = cidades[cromossomo[i+1]]  # Próxima cidade
        # Calcula a distância euclidiana entre a cidade atual e a próxima
        distancia += np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    # Calcula a distância de retorno à cidade inicial para completar o ciclo
    x1, y1 = cidades[cromossomo[-1]]  # Última cidade
    x2, y2 = cidades[cromossomo[0]]    # Cidade inicial
    # Adiciona a distância de retorno à cidade inicial
    distancia += np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    return distancia  # Retorna a distância total do caminho

# Função de aptidão que avalia a qualidade de cada cromossomo com base na distância total.
def aptidao(populacao, cidades):
    # Retorna uma lista de distâncias totais para cada cromossomo na população
    return [distancia_total(cromossomo, cidades) for cromossomo in populacao]

# Função de seleção por roleta ajustada
def selecao_roleta(aptidoes, populacao):
    # Inverte as aptidões para dar mais peso às soluções melhores (menores distâncias)
    aptidoes_invertidas = [1 / aptidao if aptidao != 0 else 1e10 for aptidao in aptidoes]  # Evita divisão por zero
    fitness_total = sum(aptidoes_invertidas)  # Soma total das aptidões invertidas

    # Gera um valor aleatório proporcional à soma total das aptidões invertidas
    pick = np.random.rand() * fitness_total
    current = 0  # Inicializa o acumulador de aptidão

    # Itera sobre a população acumulando a aptidão invertida de cada cromossomo
    for i, cromossomo in enumerate(populacao):
        current += aptidoes_invertidas[i]  # Acumula a aptidão invertida do cromossomo atual
        # Se a aptidão acumulada ultrapassa o valor sorteado, seleciona este cromossomo
        if current > pick:
            print(f"Cromossomo selecionado: {cromossomo} com aptidão: {aptidoes[i]}")  # Imprime o cromossomo selecionado
            return cromossomo  # Retorna o cromossomo selecionado

# Função de crossover utilizando a técnica Cycle Crossover para gerar um novo cromossomo.
def crossover(pai1, pai2):
    n = len(pai1)  # Número de cidades (genes) no cromossomo
    filho = [-1] * n  # Inicializa o filho com valores -1 (não preenchido)
    idx = 0  # Índice inicial para o ciclo de preenchimento
    ciclo = True  # Flag para controle do ciclo

    while ciclo:
        # Preenche o filho até encontrar um valor já preenchido
        while filho[idx] == -1:
            filho[idx] = pai1[idx]  # Copia o gene do pai1 para o filho
            # Encontra o índice do gene correspondente no pai1 baseado no gene do pai2
            idx = pai1.index(pai2[idx])  
        ciclo = False  # Sai do ciclo após a primeira execução
        # Verifica se ainda há elementos não preenchidos no filho
        for i in range(n):
            if filho[i] == -1:  # Se o elemento ainda não foi preenchido
                idx = i  # Atualiza o índice
                ciclo = True  # Reinicia o ciclo
                break  # Sai do loop
    
    # Preenche os restantes do pai2 nos espaços não preenchidos
    for i in range(n):
        if filho[i] == -1:
            filho[i] = pai2[i]
    
    return filho  # Retorna o cromossomo filho gerado

# Função de mutação que altera aleatoriamente a ordem dos genes em um cromossomo.
def mutacao(cromossomo, taxa_mutacao=0.1):
    # Verifica se a mutação deve ocorrer com base na taxa de mutação
    if np.random.rand() < taxa_mutacao:
        # Seleciona dois índices aleatórios para realizar a troca
        i, j = np.random.randint(0, len(cromossomo), 2)
        # Troca os genes nos índices selecionados
        cromossomo[i], cromossomo[j] = cromossomo[j], cromossomo[i]
    return cromossomo  # Retorna o cromossomo (mutado ou não)

# Função para imprimir a distância de um caminho específico representado por um cromossomo.
def print_distancia(cromossomo, cidades):
    distancia = distancia_total(cromossomo, cidades)  # Calcula a distância total do cromossomo
    # Imprime a distância formatada
    print(f"Distância do caminho {cromossomo}: {distancia:.4f}")

# Função para plotar a solução final em um gráfico.
def plot_cidades(cidades, melhor_solucao):
    # Prepara os dados para plotagem: coordenadas x e y do caminho
    x = [cidades[i][0] for i in melhor_solucao] + [cidades[melhor_solucao[0]][0]]  # Adiciona a cidade inicial no final
    y = [cidades[i][1] for i in melhor_solucao] + [cidades[melhor_solucao[0]][1]]  # Adiciona a cidade inicial no final
    plt.plot(x, y, marker='o')  # Plota o caminho com marcadores nas cidades
    plt.title("Melhor caminho encontrado")  # Define o título do gráfico
    plt.show()  # Exibe o gráfico

# Algoritmo Genético com elitismo que busca a melhor rota entre as cidades.
def algoritmo_genetico(cidades, tamanho_pop=20, num_geracoes=10000, taxa_mutacao=0.1, elite_size=2):
    n = len(cidades)  # Número total de cidades
    
    # Inicializa a população com cromossomos aleatórios (ordens de visita às cidades)
    populacao_inicial = [np.random.permutation(n).tolist() for _ in range(tamanho_pop)]
    populacao = populacao_inicial.copy()  # Cópia da população inicial para manipulação
    
    # Itera através do número de gerações especificadas
    for geracao in range(num_geracoes):
        # Calcula as aptidões (distâncias) de todos os cromossomos na população
        aptidoes = aptidao(populacao, cidades)
        
        # Elitismo: mantém os melhores indivíduos na próxima geração
        melhores_individuos = sorted(populacao, key=lambda cromo: distancia_total(cromo, cidades))[:elite_size]
        
        # Nova população para a próxima geração
        nova_populacao = []
        # Cria novos indivíduos até preencher a nova população
        for _ in range((tamanho_pop - elite_size) // 2):
            pai1 = selecao_roleta(aptidoes, populacao)  # Seleciona o primeiro pai
            pai2 = selecao_roleta(aptidoes, populacao)  # Seleciona o segundo pai
            filho1 = crossover(pai1, pai2)  # Cria o primeiro filho através do crossover
            filho2 = crossover(pai2, pai1)  # Cria o segundo filho através do crossover
            # Aplica mutação em ambos os filhos
            nova_populacao.append(mutacao(filho1, taxa_mutacao))
            nova_populacao.append(mutacao(filho2, taxa_mutacao))
        
        # Atualiza a população com os melhores indivíduos e a nova geração
        populacao = melhores_individuos + nova_populacao
        
        # Imprime o melhor resultado a cada 100 gerações
        if geracao % 100 == 0:
            melhor_aptidao = min(aptidoes)  # Encontra a menor distância
            melhor_solucao = populacao[np.argmin(aptidoes)]  # Encontra o cromossomo correspondente
            print(f"Geração {geracao}: Melhor Distância = {melhor_aptidao:.4f}")
    
    # Melhor solução final encontrada
    melhor_aptidao = min(aptidoes)
    melhor_solucao = populacao[np.argmin(aptidoes)]
    
    # Imprimir a melhor solução e sua distância total
    print(f"Melhor solução: {melhor_solucao}")
    print(f"Melhor distância: {melhor_aptidao:.4f}")
    print_distancia(melhor_solucao, cidades)  # Imprime a distância do melhor caminho

    # Exibir os resultados finais
    print("\nResultados Finais:")
    print(f"Tamanho da População: {tamanho_pop}")
    print("População Inicial:")  # Título para a população inicial
    for individuo in populacao_inicial:  # Imprime cada cromossomo em uma nova linha
        print(individuo)  # Imprime o cromossomo
    
    print("População Final:")  # Título para a população final
    for individuo in populacao:  # Imprime cada cromossomo em uma nova linha
        print(individuo)  # Imprime o cromossomo

    print(f"Número de Cidades: {n}")
    print(f"Melhor Custo: {melhor_aptidao:.4f}")
    print(f"Melhor Solução: {melhor_solucao}")

    # Plotar solução encontrada
    plot_cidades(cidades, melhor_solucao)

# Coordenadas fornecidas pela professora
x = [
    0.77687122244663642, 0.5572653296455039, 0.65639441309858648, 0.60439895238077324, 
    0.10984792404443977, 0.30681838758814639, 0.036420458719028548, 0.50750194272285054, 
    0.79819787712259027, 0.79896874846157562, 0.14326939769923641, 0.071101926660729675, 
    0.72613149506352259, 0.22624105387667293, 0.6248041238023041, 0.5483227916626594, 
    0.39699387912590556, 0.075454958741316913, 0.67595096782693853, 0.074297051769727118
]

y = [
    0.27943919986108079, 0.11661366329340583, 0.39053913424199571, 0.66616903964750607, 
    0.6985758378186272, 0.20730006383213373, 0.5024721283845478, 0.073938685056537334, 
    0.67991802460956252, 0.39749277989717913, 0.14151256215331487, 0.12773617026441342, 
    0.37197289724774407, 0.69033435138929333, 0.9189034809361033, 0.52333815217506263, 
    0.42525694545543524, 0.37166915101708831, 0.99033329254439939, 0.15694231625653665
]

# Juntar as coordenadas X e Y em um array de cidades
cidades = np.column_stack((x, y))

# Executar o algoritmo genético com as cidades fornecidas
algoritmo_genetico(cidades)