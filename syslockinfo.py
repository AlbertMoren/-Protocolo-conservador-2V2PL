import os
import time
import utils

class LockTable:
    transaction_counter = 100  

    def __init__(self):
        self.locks = []

    
    def add_lock(self, transaction_id,granulosidade, tupla_id, tipo_bloqueio, status):
        lock_id = len(self.locks) + 1  

        lock_entry = [lock_id, transaction_id, granulosidade, tupla_id, tipo_bloqueio, status]
        self.locks.append(lock_entry)

    def remove_lock(self, lock_id):
        for lock in self.locks:
            if lock[0] == lock_id:
                self.locks.remove(lock)
                print(f"LockID {lock_id} removido com sucesso.")
                return
        print(f"LockID {lock_id} não encontrado.")

    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

   
    def show_locks(self):
        time.sleep(2)
        self.clear_screen()

        header = f"{'LockID':<8} {'TransactionID':<14} {'Granulosidade':<14} {'Tupla ID':<10} {'Tipo Bloqueio':<15} {'Status':<12}"
        print(header)
        print("-" * len(header))  
        
       
        for lock in self.locks:
            lock_id, transaction_id, granulosidade, tupla_id, tipo_bloqueio, status = lock
            print(f"{lock_id:<8} {transaction_id:<14} {granulosidade:<14} {tupla_id:<10} {tipo_bloqueio:<15} {status:<12}")


lock_table_instance = LockTable()


lock_table_instance.add_lock('2',f'{utils.TABELA}', '2', f'{utils.LEITURA}', f'{utils.CONCEDIDO}')
lock_table_instance.add_lock('3',f'{utils.TUPLA}', '3', f'{utils.ESCRITA}', f'{utils.AGUARDANDO}')
lock_table_instance.add_lock('4',f'{utils.PAGINA}', '4', f'{utils.LEITURA}', f'{utils.CONCEDIDO}')


lock_table_instance.show_locks()
