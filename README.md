# Aplicativo Bancário
Este projeto é um sistema de gerenciamento bancário desenvolvido em Python que simula operações com contas bancárias. Ele utiliza um banco de dados SQLite para persistência dos dados, o pacote SQLModel/SQLAlchemy para modelagem e manipulação dos dados, Tkinter para a interface gráfica e Matplotlib para a visualização do histórico de transações.

![appbancario](https://github.com/user-attachments/assets/ca00e8ee-477e-46fc-b49e-3038e92fd2ad)


## Funcionalidades
* Criar Conta: Cadastro de novas contas bancárias com validação para evitar duplicidade (mesmo banco e número).
* Listar Contas: Exibe todas as contas cadastradas no sistema.
* Atualizar Conta: Permite atualizar os dados de uma conta (exceto campos críticos, como o ID).
* Desativar Conta: Desativa uma conta se o saldo estiver zerado.
* Transferir Saldo: Realiza transferência de saldo entre contas, verificando saldo suficiente e a existência das contas.
* Movimentar Saldo: Registra transações (entradas ou saídas) em uma conta.
* Total de Contas: Calcula a soma dos saldos de todas as contas cadastradas.
* Buscar Histórico por Data: Filtra o histórico de transações entre duas datas específicas.
* Gerar Gráfico de Transações: Exibe um gráfico do histórico de transações (todas, somente entradas ou somente saídas) utilizando Matplotlib.

## Tecnologias Utilizadas
* Python 3.x
* SQLModel/SQLAlchemy: ORM para criação e manipulação do banco de dados.
* SQLite: Banco de dados leve para armazenamento das informações.
* Tkinter: Biblioteca padrão do Python para interfaces gráficas.
* Matplotlib: Biblioteca para criação de gráficos e visualizações.

## Uso
Na interface gráfica, você encontrará as seguintes opções:
* Criar Conta: Preencha os dados solicitados (banco, agência, número e saldo inicial) para cadastrar uma nova conta.
* Desativar Conta: Selecione uma conta com saldo zerado para desativá-la.
* Transferir Dinheiro: Selecione a conta de origem e a conta de destino, informe o valor e confirme a transferência.
* Movimentar Dinheiro: Registre transações de entrada ou saída em uma conta.
* Total de Contas: Exibe o total (soma dos saldos) de todas as contas cadastradas.
* Filtrar Histórico: Informe as datas inicial e final para filtrar o histórico de transações.
* Mostrar Gráfico: Exibe um gráfico das transações com base no filtro escolhido (todas, apenas entradas ou apenas saídas).

## Observações
* Validações: O sistema implementa diversas validações, como verificação de conta duplicada, saldo insuficiente para saídas e transferência, e somente permite desativar contas com saldo zero.
* Interface Gráfica: Desenvolvida com Tkinter, a interface facilita a interação do usuário com o sistema.
* Gráficos: A função de geração de gráfico permite a visualização do histórico de transações de forma intuitiva, utilizando o Matplotlib.

