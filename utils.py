import os


def limpa_tela():
    return os.system('clear') or None

def colorir(texto, cor=37, bold=0, end='\n'):
    print(f"\033[{bold};{cor}m{texto}\033[0m", end=end)

def menu():
    limpa_tela()
    t = 30
    cor = 32
    colorir('=' * t, cor)
    colorir('MENU'.center(t), cor)
    colorir('=' * t, cor)
    colorir('  1 - Cliente', cor)
    colorir('  2 - Conta', cor)
    colorir('  3 - Gerar gráfico', cor)
    colorir('  4 - Sair', cor)
    colorir('=' * t, cor)
    print()
    
def submenu(titulo, list_submenu):
    t = 30
    cor = 32
    colorir('=' * t, cor)
    colorir(titulo.upper().center(t), cor)
    colorir('=' * t, cor)
    for x in list_submenu:
        colorir(f'  {x}', cor)
    print()

