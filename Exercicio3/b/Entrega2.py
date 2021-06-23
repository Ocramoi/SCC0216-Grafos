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

    def detectaCiclo(self, vInicio: int) -> bool:
        """
        Realiza DFS a partir da aresta [vInicio] ([1, ...])
        checando por aresta de retorno
        """
        # Inicializa vetor de valores para cada vértice
        valores = [self.cores["BRANCO"] for _ in range(self.nVerts)]
        # Inicia busca recursiva e retorna presença de ciclo
        return self._detectaCiclo(vInicio - 1, valores)[0]

    def _detectaCiclo(self,
                      atual: int,
                      valores: [int]) -> [bool, [int]]:
        """
        Implementação 'privada' da busca por profundidade recursiva
        checando por aresta
        """
        # Atualiza cor para vértice descoberto
        valores[atual] = self.cores["CINZA"]
        # Para todos os vértices
        for adj in range(self.nVerts):
            # Cria cópia local dos valores
            estat = [val for val in valores]
            # Garante aresta entre o atual
            if not self.adjMatrix[atual][adj]:
                continue
            # Caso vértice não descoberto
            if valores[adj] == self.cores["BRANCO"]:
                # Chama recursivamente no vértice com cópia local de valores
                # conferindo por ciclo em todas as chamadas
                ret = self._detectaCiclo(adj, estat)[0]
                if ret:
                    return [True, valores]
            # Caso aresta de retorno (voltando a vértice descoberto)
            else:
                return [True, valores]

        # Atualiza situação do vértice e retorna falso + valores achados
        valores[atual] = self.cores["PRETO"]
        return [False, valores]


def checaCiclo(g: Grafo) -> bool:
    """
    Checa ciclo em cada vértice
    """
    for vert in range(g.nVerts):
        if g.detectaCiclo(vert + 1):
            return True
    return False


def main():
    # Lê nome do arquivo
    nomeArq = input()
    # Cria grafo com base no arquivo
    grafoLido = Grafo(nomeArq)
    # Checa ciclos e exibe correspondentemente
    if checaCiclo(grafoLido):
        print("S")
    else:
        print("N")


if __name__ == "__main__":
    main()
