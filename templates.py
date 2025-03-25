from utils import *
from models import Banco, Conta
from views import *


class UI:

    def start(self):
        while True:
            menu()
            opcao = input('Informe a opção: ')

            match opcao:
                case '1':
                    lista = [
                        '1 - Adicionar',
                        '2 - Alterar',
                        '3 - Desativar',
                        '4 - Listar',
                    ]
                    submenu('cliente', lista)
                    opcao_cliente = input('Informe opção: ')
                    match opcao_cliente:
                        case '1':
                            self._add_cliente()
                        case '2':
                            self._alt_cliente()
                        case '3':
                            self._desativar_cliente()
                        case '4':
                            mostrar_clientes()
                        case _:
                            colorir('\nOpção inválida!\n', 33)

                case '2':
                    lista = [
                        '1 - Adicionar',
                        '2 - Alterar',
                        '3 - Desativar',
                        '4 - Listar',
                        '5 - Depositar',
                        '6 - Sacar',
                        '7 - Transferir',
                        '8 - Histórico movimentação',
                        '9 - Valor total das contas',
                    ]
                    submenu('conta', lista)
                    opcao_conta = input('Informe opção: ')
                    match opcao_conta:
                        case '1':
                            self._add_conta()
                        case '2':
                            self._alt_conta()
                        case '3':
                            self._desativar_conta()
                        case '4':
                            mostrar_contas()
                        case '5':
                            self._depositar()
                        case '6':
                            self._sacar()
                        case '7':
                            self._transferir()
                        case '8':
                            self._historico()
                        case '9':
                            self._total_contas()
                        case _:
                            colorir('\nOpção inválida!\n', 33)

                case '3':
                    self._gerar_grafico()
                case '4':
                    colorir('\nSistema Finalizado!\n', 36)
                    exit()             
                case _:
                    colorir('\nOpção inválida!\n', 33)

            input('\nTecle <ENTER> para continuar ...')

    def _add_cliente(self):
        nome_cliente = input('\nInforme o nome do cliente: ').upper()
        cpf_cliente = input('Informe o CPF do cliente: ')
        if all((nome_cliente, cpf_cliente)):
            try:
                adicionar_cliente(Cliente(nome=nome_cliente, cpf=cpf_cliente))
                colorir('\nCliente adicionado com sucesso.', 32)
            except Exception as e:
                colorir(f'\n\t{e}', 31)
        else:
            colorir(f'\nO Nome e o CPF são obrigatórios.', 31)

    def _alt_cliente(self):
        mostrar_clientes()
        cliente_id = input('\nInforme o ID do cliente: ')
        if cliente_id and cliente_id.isnumeric():
            cliente = buscar_cliente(int(cliente_id))
            if cliente:
                colorir(f'\nCliente escolhido: ', cor=32, end='')
                colorir(f'{cliente.nome} - {cliente.cpf}', 36)
                novo_nome = input('\nInforme o novo nome do cliente: ').upper()
                novo_cpf = input('Informe o novo CPF do cliente: ')
                novo_status = input('Informe o status do cliente [A/I]: ').upper()
                if novo_nome or novo_cpf or novo_status:
                    try:
                        alterar_cliente(int(cliente_id), novo_nome, novo_cpf, novo_status)
                        colorir('\n\tAlteração realizada com sucesso.', 32)
                    except Exception as e:
                        colorir(f'\n\t{e}', 31)
                else:
                    colorir('\n\tNão houve alterações!', 33)
            else:
                colorir('\n\tCliente não localizado!', 33)
        else:
            colorir('\n\tID do cliente não informado ou inválido!', 31)

    def _desativar_cliente(self):
        mostrar_clientes(status=Status.A)

        cliente_id = input('\nInforme o ID do cliente que deseja desativar: ')

        if cliente_id and cliente_id.isnumeric():
            cliente = buscar_cliente(int(cliente_id))
            if cliente:
                colorir(f'\nCliente escolhido: ', cor=32, end='')
                colorir(f'{cliente.nome} - {cliente.cpf}', 36)
                try:
                    desativar_cliente(int(cliente_id))
                    colorir('\n\tCliente desativado com sucesso.', 32)
                except Exception as e:
                    colorir(f'\n\t{e}', 31)
            else:
                colorir('\n\tCliente não localizado!', 33)
        else:
            colorir('\n\tID do cliente não informado ou inválido!', 31)

    def _add_conta(self):
        mostrar_bancos()

        banco_index = input('\nInforme o nº do banco: ')
        if banco_index:
            try:
                banco = Banco(int(banco_index))
                colorir(f'\nBanco escolhido: ', 33, end='')
                colorir(f'{banco.name}', 36)
                mostrar_clientes(status=Status.A)

                cliente_id = input('\nInforme o ID do cliente: ')
                if cliente_id and cliente_id.isnumeric():
                    cliente = buscar_cliente(int(cliente_id))                   
                    if cliente and cliente.status == Status.A:
                        colorir(f'\nCliente escolhido: ', 33, end='')
                        colorir(f'{cliente.nome}', 36)
                        try:
                            saldo = float(input('\nInforme o saldo inicial: '))
                            criar_conta(Conta(banco=banco, cliente_id=int(cliente_id), saldo=saldo))
                            colorir('\nConta criada com sucesso.', 32)
                        except Exception as e:
                            colorir(f'\n\t{e}', 31)
                    else:
                        colorir('\n\tID cliente não cadastrado ou inativo!', 31)
                else:
                    colorir('\n\tID cliente não informado ou inválido!', 31)

            except ValueError:
                colorir(f'\n\tNúmero do banco inválido!', 31)
        else:
            colorir('\tNúmero do banco não informado!', 31)

    def _alt_conta(self):
        mostrar_contas()

        conta_id = input('\nInforme o ID do conta: ')
        if conta_id and conta_id.isnumeric():
            conta_id = int(conta_id)
            conta = buscar_conta(conta_id)
            cliente_conta = buscar_cliente(conta.cliente_id)
            colorir(f'\n\tConta escolhida: ', cor=32, end='')
            colorir(f'{conta.id:<4}{conta.banco.name:<15}{cliente_conta.nome:<15}', 36)
            
            mostrar_clientes(status=Status.A)

            cliente_id = input('\nInforme o ID do cliente: ')
            if cliente_id and cliente_id.isnumeric():
                cliente_id = int(cliente_id)
                cliente = buscar_cliente(cliente_id)
                if cliente:
                    colorir(f'\n\tCliente escolhido: ', cor=32, end='')
                    colorir(f'{cliente.nome} - {cliente.cpf}', 36)
                    novo_status = input('\nInforme o status para a conta [A/I]: ').upper()
                    try:
                        alterar_conta(conta_id, cliente_id, novo_status)
                        colorir('\n\tAlteração realizada com sucesso.', 36)
                    except Exception as e:
                        colorir(f'\n\t{e}', 31)
                else:
                    colorir('\n\tID do cliente não cadastrado ou inativo!', 31)
            else:
                colorir('\n\tID do cliente não informado ou inválido!', 31)
        else:
            colorir('\n\tID da conta não informado ou inválido!', 31)

    def _desativar_conta(self):

        mostrar_contas(status=Status.A)

        id_conta = input('\nInforme o ID da conta que deseja desativar: ')

        if id_conta and id_conta.isnumeric():
            try:
                desativar_conta(int(id_conta))
                colorir('\n\tConta desativada com sucesso.', 32)
            except Exception as e:
                colorir(f'\n\t{e}', 31)
        else:
            colorir(f'\n\tID da conta não informado ou inválido!', 31)

    def _depositar(self):
        mostrar_contas(status=Status.A)

        id_conta = input('\nInforme o ID da conta para depósito: ')

        if id_conta and id_conta.isnumeric():
            id_conta = int(id_conta)
            conta = buscar_conta(id_conta)
            if not conta:
                colorir(f'\n\tConta inexistente!', 31)
            else:
                try:
                    valor = float(input('\nInforme o valor para depósito: '))
                    deposita_valor(conta, valor)
                    colorir('\n\tDepósito efetuado com sucesso.', 32)
                except Exception as e:
                    colorir(f'\n\t{e}', 31)
        else:
            colorir(f'\n\tID da conta não informado ou inválido!', 31)

    def _sacar(self):
        mostrar_contas(status=Status.A)

        id_conta = input('\nInforme o ID da conta para saque: ')

        if id_conta and id_conta.isnumeric():
            id_conta = int(id_conta)
            conta = buscar_conta(id_conta)
            if not conta:
                colorir(f'\n\tConta inexistente!', 31)
            else:
                try:
                    valor = float(input('\nInforme o valor para saque: '))
                    saca_valor(conta, valor)
                    colorir('\n\tSaque efetuado com sucesso.', 32)
                except Exception as e:
                    colorir(f'\n\t{e}', 31)
        else:
            colorir(f'\n\tID da conta não informado ou inválido!', 31)

    def _transferir(self):
        mostrar_contas(Status.A)

        try:
            conta_retirar_id = int(input('\nInforme a conta de onde retirar o dinheiro: '))

            conta_enviar_id = int(input('Informe a conta para onde enviar dinheiro: '))

            valor = float(input('Informe o valor a ser transferido: '))

            if transferir_valor(conta_retirar_id, conta_enviar_id, valor):
                colorir('\n\tValor transferido com sucesso.', 32)

        except Exception as e:
            colorir(f'\n\t{e}', 31)
 
    def _historico(self):
        mostrar_contas()

        id_conta = input('\nInforme o ID da conta para visualizar o histórico: ')

        if id_conta and id_conta.isnumeric():
            id_conta = int(id_conta)
            conta = buscar_conta(id_conta)
            if not conta:
                colorir(f'\n\tConta inexistente!', 31)
            else:
                try:
                    data_inicial = input('\nInforme a data inicial: ')
                    data_final = input('\nInforme a data final: ')

                    if data_inicial:
                        data_inicial = datetime.strptime(data_inicial, '%d/%m/%Y').date()
                    if data_final:
                        data_final = datetime.strptime(data_final, '%d/%m/%Y').date()

                    visualizar_historico_conta(id_conta, data_inicial, data_final)

                except Exception as e:
                    colorir(f'\n\t{e}', 31)
        else:
            colorir(f'\n\tID da conta não informado ou inválido!', 31)

    def _total_contas(self):
        colorir(f'\n\tValor total das contas: ', 33, end='')
        colorir(f'R$ {total_contas():.2f}', 36)

    def _gerar_grafico(self):
        mostrar_contas(status=Status.A)
        id_conta = input('\nInforme o ID da conta para visualizar o gráfico: ')

        if id_conta and id_conta.isnumeric():
            id_conta = int(id_conta)
            conta = buscar_conta(id_conta)
            if not conta:
                colorir(f'\n\tConta inexistente!', 31)
            else:
                data_inicial = input('\nInforme uma data inicial para o gráfico: ')
                if data_inicial:
                    try:
                        gerar_grafico_movimentacao_diaria_conta(id_conta, data_inicial)
                    except Exception as e:
                        colorir(f'\n\t{e}', 31)
                else:
                    colorir(f'\n\tA data inicial é obrigatória!', 31)
        else:
            colorir(f'\n\tID da conta não informado ou inválido!', 31)

if __name__ == '__main__':

    UI().start()
