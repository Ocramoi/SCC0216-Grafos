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
                    # Confere formatação da linha
                    if len(linhas[i].split()) != 2:
                        continue
                    j, k = [int(val) for val in linhas[i].split()]
                    self.adjMatrix[j - 1][k - 1] = 1
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


def checaCiclo(g: Grafo) -> bool:
    """
    Confere ciclo vértice a vértice
    """
    for vert in range(g.nVerts):
        for adj in range(g.nVerts):
            if g.adjMatrix[vert][adj] and g.dfs(adj + 1, vert + 1) > 0:
                return True
    return False


def main():
    # Lê nome do arquivo
    nomeArq = input()
    # Cria grafo com base no arquivo
    grafoLido = Grafo(nomeArq)
    # Exibe mensagem conforme existência de ciclo
    if checaCiclo(grafoLido):
        print("S")
    else:
        print("N")


if __name__ == "__main__":
    main()
