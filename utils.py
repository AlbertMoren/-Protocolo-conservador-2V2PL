
#TIPOS DE OPERAÇÕES
LEITURA = 0
ESCRITA = 1
UPDATE = 2
COMMIT = 3

#TIPO DE OBJETOS
BANCO = 1
AREA = 2
TABELA = 3
PAGINA = 4
TUPLA = 5

#CONVERSÃO OBJETO
tipos = {BANCO: 'Banco', AREA: 'Área', TABELA: 'Tabela', PAGINA: 'Página', TUPLA: 'Tupla'}

#BLOQUEIOS
BLOQUEIO_LEITURA = 0
BLOQUEIO_ESCRITA = 1
BLOQUEIO_UPDATE = 2
BLOQUEIO_CERTIFY = 4
I_BLOQUEIO_LEITURA = 5
I_BLOQUEIO_ESCRITA = 6
I_BLOQUEIO_UPDATE = 7
I_BLOQUEIO_CERTIFY = 8


#status
CONCEDIDO = 1
CONVERTENDO = 2
AGUARDANDO = 3

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
        return f"index = {self.index}, tipo = {tipos[self.objeto]}"

#CLASSE OPERAÇÃO
class Operation():
    def __init__(self, id:int, T:int, op:int, obj:Objeto):
        self.id = id
        self.T = T
        self.op = op
        self.obj = obj
        