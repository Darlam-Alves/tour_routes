import pandas as pd
import heapq
import queue as Q

tabela = pd.read_csv("pontos_turisticos-rio.csv")

# dicionario com {codigo, nome}
pontos_turisticos = {}


for index, row in tabela.iterrows():
    pontos_turisticos[row["Place ID"]] = row["Name"]

matriz_distancia = pd.read_csv("matriz_distancia_carro_km.csv", index_col=0)


# Função para adicionar uma aresta no grafo
def adicionar_aresta(grafo, origem, destino, peso):
    if origem not in grafo:
        grafo[origem] = {}
    grafo[origem][destino] = peso

# Função para criar o grafo a partir da matriz de distância
def criar_grafo(matriz_distancia):
    grafo = {}
    for index, row in matriz_distancia.iterrows():
        for col, value in row.items():
            peso = float(value.replace(',', '.'))
            adicionar_aresta(grafo, index, col, peso)
    return grafo

# Criar o grafo
grafo = criar_grafo(matriz_distancia)

def dfs(grafo, origem, destino, visitados=None, caminho=None):
    if visitados is None:
        visitados = set()
        
    if caminho is None:
        caminho = []

    caminhos_explorados = [] 
    visitados.add(origem)
    caminho.append(origem)

    if origem == destino:
        caminhos_explorados.append(caminho.copy())  
        return caminho

    for vizinho in grafo[origem]:
        if vizinho not in visitados:
            novo_caminho = dfs(grafo, vizinho, destino, visitados, caminho)
            if novo_caminho:
                caminhos_explorados.extend(novo_caminho)  
                return novo_caminho

    caminho.pop()
    return None

def encontrar_pontos_proximos(df):
    pontos_proximos = {}
    for ponto, distancias in df.iterrows():
        distancias = distancias.str.replace(',', '.').astype(float)  
        distancias_ordenadas = distancias.sort_values()
        pontos_mais_proximos = distancias_ordenadas.index[1:6] 
        pontos_proximos[ponto] = pontos_mais_proximos
    return pontos_proximos

def nome_para_codigo(nome, pontos_turisticos):
    for codigo, nome_ponto in pontos_turisticos.items():
        if nome_ponto == nome:
            return codigo
    return None  

def codigo_para_nome(codigo, pontos_turisticos):
    for codigo_ponto, nome_ponto in pontos_turisticos.items():
        if codigo_ponto == codigo:
            return nome_ponto
    return None

def distancia_real(codigo_origem, codigo_destino):
    matriz_distancias = pd.read_csv("matriz_distancia_carro_km.csv", index_col=0)
    matriz_distancias = matriz_distancias.replace(",", ".", regex=True)  # Substituir vírgulas por pontos
    distancia = pd.to_numeric(matriz_distancias.loc[codigo_origem, codigo_destino], errors='coerce')
    return distancia

def tempo_real(codigo_origem, codigo_destino):
    matriz_distancias = pd.read_csv("matriz_tempo_carro_horas.csv", index_col=0)
    matriz_distancias = matriz_distancias.replace(",", ".", regex=True)  # Substituir vírgulas por pontos
    tempo = pd.to_numeric(matriz_distancias.loc[codigo_origem, codigo_destino], errors='coerce')
    return tempo

def distancia_final(codigo_origem, codigo_destino):
    matriz_distancias = pd.read_csv("matriz_distancia_euclidiana.csv", index_col=0)
    matriz_distancias = matriz_distancias.replace(",", ".", regex=True)  # Substituir vírgulas por pontos
    distanciaEuclidiana = pd.to_numeric(matriz_distancias.loc[codigo_origem, codigo_destino], errors='coerce')
    return distanciaEuclidiana

def funcao_de_custo_real(codigo_origem, codigo_destino):
    dReal = distancia_real(codigo_origem, codigo_destino)
    tReal = tempo_real(codigo_origem, codigo_destino)
    resultado = (dReal*tReal) * (5.93 / 2.215)
    return resultado

def funcao_de_avaliacao(codigo_origem, codigo_destino):  
    dFinal = distancia_final(codigo_origem, codigo_destino)
    resultado = (5.93 / (2.215*90)) * (dFinal * dFinal)
    return resultado

def heuristica(codigo_origem, codigo_destino):
    custo_real = funcao_de_custo_real(codigo_origem, codigo_destino)
    avaliacao = funcao_de_avaliacao(codigo_origem, codigo_destino)
    total = custo_real + avaliacao
    return total

def getPriorityQueue(grafo, v, heuristics):
    q = Q.PriorityQueue()
    for node in grafo[v]:
        heuristica_node = heuristics[node]  # Supondo que 'heuristics' seja um dicionário de heurísticas
        comprimento_aresta = grafo[v][node]  # Supondo que o comprimento da aresta seja acessado dessa maneira
        prioridade = float(heuristica_node) + float(comprimento_aresta)
        q.put((prioridade, node))
    return q, len(grafo[v])

def busca_a_estrela(grafo, nome_origem, nome_destino, min_pontos):
    codigo_origem = nome_para_codigo(nome_origem, pontos_turisticos)
    codigo_destino = nome_para_codigo(nome_destino, pontos_turisticos)
    
    heuristics = {}  # Dicionário para armazenar as heurísticas de cada nó
    for node in grafo.keys():
        heuristics[node] = heuristica(codigo_origem, node)  # Calcular a heurística para cada nó
    
    visited = {}
    for node in grafo.keys():  
        visited[node] = False
    final_path = []
    goal = busca_a_estrela_util(grafo, codigo_origem, visited, final_path, codigo_destino, 0, heuristics)

def busca_a_estrela_util(grafo, v, visited, final_path, dest, goal, heuristics):
    if goal == 1:
        return goal
    visited[v] = True
    final_path.append(v)
    if v == dest:
        goal = 1
        caminho_nomes = [codigo_para_nome(c, pontos_turisticos) for c in final_path]  
        print("Caminho encontrado:", caminho_nomes)  
    else:
        pq, size = getPriorityQueue(grafo, v, heuristics)
        for i in range(size):
            heuristic, node = pq.get()
            if goal != 1:
                if not visited[node]:
                    goal = busca_a_estrela_util(grafo, node, visited, final_path, dest, goal, heuristics)
    return goal





if __name__ == "__main__":
    df = pd.read_csv('matriz_tempo_carro_horas.csv', index_col=0)
    
    pontos_proximos = encontrar_pontos_proximos(df)

    origem = "Sede da empresa (Ponto inicial)"
    destino = "Maracanã"
    #destino = "Cristo Redentor"
    #destino = "Parque Nacional da Tijuca"

    #caminho = dfs(grafo, origem, destino)
    busca_a_estrela(grafo, origem, destino, 20)
    

"""     for ponto, proximos in pontos_proximos.items():
        print("Os 5 pontos mais próximos a", ponto, "são:")
        print(proximos)  """

"""     if caminho:
        print(" -> ".join(caminho))
    else:
        print("caminho nao encontrado")  """ 
