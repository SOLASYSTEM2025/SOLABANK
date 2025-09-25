from utils.helpers import limpar_tela, pausar


def pagamento_boletos(usuario, usuario_manager, auditoria):
    """
    🧾 PAGAMENTO DE BOLETOS
    
    Esta função simula o pagamento de contas (luz, água, telefone, etc.).
    O dinheiro é debitado da conta do usuário, como se fosse um saque
    para pagar uma conta externa.
    """
    
    limpar_tela()
    print(f"\n🧾 PAGAMENTO DE BOLETOS - {usuario}")
    
    try:
        valor = float(input("💰 Valor do boleto: R$ "))
        descricao = input("📝 Descrição (ex: Conta de Luz): ")
        
        if usuario_manager.sacar(usuario, valor):
            # Adiciona no histórico como pagamento de boleto
            usuario_manager.adicionar_historico(usuario, f"BOLETO: {descricao} - R$ {valor:.2f}")
            # Registra no log de auditoria
            auditoria.log_acao(usuario, "PAGAMENTO_BOLETO", f"Pagamento de boleto: {descricao} - R$ {valor:.2f}")
            print("✅ Boleto pago com sucesso!")
        else:
            print("❌ Saldo insuficiente!")
    
    except ValueError:
        # Se digitou um valor inválido (não numérico)
        print("❌ Valor inválido!")
    
    pausar()
