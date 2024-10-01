# Escalonador de Transações com Controle de Concorrência 2V2PL

Trabalho final da disciplina de Sistemas de Gerenciamento de Banco de Dados, realizado em grupo, no qual devemos implementar um escalonador de transações com controle de concorrência utilizando o **protocolo Two-Version Two-Phase Locking (2V2PL)**. O objetivo é verificar se um escalonamento de transações é válido, detectando deadlocks e gerenciando bloqueios de leitura e escrita em um banco de dados.

## Funcionalidades

- **Bloqueios de Leitura e Escrita**: Implementação de bloqueios de leitura (`RL`), escrita (`WL`), e certificação (`Certify`) com base no protocolo 2V2PL.
- **Grafo de Espera**: Detecção de deadlocks utilizando um grafo de espera das transações.
- **Abortamento de Transações**: Em caso de deadlock, a transação mais recente é abortada para liberar os recursos.
- **Compatibilidade com múltiplas operações**: Leitura (`R`), Escrita (`W`), Atualização (`U`), e Commit (`C`) são suportadas.


## Estrutura do Projeto

- `entrada_dados.py`: Arquivo que aceita como entrada um schedule S de transações, o decodifica e, após isso, envia para o escalonador.
- `escalonador.py`:  Arquivo principal, faz a verificação de cada operação, indica o devido bloqueio para tal, e envia os dados para o syslockinfo.
- `Grafo.py`: Arquivo responsável por verificar se o schedule é serializável por conflito, analisando se há ciclos.
- `syslockinfo.py`: Responsável por representar como as transações estão sendo aplicadas sobre os objetos
- `tree.py`:  Estrutura de dados responsável por mapear a arquitetura de nossa tabela, sendo o nó raiz o banco, até as folhas que são as tuplas.
- `utils.py`: Classe responsável por estruturar as transações.

