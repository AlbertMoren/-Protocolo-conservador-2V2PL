import utils
import tree

class LockTable:
    transaction_counter = 100  # Contador de transações (começa de 100).

    """
    Inicializa a tabela de bloqueios e associa a árvore do sistema para gerenciamento de objetos.
    """
    def __init__(self, tree: tree.Tree):
        self.locks = []
        self.tree = tree

    """
    Busca e retorna um bloqueio específico baseado no seu ID.
    """
    def getLock(self,lock_id):
        for lock in self.locks:
            if lock[0] == lock_id:
                return lock

    """
    Adiciona um novo bloqueio à tabela de bloqueios.
    O `lock_id` é gerado automaticamente baseado no número de bloqueios já existentes.
    - Busca o objeto correspondente na árvore e obtém seus pais e descendentes.
    - Adiciona bloqueios de intenção nos pais do objeto.
    - Adiciona bloqueios nos descendentes do objeto.
    """
    def add_lock(self, transaction_id,granulosidade, objeto_id, tipo_bloqueio, status):

        lock_id = len(self.locks) + 1  
        lock_entry = [lock_id, transaction_id, granulosidade, objeto_id, tipo_bloqueio, status]
        self.locks.append(lock_entry)

        # Busca o objeto correspondente na árvore e obtém seus pais e descendentes.
        obj_tupla = self.tree.find_obj(objeto_id)
        print('objeto_id: ', objeto_id)
        print('obj_tupla: ', obj_tupla)
        obj = self.tree.get_parent_obj(obj_tupla, granulosidade)

        parents = self.tree.get_parents_obj(obj)
        descendants = self.tree.get_descendants_obj(obj)

        # Adiciona bloqueios de intenção nos pais do objeto.
        for parent in parents:
            bloqueio_final = utils.SEM_BLOQUEIO

            if tipo_bloqueio == utils.BLOQUEIO_ESCRITA:
                bloqueio_final = utils.I_BLOQUEIO_ESCRITA
            elif tipo_bloqueio == utils.BLOQUEIO_LEITURA:
                bloqueio_final = utils.I_BLOQUEIO_LEITURA
            elif tipo_bloqueio == utils.BLOQUEIO_UPDATE:
                bloqueio_final = utils.I_BLOQUEIO_UPDATE
            elif tipo_bloqueio == utils.BLOQUEIO_CERTIFY:
                bloqueio_final = utils.I_BLOQUEIO_CERTIFY

            lock_id = len(self.locks) + 1           # Novo ID de bloqueio para os pais.

            self.locks.append([lock_id, transaction_id, granulosidade, parent.index, bloqueio_final, status])       
            parent.bloqueios.append(lock_id)        # Associa o bloqueio ao pai.

        
        # Adiciona bloqueios nos descendentes do objeto
        for descendant in descendants:
            lock_id = len(self.locks) + 1           # Novo ID de bloqueio para os descendentes.

            self.locks.append([lock_id, transaction_id, granulosidade, descendant.index, tipo_bloqueio, status])
            descendant.bloqueios.append(lock_id)    # Associa o bloqueio ao descendente.

    """
    Remove um bloqueio específico da tabela de bloqueios.
    - Remove o bloqueio do objeto e de seus pais e descendentes.
    - Remove o bloqueio de intenção dos pais.
    - Remove o bloqueio dos descendentes.
    - Remove o bloqueio da lista.
    """
    def remove_lock(self, lock_id):
        for lock in self.locks:
            if lock[0] == lock_id:
                lock_id, transaction_id, granulosidade, objeto_id, tipo_bloqueio, status = lock

                # Remove o bloqueio do objeto e de seus pais e descendentes.
                obj_tupla = self.tree.find_obj(objeto_id)
                obj = self.tree.get_parent_obj(obj_tupla, granulosidade)

                parents = self.tree.get_parents_obj(obj)
                descendants = self.tree.get_descendants_obj(obj)

                # Remove o bloqueio de intenção dos pais.
                for parent in parents:
                    if tipo_bloqueio == utils.BLOQUEIO_ESCRITA:
                        parent.bloqueios.remove(utils.I_BLOQUEIO_ESCRITA)
                    elif tipo_bloqueio == utils.BLOQUEIO_LEITURA:
                        parent.bloqueios.remove(utils.I_BLOQUEIO_LEITURA)
                    elif tipo_bloqueio == utils.BLOQUEIO_UPDATE:
                        parent.bloqueios.remove(utils.I_BLOQUEIO_UPDATE)
                    elif tipo_bloqueio == utils.BLOQUEIO_CERTIFY:
                        parent.bloqueios.remove(utils.I_BLOQUEIO_CERTIFY)
                
                # Remove o bloqueio dos descendentes.
                for descendant in descendants:
                    descendant.bloqueios.remove(tipo_bloqueio)
                
                # Remove o bloqueio da lista.
                self.locks.remove(lock)

                print(f"LockID {lock_id} removido com sucesso.")
                return
        print(f"LockID {lock_id} não encontrado.")
    
    """
    Remove todos os bloqueios associados a uma transação específica.
    - Coleta os IDs dos bloqueios que pertencem à transação.
    - Remove os bloqueios da lista que pertencem à transação.
    - Remove os bloqueios dos descendentes na árvore.
    """
    def remove_transactionID(self, transaction_id):
        original_length = len(self.locks)
        to_remove_locks_id = []

        # Coleta os IDs dos bloqueios que pertencem à transação.
        for lock in self.locks:
            if lock[1] == transaction_id:
                to_remove_locks_id.append(lock[0])

        # Remove os bloqueios da lista que pertencem à transação.
        self.locks = [lock for lock in self.locks if lock[1] != transaction_id]

        # Remove os bloqueios dos descendentes na árvore.
        descents = self.tree.get_descendants(self.tree.raiz)
        for desc in descents:
            for to_remove_lock_id in to_remove_locks_id:
                if to_remove_lock_id in desc.objeto.bloqueios:
                    desc.objeto.bloqueios.remove(to_remove_lock_id)

        if len(self.locks) < original_length:
            print(f"Transaction {transaction_id} removida com sucesso.")
        else:
            print(f"Transaction {transaction_id} não encontrada.")

    """
    # Exibe a tabela de bloqueios formatada.
    - Itera sobre a lista de bloqueios e exibe cada um deles.
    """
    def show_locks(self):
        header = f"{'LockID':<8} {'TransactionID':<14} {'Granulosidade':<14} {'objeto_id':<10} {'Tipo Bloqueio':<15} {'Status':<12}"
        print(header)
        print("-" * len(header))  
        
       
        for lock in self.locks:
            lock_id, transaction_id, granulosidade, objeto_id, tipo_bloqueio, status = lock
            print(f"{lock_id:<8} {transaction_id:<14} {granulosidade:<14} {objeto_id:<10} {tipo_bloqueio:<15} {status:<12}")