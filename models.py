from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, create_engine


class Banco(Enum):
    CAIXA = 1
    INTER = 2
    NUBANK = 3
    SANTANDER = 4

class Status(Enum):
    A = 'Ativo'
    I = 'Inativo'

class Tipo(Enum):
    E = 'Entrada'
    S = 'Saída'

class Cliente(SQLModel, table=True):
    id: int = Field(primary_key=True)
    nome: str
    cpf: str
    status: Status = Field(default=Status.A)

class Conta(SQLModel, table=True):
    id: int = Field(primary_key=True)
    banco: Banco = Field(default=Banco.NUBANK)
    cliente_id: int = Field(foreign_key='cliente.id')
    cliente: Cliente = Relationship()
    saldo: float
    status: Status = Field(default=Status.A)
    historico: list['Historico'] = Relationship(back_populates="conta")

class Historico(SQLModel, table=True):
    id: int = Field(primary_key=True)
    conta_id: int = Field(foreign_key='conta.id')
    tipo: Tipo = Field(default=Tipo.E)
    descricao: str
    valor: float
    data: datetime
    conta: Conta = Relationship(back_populates='historico')

sqlite_file_name = "database.db"  
sqlite_url = f"sqlite:///{sqlite_file_name}"  

engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():  
    SQLModel.metadata.create_all(engine)  


if __name__ == "__main__":  
    create_db_and_tables()  
