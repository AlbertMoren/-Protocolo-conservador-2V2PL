import utils

# Função que cria as operações a partir do schedule
def cria_operacao(operacoes):
    operacao_objs = []
    id_count = 0
    
    for operacao, granulosidade in operacoes:
        T = int(operacao[1]) 

        if operacao[0] == 'r':
            op = utils.LEITURA
            obj_id = operacao[3:-1]
        elif operacao[0] == 'w':
            op = utils.ESCRITA
            obj_id = operacao[3:-1]
        elif operacao[0] == 'u':
            op = utils.UPDATE
            obj_id = operacao[3:-1]
        elif operacao[0] == 'c':
            op = utils.COMMIT
            obj_id = None

        if granulosidade == 'Banco':
            gra = utils.BANCO
        elif granulosidade == 'Area':
            gra = utils.AREA
        elif granulosidade == 'Tabela':
            gra = utils.TABELA
        elif granulosidade == 'Pagina':
            gra = utils.PAGINA
        elif granulosidade == 'Tupla':
            gra = utils.TUPLA
        elif granulosidade == None:
            gra = utils.PAGINA
        
        nova_operacao = utils.Operation(id_count, T, op, utils.Objeto(utils.TUPLA, obj_id), gra)
        operacao_objs.append(nova_operacao)
        id_count += 1 

    return operacao_objs


# Transforma o schedule recebido em uma lista de operações
def lista_operacoes(schedule_str):
    operacoes_str = schedule_str.replace(" ", "").split(",")
    
    operacoes_formatadas = []
    for operacao_gran in operacoes_str:
        if '-' in operacao_gran:
            operacao, granulosidade = operacao_gran.split("-")
        else:
            operacao = operacao_gran
            granulosidade = None

        operacoes_formatadas.append([operacao, granulosidade])
    
    transacoes = separa_transacoes(operacoes_formatadas)
    return operacoes_formatadas, transacoes

# Função que identifica as transações e suas respectivas operações
def separa_transacoes(operacoes):
    transacoes_dict = {}

    for operacao, _ in operacoes:
        transacao_id = operacao[1]
        if transacao_id not in transacoes_dict:
            transacoes_dict[transacao_id] = []
        transacoes_dict[transacao_id].append(operacao)
    
    return transacoes_dict

def main():
    schedule_str = input("Digite o schedule: ") 
    # Ex: w1(011) - Tupla, r2(110) - Pagina, r1(110) - Tabela, u1(110) - Banco, w2(011) - Tupla, u2(011) - Pagina, c2
    
    schedule, transacoes = lista_operacoes(schedule_str)
    operacoes = cria_operacao(schedule)
    
    print("\nOperações:")
    for operacao in operacoes:
        print(f"ID: {operacao.id}, Transação: T{operacao.T}, Operação: {operacao.op}, Granulosidade: {operacao.gra} | Objeto: {operacao.obj}")
    
    print("\nTransações:")
    for transacao, operacoes in transacoes.items():
        operacoes_formatadas = ", ".join(operacoes)
        print(f"Transação {transacao}: {operacoes_formatadas}")
    

main()