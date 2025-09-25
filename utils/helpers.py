import os
import random

def limpar_tela():
    """
    🧹 LIMPAR TELA
    
    Esta função limpa a tela do terminal para deixar a interface mais limpa.
    Funciona tanto no Windows (cls) quanto no Linux/Mac (clear).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    """
    ⏸️ PAUSAR EXECUÇÃO
    
    Esta função pausa o programa e espera o usuário pressionar Enter.
    É útil para dar tempo do usuário ler as mensagens antes de continuar.
    """
    input("\nPressione Enter para continuar...")


def validar_cpf(cpf):
    """
    📋 VALIDAR CPF
    
    Esta função verifica se um CPF tem o formato correto (11 dígitos).
    É uma validação básica, não verifica os dígitos verificadores.
    """
    cpf = cpf.replace(".", "").replace("-", "")  # Remove pontos e traços
    return len(cpf) == 11 and cpf.isdigit()     # Verifica se tem 11 dígitos


def formatar_moeda(valor):
    """
    💰 FORMATAR MOEDA
    
    Esta função formata um número para aparecer como dinheiro brasileiro.
    Exemplo: 1234.56 vira "R$ 1.234,56"
    """
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def gerar_numero_cartao():
    """
    💳 GERAR NÚMERO DE CARTÃO
    
    Esta função gera um número de cartão de crédito fictício.
    Começa com 4000 (padrão Visa) e adiciona 12 dígitos aleatórios.
    """
    return "4000" + "".join([str(random.randint(0, 9)) for _ in range(12)])

# ============================================================================
# CLASSE GERENCIADOR DE USUÁRIOS
# ============================================================================
