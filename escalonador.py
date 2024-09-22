from typing import Protocol
from Grafo import Grafo
from copy import deepcopy
import utils

# Função para ler um arquivo CSV
def read_csv(filename):
    with open(filename, 'r') as file:
        data = []
        for line in file:
            # Remove espaços em branco e divide a linha em colunas
            row = line.strip().split(',')
            # Converte os valores para inteiros
            data.append([int(value) for value in row])
    return data

# Nome do arquivo CSV
filename = 'matrix.csv'

# Lê o CSV e armazena os dados
data = read_csv(filename)


class Escalonador():
    def __init__(self) -> None:
        self.escalonamento = list[utils.Operation]
        self.para_escalonar = list[utils.Operation]

    def escalonar(self, operations:list[utils.Operation]) -> None:
        self.para_escalonar = deepcopy(operations)

    def tentar_escalonar(self, op:utils.Operation):
        tipo_op = op.op
        bloqueios = op.obj.bloqueios

        #COMPATIBILIDADE DE BLOQUEIOS
        



    def teste_compativel() -> bool:
        
        return False

    def loop(self) -> None:
        for op in self.para_escalonar.reverse():



