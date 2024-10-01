class Grafo:
    """
    Inicializa um grafo vazio representado por um dicionário.
    As chaves são os vértices, e os valores são listas que armazenam os vértices adjacentes (arestas).
    """
    def __init__(self):
        self.grafo = {}

    """
    Adiciona um novo vértice ao grafo, caso ele ainda não exista.
    Cada vértice é uma chave no dicionário `grafo`, e o valor é uma lista de adjacências.
    """
    def adicionar_vertice(self, vertice):
        if vertice not in self.grafo:
            self.grafo[vertice] = []

    """
    # Função auxiliar que implementa a busca em profundidade (DFS) para detectar ciclos.
    Marca o vértice atual como visitado e presente na pilha de recursão.
    Para cada vizinho do vértice, realiza a DFS recursiva:
    - Se o vizinho não foi visitado, faz a DFS nele.
    - Se o vizinho está na pilha de recursão, significa que existe um ciclo.
    Após processar todos os vizinhos, remove o vértice da pilha de recursão.
    """
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

    """
    Verifica se o grafo contém ciclos utilizando DFS.
    Cria dois dicionários:
    - `visitado`: para marcar os vértices já processados.
    - `recursao_atual`: para verificar se um vértice está presente na pilha de recursão da DFS.
    Para cada vértice, chama a função `_dfs` para detectar ciclos. Se um ciclo for encontrado, retorna True.
    """
    def tem_ciclo(self):
        visitado = {vertice: False for vertice in self.grafo}
        recursao_atual = {vertice: False for vertice in self.grafo}

        for vertice in self.grafo:
            if not visitado[vertice]:
                if self._dfs(vertice, visitado, recursao_atual):
                    return True
        return False

    """
    Adiciona uma aresta dirigida do vértice de origem ao vértice de destino no grafo.
    - Se a origem ou o destino ainda não estão no grafo, os adiciona como novos vértices.
    - Após adicionar a aresta, verifica se a inclusão gerou um ciclo:
    - Se gerou, remove a aresta e retorna 0.
    - Se não gerou, mantém a aresta e retorna 1.
    """
    def adicionar_aresta(self, vertice_origem, vertice_destino):
        if vertice_origem not in self.grafo:
            self.adicionar_vertice(vertice_origem)
        if vertice_destino not in self.grafo:
            self.adicionar_vertice(vertice_destino)

        self.grafo[vertice_origem].append(vertice_destino)

        if self.tem_ciclo():
            self.grafo[vertice_origem].remove(vertice_destino)
            return 0
        else:
            return 1    