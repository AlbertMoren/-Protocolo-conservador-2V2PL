from typing import Protocol
from Grafo import Grafo
from copy import deepcopy
import utils

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

