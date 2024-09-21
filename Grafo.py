class Grafo:
    def __init__(self):
        self.grafo = {}

    def adicionar_vertice(self, vertice):
        if vertice not in self.grafo:
            self.grafo[vertice] = []

    def adicionar_aresta(self, vertice_origem, vertice_destino):        
        if vertice_origem not in self.grafo:
            self.adicionar_vertice(vertice_origem)
        if vertice_destino not in self.grafo:
            self.adicionar_vertice(vertice_destino)
        self.grafo[vertice_origem].append(vertice_destino)
    
    def remover_vertice(self, vertice):
        if vertice in self.grafo:
            del self.grafo[vertice]
        for adjacencias in self.grafo.values():
            if vertice in adjacencias:
                adjacencias.remove(vertice)
    
    def _dfs(self, vertice, visitado, recursao_atual):
        visitado[vertice] = True
        recursao_atual[vertice] = True
        for vizinho in self.grafo.get(vertice, []):
            if not visitado[vizinho]:
                if self._dfs(vizinho, visitado, recursao_atual):
                    return True
            elif recursao_atual[vizinho]:
                return True

        recursao_atual[vertice] = False
        return False

    def tem_ciclo(self):
        visitado = {vertice: False for vertice in self.grafo}
        recursao_atual = {vertice: False for vertice in self.grafo}

        for vertice in self.grafo:
            if not visitado[vertice]:
                if self._dfs(vertice, visitado, recursao_atual):
                    return True
        return False