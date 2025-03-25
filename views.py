from datetime import datetime, timedelta
from models import Cliente, Conta, Historico, Tipo, engine, Banco, Status
from sqlmodel import Session, select, func
from utils import colorir
from rich import box
from rich.table import Table
from rich.console import Console
import matplotlib.pyplot as plt
import numpy as np


console = Console()

def mostrar_bancos():
    print('')
    table = Table(title='Bancos disponíveis', width=30, box=box.HORIZONTALS)
    headers = ['Nº', 'NOME']
    for header in headers:
        table.add_column(header, style='cyan')
    for b in Banco:
        table.add_row(str(b.value), b.name)
    console.print(table, style='yellow')

def buscar_cliente(cliente_id):
    with Session(engine) as session:
        return session.exec(select(Cliente).where(Cliente.id==cliente_id)).first()

def adicionar_cliente(cliente: Cliente):
    with Session(engine) as session:
        statement = select(Cliente).where(Cliente.cpf==cliente.cpf)
        results = session.exec(statement).all()
        if results:
            raise Exception('CPF já cadastrado!')
        session.add(cliente)
        session.commit()

def alterar_cliente(cliente_id, nome, cpf, status):
    with Session(engine) as session:
        statement = select(Cliente).where(Cliente.id==cliente_id)
        cliente = session.exec(statement).one()
        if not cliente:
            raise Exception('Cliente inexistente!')
        if nome:
            cliente.nome = nome
        if cpf:
            cliente.cpf = cpf
        if status:
            if status in ['A', 'I']:
                cliente.status = Status.A if status.upper() == 'A' else Status.I
            else:
                raise Exception('Status inválido!')

        session.add(cliente)
        session.commit()
        session.refresh(cliente)

def desativar_cliente(id):
    with Session(engine) as session:
        statement = select(Cliente).where(Cliente.id==id)
        cliente = session.exec(statement).first()
        if not cliente:
            raise Exception('Cliente inexistente!')
        cliente.status = Status.I
        session.commit()
        
def listar_clientes(status=None):
    with Session(engine) as session:
        if status:
            statement = select(Cliente).where(Cliente.status==status)
        else:
            statement = select(Cliente)
        results = session.exec(statement).all()
    return results

def mostrar_clientes(status=None):
    print('')
    clientes = listar_clientes(status)
    if clientes:
        table = Table(title='Clientes ativos' if status else 'Clientes', box=box.HORIZONTALS)
        headers = ['id', 'nome', 'cpf', 'status']
        for header in headers:
            table.add_column(header, style='cyan')
        for cliente in clientes:
            cliente.status = cliente.status.value
            values = [str(getattr(cliente, header)) for header in headers]
            table.add_row(*values)
        console.print(table, style='yellow')
    else:
        colorir(f'\n\tNão há cliente cadastrado.', 33)

def buscar_conta(conta_id):
    with Session(engine) as session:
        return session.exec(select(Conta).where(Conta.id==conta_id)).first()
    
def criar_conta(conta: Conta):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.banco==conta.banco, Conta.cliente==conta.cliente)
        results = session.exec(statement).all()
        if results:
            raise Exception('Já existe uma conta neste banco para este cliente!')
        session.add(conta)
        session.commit()

        historico = Historico(conta_id=conta.id, descricao=f'Saldo inicial de R$ {conta.saldo:.2f}', valor=conta.saldo, data=datetime.now())

        session.add(historico)
        session.commit()

def alterar_conta(conta_id, cliente_id, status):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==conta_id)
        conta = session.exec(statement).one()
        if not conta:
            raise Exception('Conta inexistente!')

        conta.cliente_id = cliente_id
        if status:
            if status not in ['A', 'I']:
                raise Exception('Status inválido!')
            else:
                if status == 'A':
                    conta.status = Status.A
                else:
                    if conta.saldo > 0:
                        raise Exception('Essa conta ainda possui saldo, não é possível desativar.')
                    conta.status = Status.I

        session.add(conta)
        session.commit()
        session.refresh(conta)

def listar_contas(status=None):
    with Session(engine) as session:
        if status:
            statement = select(Conta, Cliente).where(Conta.cliente_id==Cliente.id, Conta.status==status)
        else:
            statement = select(Conta, Cliente).where(Conta.cliente_id==Cliente.id)
        results = session.exec(statement).all()
    return results

def mostrar_contas(status=None):
    print('')
    contas = listar_contas(status)
    if contas:
        table = Table(title='Contas ativas' if status else 'Contas', box=box.HORIZONTALS)
        headers = ['id', 'banco', 'cliente', 'saldo', 'status']
        for header in headers:
            if header == 'saldo':
                table.add_column(header, justify='right', style='cyan')
            else:
                table.add_column(header, style='cyan')
        for conta, cliente in contas:
            table.add_row(str(conta.id), conta.banco.name, cliente.nome, f'{conta.saldo:.2f}', conta.status.value)
        console.print(table, style='yellow')
    else:
        colorir(f'\n\tNão há conta cadastrada.', 33)

def desativar_conta(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id)
        conta = session.exec(statement).first()
        if not conta:
            raise Exception('Conta inexistente!')
        if conta.saldo > 0:
            raise Exception('Essa conta ainda possui saldo, não é possível desativar.')
        conta.status = Status.I
        session.commit()

def deposita_valor(conta: Conta, valor, descricao='Depósito'):
    if float(valor) < 0.00:
        raise Exception('Valor negativo não pode ser depositado.')
    with Session(engine) as session:
        conta.saldo += valor
        session.add(conta)
        session.commit()

        historico = Historico(conta_id=conta.id, descricao=f'{descricao} de R$ {valor:.2f}', valor=valor, data=datetime.now())
        session.add(historico)
        session.commit()

def saca_valor(conta: Conta, valor, descricao='Saque'):
    if float(valor) < 0.00:
        raise Exception('Valor negativo não pode ser sacado.')
    with Session(engine) as session:
        if conta.saldo < valor:
            raise Exception(f'Saldo insuficiente')
        conta.saldo -= valor
        session.add(conta)
        session.commit()

        historico = Historico(conta_id=conta.id, tipo=Tipo.S, descricao=f'{descricao} de R$ {valor:.2f}', valor=valor, data=datetime.now())
        session.add(historico)
        session.commit()

def transferir_valor(id_conta_origem, id_conta_destino, valor):
    try:
        conta_origem = buscar_conta(id_conta_origem)
        if not conta_origem:
            raise Exception('Conta para saque inexistente!')
        
        conta_destino = buscar_conta(id_conta_destino)
        if not conta_destino:
            raise Exception('Conta para depósito inexistente!')
        
        saca_valor(conta_origem, valor, descricao=f'Transferência efetuada para a conta {id_conta_destino}')
        deposita_valor(conta_destino, valor, descricao=f'Transferência recebida da conta {id_conta_origem}')
        return True
    except Exception as e:
        colorir(f'\n\t{e}', 31)
        return False

def historico_conta_periodo(conta_id, data_inicial=None, data_final=None):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==conta_id)
        conta = session.exec(statement).one()
        lista_historicos = conta.historico
        lista_filtrada = []
        if data_inicial:
            lista_inicial = [historico for historico in lista_historicos if historico.data.date() >= data_inicial]
            if lista_inicial:
                lista_filtrada += lista_inicial
        if data_final:
            lista_final = [historico for historico in lista_historicos if historico.data.date() <= data_final]
            if lista_final:
                lista_filtrada += lista_final

        return lista_filtrada if lista_filtrada else lista_historicos

def visualizar_historico_conta(conta_id, data_inicial=None, data_final=None):
    print('')
    table = Table(title=f'Histórico da conta {conta_id}', box=box.HORIZONTALS)
    headers = ['id', 'tipo', 'descricao', 'valor', 'data']
    for header in headers:
        if header == 'id' or header == 'valor':
            table.add_column(header, justify='right', style='cyan')
        else:
            table.add_column(header, style='cyan')
    for hist in historico_conta_periodo(conta_id, data_inicial, data_final):
        hist.tipo = hist.tipo.name
        hist.valor = f'{hist.valor:.2f}'
        values = [str(getattr(hist, header)) for header in headers]
        table.add_row(*values)
    console.print(table, style='yellow')

def total_contas():
    with Session(engine) as session:
        statement = select(func.sum(Conta.saldo))
        total = session.exec(statement).one()

    return float(total)

def obter_dados_para_grafico(conta_id, data_inicial):
    dt_inicial = datetime.strptime(data_inicial, '%d/%m/%Y').date()
    dt_final = (datetime.strptime(data_inicial, '%d/%m/%Y') + timedelta(days=6)).date()

    datas_unicas = []
    for i in range(7):
        d = (dt_inicial + timedelta(days=i))
        if d > datetime.now().date():
            break
        datas_unicas.append(d.strftime('%d/%m/%Y'))

    with Session(engine) as session:
        statement = (
            select(
                func.strftime('%d/%m/%Y', Historico.data).label("data_formatada"),  # Trunca a data para d/m/Y
                Historico.tipo,
                func.sum(Historico.valor).label("total")
            )
            .where(Historico.conta_id == conta_id, Historico.data >= dt_inicial, Historico.data <= dt_final)  # Filtra por conta_id=2
            .group_by("data_formatada", Historico.tipo)  # Agrupa pela data truncada e pelo tipo
        )

        historico_conta = session.exec(statement).all()

        # datas = [historico_conta[i][0] for i in range(len(historico_conta))]
        # datas_unicas = sorted(list(set(datas)))

        dict_entradas =  {
            historico_conta[i][0]:historico_conta[i][2] for i in range(len(historico_conta)) if historico_conta[i][1] == Tipo.E
        }

        dict_saidas = {
            historico_conta[i][0]:historico_conta[i][2] for i in range(len(historico_conta)) if historico_conta[i][1] == Tipo.S
        }

        entradas, saidas = [], []

        for dt in datas_unicas:

            if dict_entradas.get(dt):
                entradas.append(dict_entradas.get(dt))
            else:
                entradas.append(0)
            if dict_saidas.get(dt):
                saidas.append(dict_saidas.get(dt))
            else:
                saidas.append(0)

        return datas_unicas, entradas, saidas

def gerar_grafico_movimentacao_diaria_conta(conta_id, data_inicial):

    datas, entradas, saidas = obter_dados_para_grafico(conta_id, data_inicial)

    tipos = {
        'Entradas': entradas,
        'Saídas': saidas,
    }

    valor_max = max(entradas + saidas)

    x = np.arange(len(datas))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in tipos.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Valores (R$)')
    ax.set_title(f'Entradas e saídas semanal: Conta {conta_id}')
    ax.set_xticks(x + width, datas)
    ax.legend(loc='upper center', ncols=2)
    ax.set_ylim(0, valor_max + 100)

    plt.show()
