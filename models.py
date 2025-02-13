from sqlmodel import Field, SQLModel, create_engine, Relationship
from sqlalchemy import UniqueConstraint, Column, String
from enum import Enum
from datetime import date

# Enum para representar os bancos disponíveis
class Bancos(Enum):
    BANCO_DO_BRASIL = "Banco do Brasil"
    BRADESCO = "Bradesco"
    ITAU = "Itaú"
    CAIXA = "Caixa Econômica Federal"
    SANTANDER = "Santander"
    NUBANK = "Nubank"
    INTER = "Inter"
    C6 = "C6 Bank"
    OUTRO = "Outro"

# Enum para representar os status da conta
class Status(Enum):
    ATIVO = "Ativo"
    INATIVO = "Inativo"
    APROVAR = "Em aprovação"
    NEGAR = "Negado"

# Modelo de dados para uma conta bancária
class Conta(SQLModel, table=True):
    # Garante que o par (agencia, numero) seja único
    __table_args__ = (UniqueConstraint("agencia", "numero", name="uix_agencia_numero"),)
    
    id: int = Field(default=None, primary_key=True)  # Identificador único da conta
    agencia: int  # Número da agência
    numero: int  # Número da conta
    saldo: float  # Saldo disponível na conta
    banco: Bancos = Field(default=Bancos.OUTRO)  # Banco associado à conta (valor padrão: Outro)
    status: Status = Field(default=Status.ATIVO)  # Status da conta (valor padrão: Ativo)

# Enum para representar os tipos de transações no histórico
class Tipos(Enum):
    ENTRADA = "Entrada"
    SAIDA = "Saída"
    FALTADADOS = "Não informado"

# Modelo de dados para o histórico de transações da conta
class Historico(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Identificador único do registro histórico
    conta_id: int = Field(foreign_key="conta.id")  # Chave estrangeira para a conta associada
    conta: Conta = Relationship()  # Relacionamento com a tabela Conta
    tipo: Tipos = Field(default=Tipos.FALTADADOS)  # Tipo de transação (entrada, saída, etc.)
    valor: float  # Valor da transação
    data: date  # Data em que a transação ocorreu
    # Coluna para descrição da transação, com valor padrão vazio e não nulo
    descricao: str = Field(default="", sa_column=Column(String, nullable=False))

# Configuração do banco de dados utilizando SQLite
sqlite_file_name = "database.db"  # Nome do arquivo do banco de dados
sqlite_url = f"sqlite:///{sqlite_file_name}"  # URL de conexão com o SQLite
engine = create_engine(sqlite_url, echo=True)  # Troque para echo=False em produção

# Função para criar o banco de dados e as tabelas definidas nos modelos
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Bloco principal que executa a criação das tabelas se o script for executado diretamente
if __name__ == "__main__":
    create_db_and_tables()
