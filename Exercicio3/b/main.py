#!/usr/bin/env python3

from GrafoDir import Grafo


def checaCiclo(g: Grafo) -> bool:
    for vert in range(g.nVerts):
        if g.detectaCiclo(vert + 1):
            return True
        # for adj in range(g.nVerts):
        #     if g.adjMatrix[vert][adj] and g.dfs(adj + 1, vert + 1) > 0:
        #         return True
    return False


def main():
    # Lê nome do arquivo
    nomeArq = input()
    # Cria grafo com base no arquivo
    grafoLido = Grafo(nomeArq)
    if checaCiclo(grafoLido):
        print("S")
    else:
        print("N")


if __name__ == "__main__":
    main()
