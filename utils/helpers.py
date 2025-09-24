# ============================================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================================

def limpar_tela():
    """
    🧹 LIMPAR TELA
    
    Esta função limpa a tela do terminal para deixar a interface mais limpa.
    Funciona tanto no Windows (cls) quanto no Linux/Mac (clear).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


