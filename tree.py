import utils 
from utils import Objeto 

# Definição da classe TreeNode
class TreeNode:
    def __init__(self, objeto: Objeto):
        self.objeto = objeto
        self.children = []

    def add_child(self, child_node: 'TreeNode'):
        self.children.append(child_node)

    def print_tree(self, level=0):
        #tipos = {utils.BANCO: 'Banco', utils.AREA: 'Área', utils.TABELA: 'Tabela', utils.PAGINA: 'Página', utils.TUPLA: 'Tupla'}
        print('    ' * level + f"{utils.tipos[self.objeto.objeto]} (Index: {self.objeto.index})")
        for child in self.children:
            child.print_tree(level + 1)

class Tree:
    def __init__(self, raiz:TreeNode) -> None:
        self.raiz = raiz
    
    def find_obj(self, id_obj:int):
        node = self.find_node(id_obj)

        if node == None:
            return None
        
        return node.objeto

    def find_node(self, id_node:int):
        return self.find_node_(self.raiz, id_node)
    
    def find_node_(self, node:TreeNode, id_node:int):
        if node.objeto.index == id_node:
            return node 
        
        if len(node.children) != 0:
            for filho in node.children:
                result = self.find_node_(filho, id_node)

                if result is not None:
                    return result

        return None

# Construindo a árvore
banco_obj = Objeto(tipo=1, index=1)
banco_node = TreeNode(banco_obj)
tree = Tree(banco_node)

# Adicionando Áreas
area1_obj = Objeto(tipo=2, index=2)
area1_node = TreeNode(area1_obj)
banco_node.add_child(area1_node)

area2_obj = Objeto(tipo=2, index=3)
area2_node = TreeNode(area2_obj)
banco_node.add_child(area2_node)

# Adicionando Tabelas à Área1
tabela1_obj = Objeto(tipo=3, index=4)
tabela1_node = TreeNode(tabela1_obj)
area1_node.add_child(tabela1_node)

tabela2_obj = Objeto(tipo=3, index=5)
tabela2_node = TreeNode(tabela2_obj)
area1_node.add_child(tabela2_node)

# Adicionando Páginas à Tabela1
pagina1_obj = Objeto(tipo=4, index=6)
pagina1_node = TreeNode(pagina1_obj)
tabela1_node.add_child(pagina1_node)

pagina2_obj = Objeto(tipo=4, index=7)
pagina2_node = TreeNode(pagina2_obj)
tabela1_node.add_child(pagina2_node)

# Adicionando Tuplas à Página1
tupla1_obj = Objeto(tipo=5, index=8)
tupla1_node = TreeNode(tupla1_obj)
pagina1_node.add_child(tupla1_node)

tupla2_obj = Objeto(tipo=5, index=9)
tupla2_node = TreeNode(tupla2_obj)
pagina1_node.add_child(tupla2_node)

# Adicionando Tuplas à Página2
tupla3_obj = Objeto(tipo=5, index=10)
tupla3_node = TreeNode(tupla3_obj)
pagina2_node.add_child(tupla3_node)

tupla4_obj = Objeto(tipo=5, index=11)
tupla4_node = TreeNode(tupla4_obj)
pagina2_node.add_child(tupla4_node)

# (Opcional) Adicionando Páginas e Tuplas à Tabela2
pagina3_obj = Objeto(tipo=4, index=12)
pagina3_node = TreeNode(pagina3_obj)
tabela2_node.add_child(pagina3_node)

tupla5_obj = Objeto(tipo=5, index=13)
tupla5_node = TreeNode(tupla5_obj)
pagina3_node.add_child(tupla5_node)

# Imprimindo a árvore completa
banco_node.print_tree()

print(tree.find_obj(11))