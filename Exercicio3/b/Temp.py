#!/usr/bin/env python3

import collections


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
