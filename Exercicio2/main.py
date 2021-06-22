#!/usr/bin/env python3

import sys
import collections


class Grafo:
    nVerts = -1
    adjMatrix = [[]]

    def __init__(self, path: str):
        """
        Inicializa grafo com base no arquivo em [path]
        """
        try:
            # Abre arquivo pajek
            with open(path, "r") as arq:
                # Lê linhas
                linhas = arq.readlines()
                # Lê número de vértices do cabeçalho e
                # inicializa matriz de adjacência
                self.nVerts = int(linhas[0].split()[1])
                self.adjMatrix = [([0] * self.nVerts)
                                  for _ in range(self.nVerts)]
                # Popula matriz de adjacência a partir do arquivo
                for i in range(2, len(linhas)):
                    j, k = [int(val) for val in linhas[i].split()]
                    self.adjMatrix[j - 1][k - 1] = \
                        self.adjMatrix[k - 1][j - 1] = \
                        1
        # Trata Erros no arquivo
        except FileNotFoundError:
            print("Erro! Arquivo não existente.")
            exit(1)
        except IndexError as idxEr:
            print("Erro! Arquivo mal formatado.")
            print(idxEr)
            exit(1)

    def exibeGrafo(self):
        """
        Exibe matriz de adjacência do grafo formatada
        """
        N = len(self.adjMatrix)  # Tamanho do lado da matriz
        # Exibe rótulos de x
        print("\033[1m X |", " | ".join([str(x + 1)
                                         for x in range(N)]), "\033[0m")
        # Exibe rótulos e valores de cada linha em y
        for linhaN in range(len(self.adjMatrix)):
            print("\033[1m", "".join(["-"] * (4*(N + 1) - 2)), "\033[0m")
            print(f'\033[1m {linhaN + 1} | \033[0m', end="")
            print("\033[1m | \033[0m".join([str(x)
                                            for x in self.adjMatrix[linhaN]]))

    def bfs(self, v: int) -> [int]:
        """
        Busca em largura a partir do vértice [v] até todos os
        outros no grafo
        """
        # Transofrma índice
        v -= 1
        # Inicializa distâncias nulas
        dists = [-1] * self.nVerts
        # Variáveis auxiliares
        visitados = []
        q = collections.deque()
        dists[v] = 0
        # Adiciona vértice inicial à fila
        q.append(v)
        # Procedimento de busca entre a fila
        while len(q) > 0:
            atual = q.popleft()
            visitados.append(atual)
            for w in range(self.nVerts):
                if not self.adjMatrix[atual][w]:
                    continue
                if not (w in visitados):
                    dists[w] = dists[atual] + 1
                    q.append(w)
        return dists

    def dfs(self, vInicio: int, vFim: int) -> int:
        """
        Distância na busca em profundidade a partir de [vInicio] até [vFim]
        """
        # Inicializa vetor auxiliar de distâncias
        dists = [-1] * len(self.adjMatrix)
        return self._dfs(vInicio - 1, 0, dists, vFim - 1)

    def _dfs(self, atual: int, anterior: int,
             dists: [int], destino: int) -> int:
        """
        Implementação 'privada' da busca por profundidade recursiva
        """
        # Marca vértice atual
        dists[atual] = dists[anterior] + 1
        # Confere chegada
        if atual == destino:
            return dists[atual]
        # Procedimento de busca no vértice atual
        for adj in range(self.nVerts):
            if not self.adjMatrix[atual][adj]:
                continue
            if dists[adj] == -1:
                ret = self._dfs(adj, atual, dists, destino)
                if ret != -1:
                    return ret
        return -1


def main():
    # Lê e cria grafo a partir do arquivo dado na entrada
    if len(sys.argv) > 1:
        nomeArq = sys.argv[1]
    else:
        nomeArq = input()
    nomeArq = nomeArq.strip()
    g = Grafo(nomeArq)

    # g.exibeGrafo()

    # Cria matriz de distâncias por profundidade
    matrixDists = [([0] * g.nVerts) for _ in range(g.nVerts)]
    for i in range(g.nVerts):
        for j in range(i + 1, g.nVerts):
            matrixDists[i][j] = matrixDists[j][i] = g.dfs(i + 1, j + 1)
    # Exibe matriz de distâncias
    for linha in matrixDists:
        print(' '.join([str(x) for x in linha]))


if __name__ == "__main__":
    main()
