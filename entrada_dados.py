# importar as funcoes necessarias...

# Transforma o schedule recebido em uma lista de operações
def lista_operacoes(schedule_str):
    operacoes = schedule_str.replace(" ", "").split(",")
    transacoes(operacoes) # Printa as transações existentes
    return operacoes

# Função que identifica as transações e suas respectivas operações
def transacoes(operacoes):
    transacoes_dict = {}

    for operacao in operacoes:
        transacao_id = operacao[1]
        if transacao_id not in transacoes_dict:
            transacoes_dict[transacao_id] = []
        transacoes_dict[transacao_id].append(operacao)
    
    for transacao, operacoes in transacoes_dict.items():
        operacoes_formatadas = ", ".join(operacoes)
        print(f"Transação {transacao}: {operacoes_formatadas}")


def main():
    # Inicializando o banco de dados

    # Recebe o schedule do usuário
    schedule_str = input("Digite o schedule: ") # Exemplo: w1(x), r2(y), r1(y), ...
    schedule = lista_operacoes(schedule_str)
    # manda executar o schedule...
    

main()