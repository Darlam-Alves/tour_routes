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

def dfs(grafo, origem, destino, visitados=None, caminho=None):
    if visitados is None:
        visitados = set()
    if caminho is None:
        caminho = []
    caminhos_explorados = []  # Adiciona essa linha
    visitados.add(origem)
    caminho.append(origem)
    if origem == destino:
        caminhos_explorados.append(caminho.copy())  # Adiciona essa linha
        return caminho
    for vizinho in grafo[origem]:
        if vizinho not in visitados:
            novo_caminho = dfs(grafo, vizinho, destino, visitados, caminho)
            if novo_caminho:
                caminhos_explorados.extend(novo_caminho)  # Adiciona essa linha
                return novo_caminho
    caminho.pop()
    return None

# Função para encontrar os 5 pontos mais próximos a partir de cada ponto
def encontrar_pontos_proximos(df):
    pontos_proximos = {}
    for ponto, distancias in df.iterrows():
        distancias = distancias.str.replace(',', '.').astype(float)  
        distancias_ordenadas = distancias.sort_values()
        pontos_mais_proximos = distancias_ordenadas.iloc[1:6]  
        pontos_proximos[ponto] = pontos_mais_proximos
    return pontos_proximos

if __name__ == "__main__":

     # Carregar o arquivo CSV
    df = pd.read_csv('tempo_carro.csv', index_col=0)
    
    # Encontrar os 5 pontos mais próximos para cada ponto turístico
    pontos_proximos = encontrar_pontos_proximos(df)

    origem = "Sede da empresa (Ponto inicial)"
    destino = "Templo de Apolo"
    caminho = dfs(grafo, origem, destino)

"""     for ponto, proximos in pontos_proximos.items():
        print("Os 5 pontos mais próximos a", ponto, "são:")
        print(proximos) """

    """ if caminho:
        print(" -> ".join(caminho))
    else:
        print("caminho nao encontrado") """
