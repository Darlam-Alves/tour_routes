import pandas as pd
import heapq

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

def print_fila_prioridade(fila):
    while not fila.empty():
        item = fila.get()
        print(item)

def busca_a_estrela(grafo, nome_origem, nome_destino, min_pontos, pontos_visitados=[]):
    codigo_origem = nome_para_codigo(nome_origem, pontos_turisticos)
    codigo_destino = nome_para_codigo(nome_destino, pontos_turisticos)
    
    pontos_visitados.append(codigo_origem)
    
    if codigo_origem == codigo_destino:
        num_pontos = len(pontos_visitados)
        print(num_pontos)
        if  num_pontos >= min_pontos:
            return [codigo_para_nome(c, pontos_turisticos) for c in pontos_visitados]
        else:
            return None
    
    for vizinho in grafo[codigo_origem]:
        if vizinho not in pontos_visitados:
            caminho_encontrado = busca_a_estrela(grafo, codigo_para_nome(vizinho, pontos_turisticos), nome_destino, min_pontos, pontos_visitados.copy())
            if caminho_encontrado:
                return caminho_encontrado
    
    return None


def reconstruir_caminho(caminho, origem, destino, pontos_turisticos):
    caminho_percurso = []
    atual = destino
    while atual != origem:
        nome_atual = codigo_para_nome(atual, pontos_turisticos)
        caminho_percurso.append(nome_atual)
        atual = caminho[atual]
    caminho_percurso.append(codigo_para_nome(origem, pontos_turisticos))
    caminho_percurso.reverse()
    return caminho_percurso



if __name__ == "__main__":
    df = pd.read_csv('matriz_tempo_carro_horas.csv', index_col=0)
    
    pontos_proximos = encontrar_pontos_proximos(df)

    origem = "Sede da empresa (Ponto inicial)"
    destino = "Praça da República - Campo de Santana"

    #caminho = dfs(grafo, origem, destino)
    caminho_busca = busca_a_estrela(grafo, origem, destino, 10)
    if (caminho_busca):
        print(caminho_busca)
    else:
        print("não foi possível")

"""     for ponto, proximos in pontos_proximos.items():
        print("Os 5 pontos mais próximos a", ponto, "são:")
        print(proximos)  """

"""     if caminho:
        print(" -> ".join(caminho))
    else:
        print("caminho nao encontrado")  """ 
