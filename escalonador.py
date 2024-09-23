import Grafo
from copy import deepcopy
import tree
import syslockinfo
import utils

# Função para ler um arquivo CSV


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

    # def escalonar(self, operations:list[utils.Operation]) -> None:
    #     self.para_escalonar = deepcopy(operations)

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
        
    def abortar_transacao(self, T:int):
        self.syslockinfo.remove_transactionID(T)
            
    def esta_no_timestamp(self, T:int):
        if str(T) in self.timestamp.keys():
            return True
        return False

    def adicionar_no_timestamp(self, T:int):
        self.timestamp[str(T)] = self.count
        self.count += 1
    
    def get_timestamp(self, T:int):
        return self.timestamp[str(T)]
    
    def get_max_timestamp(self, T1:int, T2:int):
        if self.get_timestamp(T1) < self.get_timestamp(T2):
            return T2
        return T1

    def read_csv(self, filename):
        with open(filename, 'r') as file:
            data = []
            for line in file:
                # Remove espaços em branco e divide a linha em colunas
                row = line.strip().split(',')
                # Converte os valores para inteiros
                data.append([int(value) for value in row])
        return data

# tree.py (continuação)

# Função para criar operações
def criar_operacoes(tree: tree.Tree):
    """
    Cria e retorna uma lista de operações associadas aos objetos na árvore.

    Args:
        tree (Tree): A árvore onde as operações serão aplicadas.

    Returns:
        List[Operation]: Lista de instâncias de Operation.
    """
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
    
    #
    #esc.tentar_escalonar()