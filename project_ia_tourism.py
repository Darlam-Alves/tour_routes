import pandas as pd
tabela = pd.read_csv("pontos_turisticos-rio.csv")

# dicionario com {codigo, nome}
pontos_turisticos = {}


for index, row in tabela.iterrows():
    pontos_turisticos[row["Place ID"]] = row["Name"]

matriz_distancia = pd.read_csv("matriz_distancia_carro_km.csv", index_col=0)

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

# Função para encontrar os 5 pontos mais próximos a partir de cada ponto
def encontrar_pontos_proximos(df):
    pontos_proximos = {}
    for ponto, distancias in df.iterrows():
        distancias = distancias.str.replace(',', '.').astype(float)  
        distancias_ordenadas = distancias.sort_values()
        pontos_mais_proximos = distancias_ordenadas.iloc[1:6]  
        pontos_proximos[ponto] = pontos_mais_proximos
    return pontos_proximos

def nome_para_codigo(nome, pontos_turisticos):
    for codigo, nome_ponto in pontos_turisticos.items():
        if nome_ponto == nome:
            return codigo
    return None  


def distancia_real(codigo_origem, codigo_destino):
    # Ler o arquivo CSV com as distâncias
    matriz_distancias = pd.read_csv("matriz_distancia_carro_km.csv", index_col=0)

    # Obter a distância correspondente na matriz
    distancia = matriz_distancias.loc[codigo_origem, codigo_destino]

    return distancia



""" def tempo_real(codigo_origem, codigo_destino):



def distancia_final(codigo_origem, codigo_destino):



def funcao_de_custo_real(dReal, tReal):



def funcao_de_avaliacao(dFinal):  """


def busca_a_estrela(grafo, nome_origem, nome_destino, pontos_proximos, funcaoTotal):
    codigo_origem = nome_para_codigo(nome_origem, pontos_turisticos)
    codigo_destino = nome_para_codigo(nome_destino, pontos_turisticos)

    pontos_proximos_origem = pontos_proximos.get(codigo_origem, {})
    dReal = distancia_real(codigo_origem, codigo_destino)

    





"""     print("Os 5 pontos mais próximos à origem (", nome_origem, ") são:")
    for ponto, distancia in pontos_proximos_origem.items():
        print(ponto, distancia)

    print("\nOs 5 pontos mais próximos ao destino (", nome_destino, ") são:")
    for ponto, distancia in pontos_proximos_destino.items():
        print(ponto, distancia) """

   



if __name__ == "__main__":

     # Carregar o arquivo CSV
    df = pd.read_csv('matriz_tempo_carro_horas.csv', index_col=0)
    
    # Encontrar os 5 pontos mais próximos para cada ponto turístico
    pontos_proximos = encontrar_pontos_proximos(df)

    origem = "Sede da empresa (Ponto inicial)"
    destino = "Templo de Apolo"

    caminho = dfs(grafo, origem, destino)
    busca_a_estrela(grafo, origem, destino, pontos_proximos, 0)

"""     for ponto, proximos in pontos_proximos.items():
        print("Os 5 pontos mais próximos a", ponto, "são:")
        print(proximos)  """

"""     if caminho:
        print(" -> ".join(caminho))
    else:
        print("caminho nao encontrado")  """ 
