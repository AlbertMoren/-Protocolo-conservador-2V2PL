import Grafo
import tree
import syslockinfo
import utils


class Escalonador():
    def __init__(self, esquema:tree.Tree) -> None:
        #GERENCIAR
        self.escalonamento = list[utils.Operation]
        self.para_escalonar = list[utils.Operation]
        self.matrix = self.read_csv('matrix.csv')
        self.tree = esquema

        #ELEMENTOS
        self.syslockinfo = syslockinfo.LockTable(esquema)
        self.grafo = Grafo.Grafo()
        self.timestamp = {}

        self.count = 0

    """
    Tenta escalonar uma operação dada, verificando os bloqueios e determinando se a operação
    pode ser concedida ou precisa esperar.
    - Define o tipo de bloqueio necessário para a operação (leitura, escrita, update ou commit).
    - Verifica se a operação precisa ser bloqueada com base no tipo de operação e os bloqueios existentes.
    - Caso haja incompatibilidade de bloqueios, adiciona arestas ao grafo de deadlock e, se necessário, aborta transações.
    """
    def tentar_escalonar(self, op:utils.Operation):
        tipo_op = op.op
        bloqueio_requerido = utils.SEM_BLOQUEIO

        bloqueios_id = op.obj.bloqueios

        if not self.esta_no_timestamp(op.T):
            self.adicionar_no_timestamp(op.T)

        if tipo_op == utils.LEITURA:
            bloqueio_requerido = utils.BLOQUEIO_LEITURA
        elif tipo_op == utils.ESCRITA:
            bloqueio_requerido = utils.BLOQUEIO_ESCRITA
        elif tipo_op == utils.UPDATE:
            bloqueio_requerido = utils.BLOQUEIO_UPDATE
        elif tipo_op == utils.COMMIT:
            bloqueio_requerido = utils.BLOQUEIO_CERTIFY

            

        print(op.obj.bloqueios)
        print(self.syslockinfo.show_locks())
        if len(op.obj.bloqueios) > 0:
            for id_bloqueio in op.obj.bloqueios:
                
                lock_id, transaction_id, granulosidade, objeto_id, tipo_bloqueio, status = self.syslockinfo.getLock(id_bloqueio)

                #PEDINDO CERTIFY MAS TEM OUTRO BLOQUEIO QUE NÃO É CERTIFY
                if bloqueio_requerido == utils.BLOQUEIO_CERTIFY and tipo_bloqueio != utils.BLOQUEIO_CERTIFY:
                    self.syslockinfo.add_lock(op.T, op.gra, op.obj.index, bloqueio_requerido, utils.AGUARDANDO)
                
                #if (bloqueio_requerido == utils.BLOQUEIO_CERTIFY and tipo_bloqueio == utils.BLOQUEIO_CERTIFY) and (op.T == transaction_id):

                
                #COMPATIBILIDADE DE BLOQUEIOS
                if self.matrix[bloqueio_requerido][tipo_bloqueio]:
                    self.syslockinfo.add_lock(op.T, op.gra, op.obj.index, bloqueio_requerido, utils.CONCEDIDO)
                else:
                    #COMPATIBILIDADE DE DEADLOCK
                    if not self.grafo.adicionar_aresta(op.T, transaction_id):
                        T_menor_timestamp = self.get_max_timestamp(op.T, transaction_id)

                        self.abortar_transacao(T_menor_timestamp)

                    return 0
        
        self.syslockinfo.add_lock(op.T, op.gra, op.obj.index, bloqueio_requerido, utils.CONCEDIDO)

        return 1

    """
    Aborta uma transação, removendo-a da tabela de bloqueios.
    Essa função é chamada quando ocorre um deadlock e uma transação precisa ser eliminada.
    """    
    def abortar_transacao(self, T:int):
        self.syslockinfo.remove_transactionID(T)

    """
    Verifica se uma transação `T` já possui um timestamp atribuído.
    Retorna True se o timestamp já estiver no dicionário.
    """        
    def esta_no_timestamp(self, T:int):
        if str(T) in self.timestamp.keys():
            return True
        return False

    """
    Atribui um timestamp à transação `T`, armazenando a ordem de chegada da transação.
    Incrementa o contador `count` após adicionar o timestamp.
    """
    def adicionar_no_timestamp(self, T:int):
        self.timestamp[str(T)] = self.count
        self.count += 1
    """
    # Retorna o timestamp associado à transação `T` a partir do dicionário de timestamps.
    """
    def get_timestamp(self, T:int):
        return self.timestamp[str(T)]
    
    """
    Compara os timestamps de duas transações e retorna aquela com o maior timestamp.
    Isso é usado para determinar qual transação será abortada em um cenário de deadlock.
    """
    def get_max_timestamp(self, T1:int, T2:int):
        if self.get_timestamp(T1) < self.get_timestamp(T2):
            return T2
        return T1

    """
    Lê um arquivo CSV e retorna uma matriz de inteiros.
    Cada linha do arquivo CSV é convertida em uma lista de inteiros, representando a matriz de bloqueios.
    """
    def read_csv(self, filename):
        with open(filename, 'r') as file:
            data = []
            for line in file:
                # Remove espaços em branco e divide a linha em colunas
                row = line.strip().split(',')
                # Converte os valores para inteiros
                data.append([int(value) for value in row])
        return data

"""
Cria uma lista de operações associadas aos objetos da árvore.
Cada operação contém uma transação (T), o tipo de operação (leitura, escrita, update, commit),
e o objeto afetado. Essas operações serão usadas no processo de escalonamento.
"""
def criar_operacoes(tree: tree.Tree):
    operacoes = []
    
    # Operação 1: Transaction 1, LEITURA no Banco (Index: 1)
    obj1 = tree.find_obj(8)  # Banco
    op1 = utils.Operation(id=1, T=1, op=utils.LEITURA, obj=obj1, gra=utils.PAGINA)
    operacoes.append(op1)
    
    # Operação 2: Transaction 1, ESCRITA na Tabela 1 (Index: 4)
    obj2 = tree.find_obj(9)  # Tabela 1
    op2 = utils.Operation(id=2, T=1, op=utils.ESCRITA, obj=obj2, gra=utils.PAGINA)
    operacoes.append(op2)
    
    # Operação 3: Transaction 2, UPDATE na Página 1 (Index: 6)
    obj3 = tree.find_obj(9)  # Página 1
    op3 = utils.Operation(id=3, T=2, op=utils.UPDATE, obj=obj3, gra=utils.PAGINA)
    operacoes.append(op3)
    
    # Operação 4: Transaction 3, COMMIT na Tupla 1 (Index: 8)
    obj4 = tree.find_obj(13)  # Tupla 1
    op4 = utils.Operation(id=4, T=1, op=utils.COMMIT, obj=obj4, gra=utils.PAGINA)
    operacoes.append(op4)
    
    # Operação 5: Transaction 2, LEITURA na Tabela 2 (Index: 5)
    obj5 = tree.find_obj(10)  # Tabela 2
    op5 = utils.Operation(id=5, T=2, op=utils.LEITURA, obj=obj5, gra=utils.PAGINA)
    operacoes.append(op5)
    
    return operacoes



if __name__ == '__main__':
    arvore = tree.criar_tree()

    arvore.raiz.print_tree()
    operacores = criar_operacoes(arvore)
    esc = Escalonador(arvore)

    for op in operacores:
        print(op)
        esc.tentar_escalonar(op)
        print(esc.syslockinfo.locks)
        print()
        print()
