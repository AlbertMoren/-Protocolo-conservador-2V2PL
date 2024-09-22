import utils 
from utils import Objeto
from copy import deepcopy

# Definição da classe TreeNode
class TreeNode():
    def __init__(self, objeto: Objeto, father:'TreeNode' = None):
        self.objeto = objeto
        self.father = father
        self.children = []

    def add_child(self, child_node: 'TreeNode'):
        self.children.append(child_node)

    def print_tree(self, level=0):
        #tipos = {utils.BANCO: 'Banco', utils.AREA: 'Área', utils.TABELA: 'Tabela', utils.PAGINA: 'Página', utils.TUPLA: 'Tupla'}
        print('    ' * level + f"{utils.tipos[self.objeto.objeto]} (Index: {self.objeto.index})")
        for child in self.children:
            child.print_tree(level + 1)
    
    def __str__(self) -> str:
        return self.objeto.__str__()

class Tree:
    def __init__(self, raiz:TreeNode) -> None:
        self.raiz = raiz
    
    def find_obj(self, id_obj:int) -> Objeto:
        node = self.find_node(id_obj)

        if node == None:
            return None
        
        return node.objeto

    def find_node(self, id_node:int) -> TreeNode:
        return self.find_node_(self.raiz, id_node)
    
    def find_node_(self, node:TreeNode, id_node:int) -> TreeNode:
        if node.objeto.index == id_node:
            return node 
        
        if len(node.children) != 0:
            for filho in node.children:
                result = self.find_node_(filho, id_node)

                if result is not None:
                    return result

        return None
    
    def get_parents_obj(self, obj: Objeto) -> list[Objeto]:
        node = self.find_node(obj.index)

        if node == None:
            return None

        parents = [parent.objeto for parent in self.get_parents(node)]

        return parents

    def get_parents(self, node: TreeNode) -> list[TreeNode]:
        parents = []
        node_loop = node
        
        while node_loop.objeto.index != self.raiz.objeto.index:
            father = node_loop.father
            parents.append(father)
            node_loop = father
        
        return parents
    
    def get_descendants_obj(self, obj: Objeto) -> list[Objeto]:
        node = self.find_node(obj.index)

        if node == None:
            return None

        descendants = [descendant.objeto for descendant in self.get_descendants(node)]

        return descendants
    
    def get_descendants(self, node: TreeNode) -> list[TreeNode]:
        descendants = []

        if len(node.children) == 0:
            return []
        
        descendants.extend(node.children)

        for descendant in node.children:
            descendants.extend(self.get_descendants(descendant))

        return descendants
    
# Exemplo de uso
if __name__ == "__main__":
    # Criando os objetos
    banco_obj = Objeto(tipo=0, index=1)  # Banco
    area1_obj = Objeto(tipo=1, index=2)   # Área 1
    area2_obj = Objeto(tipo=1, index=3)   # Área 2
    tabela1_obj = Objeto(tipo=2, index=4) # Tabela 1
    tabela2_obj = Objeto(tipo=2, index=5) # Tabela 2
    pagina1_obj = Objeto(tipo=3, index=6) # Página 1
    tupla1_obj = Objeto(tipo=4, index=7)  # Tupla 1

    # Criando a árvore
    banco_node = TreeNode(objeto=banco_obj)
    area1_node = TreeNode(objeto=area1_obj, father=banco_node)
    area2_node = TreeNode(objeto=area2_obj, father=banco_node)
    tabela1_node = TreeNode(objeto=tabela1_obj, father=area1_node)
    tabela2_node = TreeNode(objeto=tabela2_obj, father=area1_node)
    pagina1_node = TreeNode(objeto=pagina1_obj, father=tabela1_node)
    tupla1_node = TreeNode(objeto=tupla1_obj, father=pagina1_node)

    # Montando a hierarquia
    banco_node.add_child(area1_node)
    banco_node.add_child(area2_node)
    area1_node.add_child(tabela1_node)
    area1_node.add_child(tabela2_node)
    tabela1_node.add_child(pagina1_node)
    pagina1_node.add_child(tupla1_node)

    # Criando a árvore
    tree = Tree(raiz=banco_node)

    # Imprimindo a árvore
    print("Estrutura da Árvore:")
    tree.raiz.print_tree()

    # Testando a busca
    search_id = 6
    found_obj = tree.find_obj(search_id)
    if found_obj:
        print(f"\nObjeto encontrado: {found_obj}")
    else:
        print("\nObjeto não encontrado.")

    # Obtendo pais da página
    descendants = tree.get_descendants_obj(banco_obj)
    parents = tree.get_parents_obj(banco_obj)

    print('DESCENDENTS')
    for descendant in descendants:
        print(descendant)
    
    print('PARENTS')
    for parent in parents:
        print(parent)


    