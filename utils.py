"""
Definição dos tipos de operações possíveis
"""
LEITURA = 0
ESCRITA = 1
UPDATE = 2
COMMIT = 3

"""
Definição dos tipos de objetos em um sistema hierárquico (banco de dados)
"""
BANCO = 0
AREA = 1
TABELA = 2
PAGINA = 3
TUPLA = 4

"""
Dicionário para conversão de tipo de objeto para uma string representativa
"""
tipos = {BANCO: 'Banco', AREA: 'Área', TABELA: 'Tabela', PAGINA: 'Página', TUPLA: 'Tupla'}

"""
 Definição dos diferentes tipos de bloqueios que podem ser aplicados a objetos
"""
SEM_BLOQUEIO = -1
BLOQUEIO_LEITURA = 0
BLOQUEIO_ESCRITA = 1
BLOQUEIO_UPDATE = 2
BLOQUEIO_CERTIFY = 4
I_BLOQUEIO_LEITURA = 5
I_BLOQUEIO_ESCRITA = 6
I_BLOQUEIO_UPDATE = 7
I_BLOQUEIO_CERTIFY = 8

"""
Definição dos possíveis status de uma operação de bloqueio
"""
CONCEDIDO = 1
CONVERTENDO = 2
AGUARDANDO = 3

"""
Definição da classe `Objeto`, que representa um objeto no sistema, como uma tabela, página ou tupla
"""
class Objeto():
    """
    Inicializa um objeto com um tipo (banco, área, tabela, etc.) e um índice único.

    Args:
        tipo (int): O tipo do objeto, baseado nas constantes BANCO, AREA, TABELA, etc.
        index (int): O índice único que identifica o objeto.
    """
    def __init__(self, tipo:int, index:int):
        self.index = index
        self.objeto = tipo
        self.bloqueios = []
    
    """
    Retorna o índice do objeto.
    """
    def get_index(self) -> int:
        return self.index
    
    """
    Retorna uma representação em string do objeto, mostrando seu índice e tipo.
    """
    def __str__(self) -> str:
        return f"index = {self.index}, tipo = {tipos[self.objeto]}"

"""
Definição da classe `Operation`, que representa uma operação realizada sobre um objeto
"""
class Operation():
    def __init__(self, id:int, T:int, op:int, obj:Objeto, gra: int):
        self.id = id
        self.T = T
        self.op = op
        self.obj = obj
        self.gra = gra
        