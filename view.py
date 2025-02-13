from models import Conta, engine, Historico, Tipos
from sqlmodel import Session, select
import matplotlib.pyplot as plt 

def criar_conta(conta: Conta):
    with Session(engine) as session:
        # Validação: verifica se já existe uma conta com o mesmo banco e número
        statement = select(Conta).where(
            (Conta.banco == conta.banco) & (Conta.numero == conta.numero)
        )
        resultado = session.exec(statement).one_or_none()
        if resultado:
            return "Conta já cadastrada"
        session.add(conta)
        session.commit()
        return "Conta criada com sucesso"

def listar_contas():
    with Session(engine) as session:
        statement = select(Conta)
        resultados = session.exec(statement).all()
    # Converte cada objeto Conta para dicionário, útil para serialização (ex.: API)
    return [conta.dict() for conta in resultados]

def desativar_conta(id: int):
    with Session(engine) as session:
        try:
            statement = select(Conta).where(Conta.id == id)
            conta = session.exec(statement).one_or_none()
            
            if not conta:
                return "Conta não encontrada"
            
            # Verifica se a conta possui saldo zerado para ser desativada
            if conta.saldo != 0:
                return f"Conta não pode ser desativada, saldo atual: {conta.saldo}"
            
            session.delete(conta)
            session.commit()
            return "Conta desativada com sucesso"
        
        except Exception as e:
            session.rollback()
            return f"Erro ao desativar conta: {str(e)}"

def atualizar_conta(id: int, conta: Conta):
    with Session(engine) as session:
        try:
            statement = select(Conta).where(Conta.id == id)
            conta_atual = session.exec(statement).one_or_none()
            
            if not conta_atual:
                return "Conta não encontrada"
            
            # Atualiza apenas os atributos que foram informados, excluindo campos críticos como 'id'
            dados_atualizados = conta.dict(exclude_unset=True, exclude={"id"})
            for chave, valor in dados_atualizados.items():
                setattr(conta_atual, chave, valor)
            
            session.commit()
            return "Conta atualizada com sucesso"
        
        except Exception as e:
            session.rollback()
            return f"Erro ao atualizar conta: {str(e)}"

def transferir_saldo(id_origem: int, id_destino: int, valor: float):
    # Validação: valor da transferência deve ser positivo
    if valor <= 0:
        return "Valor de transferência deve ser positivo"
    
    with Session(engine) as session:
        try:
            statement_origem = select(Conta).where(Conta.id == id_origem)
            conta_origem = session.exec(statement_origem).one_or_none()
            
            statement_destino = select(Conta).where(Conta.id == id_destino)
            conta_destino = session.exec(statement_destino).one_or_none()
            
            if not conta_origem:
                return "Conta de origem não encontrada"
            
            if not conta_destino:
                return "Conta de destino não encontrada"
            
            if conta_origem.saldo < valor:
                return "Saldo insuficiente"
            
            # Realiza a transferência de forma atômica
            conta_origem.saldo -= valor
            conta_destino.saldo += valor
            session.commit()
            return "Transferência realizada com sucesso"
        
        except Exception as e:
            session.rollback()
            return f"Erro ao transferir saldo: {str(e)}"

def movimentar_saldo(id_conta: int, valor: float, tipo: str):
    with Session(engine) as session:
        try:
            statement = select(Conta).where(Conta.id == id_conta)
            conta = session.exec(statement).one_or_none()
            
            if not conta:
                return "Conta não encontrada"
            
            if tipo.lower() == "entrada":
                conta.saldo += valor
            elif tipo.lower() == "saída":
                if conta.saldo < valor:
                    return "Saldo insuficiente"
                conta.saldo -= valor
            else:
                return "Tipo de movimentação inválido"
            
            session.commit()
            return "Movimentação realizada com sucesso"
        
        except Exception as e:
            session.rollback()
            return f"Erro ao movimentar saldo: {str(e)}"
        
def total_contas():
    with Session(engine) as session:
        statement = select(Conta)
        contas = session.exec(statement).all()
        total = sum([conta.saldo for conta in contas])
    return total

def buscar_historicos_entre_datas(data_inicial, data_final):
    with Session(engine) as session:
        statement = select(Historico).where(
            (Historico.data >= data_inicial) & (Historico.data <= data_final)
        )
        historicos = session.exec(statement).all()
    return [historico.dict() for historico in historicos]

def gerar_grafico_historico():
    # Exibe as opções para o usuário escolher o filtro desejado
    print("Selecione o que deseja visualizar:")
    print("1 - Todas as transações")
    print("2 - Apenas entradas")
    print("3 - Apenas saídas")
    opcao = input("Digite a opção desejada (1, 2 ou 3): ")

    # Define o filtro com base na opção escolhida
    filtro = None
    if opcao == "2":
        filtro = Tipos.ENTRADA
    elif opcao == "3":
        filtro = Tipos.SAIDA

    # Abre uma sessão com o banco de dados
    with Session(engine) as session:
        # Cria a consulta inicial para todos os registros de histórico
        statement = select(Historico)
        # Se um filtro foi definido, adiciona a condição na consulta
        if filtro:
            statement = statement.where(Historico.tipo == filtro)
        historicos = session.exec(statement).all()

    # Verifica se há registros para o filtro selecionado
    if not historicos:
        print("Nenhum histórico encontrado para o filtro selecionado.")
        return

    # Extrai as datas e os valores das transações para plotagem
    datas = [historico.data for historico in historicos]
    valores = [historico.valor for historico in historicos]

    # Gera o gráfico utilizando matplotlib
    plt.plot(datas, valores, marker='o')
    plt.xlabel("Data")
    plt.ylabel("Valor")
    plt.title("Histórico de Transações")
    plt.grid(True)
    plt.tight_layout()
    plt.show()