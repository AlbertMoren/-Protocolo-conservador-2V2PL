from Grafo import Grafo
from copy import deepcopy
import utils

# Função para ler um arquivo CSV


class Escalonador():
    def __init__(self) -> None:
        self.escalonamento = list[utils.Operation]
        self.para_escalonar = list[utils.Operation]
        self.matrix = self.read_csv('matrix.csv')

    # def escalonar(self, operations:list[utils.Operation]) -> None:
    #     self.para_escalonar = deepcopy(operations)

    def tentar_escalonar(self, op:utils.Operation):
        tipo_op = op.op
        bloqueio_requerido = -1
        bloqueio = op.obj.bloqueio
        compativel = True
        
        if tipo_op == utils.LEITURA:
            bloqueio_requerido = utils.BLOQUEIO_LEITURA
        elif tipo_op == utils.ESCRITA:
            bloqueio_requerido = utils.BLOQUEIO_ESCRITA
        elif tipo_op == utils.UPDATE:
            bloqueio_requerido = utils.BLOQUEIO_UPDATE
        elif tipo_op == utils.COMMIT:
            bloqueio_requerido = utils.BLOQUEIO_CERTIFY
        

        #COMPATIBILIDADE DE BLOQUEIOS
        if not self.matrix[bloqueio_requerido][bloqueio]:
            compativel = False
        
        #COMPATIBILIDADE DE DEADLOCK




    # def teste_compativel() -> bool:
        
    #     return False

    # def loop(self) -> None:
    #     for op in self.para_escalonar.reverse():

    def read_csv(self, filename):
        with open(filename, 'r') as file:
            data = []
            for line in file:
                # Remove espaços em branco e divide a linha em colunas
                row = line.strip().split(',')
                # Converte os valores para inteiros
                data.append([int(value) for value in row])
        return data

es = Escalonador()
