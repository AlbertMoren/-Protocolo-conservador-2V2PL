
#TIPOS DE OPERAÇÕES
LEITURA = 0
ESCRITA = 1
UPDATE = 2
COMMIT = 3
ABORT = 4

#TIPO DE OBJETOS
BANCO = 0
AREA = 1
TABELA = 2 
PAGINA = 3
TUPLA = 4

#BLOQUEIOS
BLOQUEIO_LEITURA = 0
BLOQUEIO_ESCRITA = 1
BLOQUEIO_UPDATE = 2
BLOQUEIO_CERTIFY = 4

#CLASSE OBJETO
class Objeto():
    def __init__(self, tipo:int, index:int):
        self.index = index
        self.objeto = tipo
        self.parentes = {'Banco' : [], 'Area': [], 'Tabela': [], 'Pagina': [], 'Tupla': []}
        self.bloqueios = []
    
    def get_index(self) -> int:
        return self.index
    
    def __str__(self) -> str:
        return f"index = {self.index}, tipo = {self.objeto}"

#CLASSE OPERAÇÃO
class Operation():
    def __init__(self, id:int, T:int, op:int, obj:Objeto):
        self.id = id
        self.T = T
        self.op = op
        self.obj = obj