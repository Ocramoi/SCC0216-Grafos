#!/usr/bin/env python3

import sys
import collections


class Grafo:
    nVerts = -1
    adjMatrix = [[]]

    def __init__(self, path: str):
        try:
            with open(path, "r") as arq:
                linhas = arq.readlines()
                self.nVerts = int(linhas[0].split()[1])
                self.adjMatrix = [([0] * self.nVerts)
                                  for _ in range(self.nVerts)]
                for i in range(2, len(linhas)):
                    j, k = [int(val) for val in linhas[i].split()]
                    self.adjMatrix[j - 1][k - 1] = \
                        self.adjMatrix[k - 1][j - 1] = \
                        1
        except FileNotFoundError:
            print("Erro! Arquivo não existente.")
            exit(1)
        except IndexError:
            print("Erro! Arquivo mal formatado.")
            exit(1)

    def exibeGrafo(self):
        """
        Com base na matriz dada (esperado N*N) exibe os elementos (i, j)
        rotulados.
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
        v -= 1
        dists = [-1] * self.nVerts
        visitados = []
        q = collections.deque()
        dists[v] = 0
        q.append(v)
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


def main():
    if len(sys.argv) > 1:
        g = Grafo(sys.argv[1])
    else:
        path = input("Arquivo .pajek a ser lido: ")
        g = Grafo(path)
    g.exibeGrafo()
    vertice = int(input("\tVértice para análise: "))
    print(g.bfs(vertice))


if __name__ == "__main__":
    main()
