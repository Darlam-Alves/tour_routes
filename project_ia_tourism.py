import pandas as pd

tabela = pd.read_csv("pontos_turisticos-rio.csv")

# dicionario com {codigo, nome}
pontos_turisticos = {}

for index, row in tabela.iterrows():
    pontos_turisticos[row["Place ID"]] = row["Name"]

matriz_distancia = pd.read_csv("matriz_indexada.csv", index_col=0)

# Tradução dos códigos dos pontos turísticos para nomes
matriz_distancia.rename(index=pontos_turisticos, columns=pontos_turisticos, inplace=True)

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
            adicionar_aresta(grafo, index, col, value)
    return grafo

# Criar o grafo
grafo = criar_grafo(matriz_distancia)

# Função de busca em profundidade (DFS)
def dfs(grafo, origem, destino, visitados=None, caminho=None):
    if visitados is None:
        visitados = set()
    if caminho is None:
        caminho = []
    visitados.add(origem)
    caminho.append(origem)
    if origem == destino:
        return caminho
    for vizinho in grafo[origem]:
        if vizinho not in visitados:
            novo_caminho = dfs(grafo, vizinho, destino, visitados, caminho)
            if novo_caminho:
                return novo_caminho
    caminho.pop()
    return None

origem = "Sede da empresa (Ponto inicial)"
destino = "Templo de Apolo"
caminho = dfs(grafo, origem, destino)

if caminho:
    print(" -> ".join(caminho))
else:
    print("caminho nao encontrado")
