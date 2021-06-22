#!/usr/bin/env python3

class Grafo:
    nVerts = -1
    adjMatrix = [[]]

    cores = {
        "BRANCO": 0,
        "CINZA": 1,
        "PRETO": 2
    }

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

    def dfsTodos(self, vInicio: int) -> [[int]]:
        """
        Retorna ("cor", "tempoDescoberta", "tempoFinal", "antecessor")
        para cada vértice do grafo referente a pesquisa em profundidade
        a partir de [vInicio] ([1, ...])
        """
        # Inicializa vetor de valores para cada vértice
        valores = []
        for _ in range(len(self.adjMatrix)):
            valores.append({
                "cor": self.cores["BRANCO"],
                "tempoDescoberta": None,
                "tempoFinal": None,
                "antecessor": None
            })
        # Inicia tempo de descoberta
        time = 0
        # Inicia busca recursiva e retorna valores de vértices
        return self._dfsTodos(vInicio - 1, valores, time)[1]

    def _dfsTodos(self,
                  atual: int,
                  valores: [int],
                  time: int) -> [int, [int]]:
        """
        Implementação 'privada' da busca por profundidade recursiva
        """
        # Atualiza tempo
        time += 1
        # Registra tempo de descoberta do vértice
        valores[atual]["tempoDescoberta"] = time
        # Atualiza cor para vértice descoberto
        valores[atual]["cor"] = self.cores["CINZA"]
        # Para todos os vértices
        for adj in range(self.nVerts):
            # Garante aresta entre o atual
            if not self.adjMatrix[atual][adj]:
                continue
            # Caso vértice não descoberto
            if valores[adj]["cor"] == self.cores["BRANCO"]:
                # Registra antecessor da busca
                valores[adj]["antecessor"] = atual
                # Atualiza tempo e valores chamando recursivamente
                # no vértice descoberto
                time, valores = self._dfsTodos(adj, valores, time)
        # Registra final de pesquisa no vértice atual
        valores[atual]["cor"] = self.cores["PRETO"]
        time += 1
        valores[atual]["tempoFinal"] = time

        # Retorna tempo e valores dos vértices
        return [time, valores]


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
