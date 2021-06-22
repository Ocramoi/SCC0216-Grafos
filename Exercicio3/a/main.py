#!/usr/bin/env python3

from GrafoND import Grafo


def main():
    # Lê nome do arquivo
    nomeArq = input()
    # Cria grafo com base no arquivo
    grafoLido = Grafo(nomeArq)
    # Vetor para tamanhos dos diferentes componentes
    # disconexos do grafo
    tamComponentes = []
    # Lista de vértices não visitados
    naoDescobertos = [_ for _ in range(grafoLido.nVerts)]

    # Enquanto há vértices não descobertos
    while len(naoDescobertos):
        # Inicia contagem de vértices do componente
        numComponente = 0
        # Realiza busca no primeiro elemento da lista
        arvr = grafoLido.dfsTodos(naoDescobertos[0] + 1)
        for vert in range(len(arvr)):
            # Contabiliza vértices descobertos
            if arvr[vert]["cor"] != grafoLido.cores["BRANCO"]:
                # Remove vértice da lista de não visitados
                naoDescobertos.remove(vert)
                # Atualiza número de vértices da componente
                numComponente += 1
        # Registra número de vértices do componente para exibição
        tamComponentes.append(numComponente)

    # Exibe número de componentes
    print(len(tamComponentes))
    # Exibe o tamamnho de cada componente em ordem decrescente
    for tam in sorted(tamComponentes, reverse=True):
        print(tam)


if __name__ == "__main__":
    main()
