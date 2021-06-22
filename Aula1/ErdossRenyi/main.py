#!/usr/bin/env python3

from random import random


def exibeMatriz(matriz: [[int]]) -> None:
    """
    Com base na matriz dada (esperado N*N) exibe os elementos (i, j)
    rotulados.
    """
    N = len(matriz)  # Tamanho do lado da matriz
    # Exibe rótulos de x
    print("\033[1m X |", " | ".join([str(x + 1) for x in range(N)]), "\033[0m")
    # Exibe rótulos e valores de cada linha em y
    for linhaN in range(len(matriz)):
        print("\033[1m", "".join(["-"] * (4*(N + 1) - 2)), "\033[0m")
        print(f'\033[1m {linhaN + 1} | \033[0m', end="")
        print("\033[1m | \033[0m".join([str(x) for x in matriz[linhaN]]))


def erdosRenyi(N: int, p: float) -> [[int]]:
    """
    Gera matriz de grafo não direcional aleatório de acordo
    com o método Ersös-Renyi
    """
    matriz = [[0] * N for _ in range(N)]  # Gera matriz vazia (zerada)
    for i in range(N):
        for j in range(i + 1, N):
            # Popula cada elemento simetricamente
            r = random()
            if p < r:
                matriz[i][j] = matriz[j][i] = 1
    # Retorna matriz de grafo gerada
    return matriz


def grauVertice(matriz: [[int]], vertice: int) -> int:
    """
    Retorna o grau do [vertice] (início em 1) na [matriz]
    """
    # Inicializa grau
    grau = 0
    # Soma seu número de arestas a cada outro
    for no in matriz[vertice - 1]:
        grau += no
    return grau


def adjacentes(matriz: [[int]], vertice: int) -> [int]:
    """
    Retorna lista de vértices adjacentes ao [vertice] (início em 1) na [matriz]
    """
    # Inicializa adjacentes
    adjs = []

    # Confere vértice a vértice
    for i in range(len(matriz[vertice - 1])):
        if matriz[vertice - 1][i]:  # Adiciona adjacentes
            adjs.append(i + 1)

    return adjs


def existenciaAresta(matriz: [[int]], i: int, j: int) -> bool:
    """
    Retorna existência da aresta (i, j)
    """
    return True if matriz[i - 1][j - 1] else False


def main():
    # Lê e trata N, p
    N, p = (0, 2)
    while N <= 0 or p < 0 or p > 1:
        try:
            N = int(input("N (> 0): "))
            p = float(input("p (0 < p <= 1): "))
        except ValueError:
            print("Valor digitado inválido, favor redigite!")
    print("")

    # Gera e exibe grafo
    grafo = erdosRenyi(N, p)
    exibeMatriz(grafo)

    print("")
    # Lê vértice desejado
    v = 0
    while v <= 0 or v > N:
        try:
            v = int(input("Vértice a ser analisado ([1, {}]): ".format(N)))
        except ValueError:
            print("Valor digitado inválido, favor redigite!")

    # Informações relativas ao vértice
    print("\tGrau do vértice {}: {}".format(v,
                                            grauVertice(grafo, v)))
    print("\tVértices adjacentes a {}: {}".format(v,
                                                  adjacentes(grafo, v)))

    # Confere existência da aresta (i, j) passada no grafo
    print("Aresta (i, j) a conferir:")
    (i, j) = (0, 0)
    while (i <= 0 or i > N) or (j <= 0 or j > N):
        try:
            i = int(input("\ti ([1, {}]): ".format(N)))
            j = int(input("\tj ([1, {}]): ".format(N)))
        except ValueError:
            print("\tValor digitado inválido, favor redigite!")
    print("Aresta ({}, {}) {}existe!".format(i, j,
                                             "" if existenciaAresta(grafo, i, j)
                                             else "não "))


if __name__ == "__main__":
    main()
