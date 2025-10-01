from .menu_cartao import menu_cartao
from .menu_emprestimos import menu_emprestimos
from .menu_investimentos import menu_investimentos
from .menu_boletos import pagamento_boletos
from .utils.helpers import limpar_tela, pausar # type: ignore


def menu_usuario(usuario, usuario_manager, cartao_manager, investimento_manager, emprestimo_manager, auditoria):
    """
    👤 MENU DO USUÁRIO LOGADO
    
    Esta função é como o "balcão de atendimento" do banco.
    Aqui o usuário pode fazer todas as operações bancárias:
    depósito, saque, transferência, usar cartão, investir, etc.
    """
    
    # Loop infinito - usuário fica no menu até fazer logout
    while True:
        limpar_tela()
        
        saldo = usuario_manager.get_saldo(usuario)    # Quanto dinheiro tem
        pontos = usuario_manager.get_pontos(usuario)  # Quantos pontos de recompensa tem
        
        # Mostra as informações do usuário
        print(f"\n👋 Bem-vindo, {usuario}!")
        print(f"💰 Saldo: R$ {saldo:.2f}")      # .2f = duas casas decimais
        print(f"⭐ Pontos: {pontos}")
        
        print("\n📋 MENU DO USUÁRIO")
        print("1. 💰 Depósito")           # Colocar dinheiro na conta
        print("2. 💸 Saque")             # Tirar dinheiro da conta
        print("3. 🔄 Transferência")     # Enviar dinheiro para outro usuário
        print("4. 💳 Cartão de Crédito") # Gerenciar cartões
        print("5. 📈 Investimentos")     # Aplicar dinheiro
        print("6. 💵 Empréstimos")       # Pedir dinheiro emprestado
        print("7. 🧾 Pagamento de Boletos") # Pagar contas
        print("8. 📊 Histórico")         # Ver movimentações
        print("9. 📄 Exportar Histórico") # Salvar histórico em arquivo
        print("10. 🚪 Logout")           # Sair da conta
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            # DEPÓSITO - adicionar dinheiro na conta
            try:
                valor = float(input("💰 Valor do depósito: R$ "))
                if usuario_manager.depositar(usuario, valor):
                    # Registra a operação no log de auditoria
                    auditoria.log_acao(usuario, "DEPOSITO", f"Depósito de R$ {valor:.2f}")
                    print("✅ Depósito realizado com sucesso!")
            except ValueError:
                print("❌ Valor inválido!")
            pausar()
        
        elif opcao == "2":
            # SAQUE - tirar dinheiro da conta
            try:
                valor = float(input("💸 Valor do saque: R$ "))
                if usuario_manager.sacar(usuario, valor):
                    auditoria.log_acao(usuario, "SAQUE", f"Saque de R$ {valor:.2f}")
                    print("✅ Saque realizado com sucesso!")
            except ValueError:
                print("❌ Valor inválido!")
            pausar()
        
        elif opcao == "3":
            # TRANSFERÊNCIA - enviar dinheiro para outro usuário
            destino = input("🎯 Usuário de destino: ")
            try:
                valor = float(input("💰 Valor da transferência: R$ "))
                if usuario_manager.transferir(usuario, destino, valor):
                    auditoria.log_acao(usuario, "TRANSFERENCIA", f"Transferência de R$ {valor:.2f} para {destino}")
                    print("✅ Transferência realizada com sucesso!")
            except ValueError:
                print("❌ Valor inválido!")
            pausar()
        
        elif opcao == "4":
            # CARTÃO DE CRÉDITO - vai para o menu específico de cartões
            menu_cartao(usuario, cartao_manager, usuario_manager, auditoria)
        
        elif opcao == "5":
            # INVESTIMENTOS - vai para o menu específico de investimentos
            menu_investimentos(usuario, investimento_manager, usuario_manager, auditoria)
        
        elif opcao == "6":
            # EMPRÉSTIMOS - vai para o menu específico de empréstimos
            menu_emprestimos(usuario, emprestimo_manager, usuario_manager, auditoria)
        
        elif opcao == "7":
            # PAGAMENTO DE BOLETOS - função específica para pagar contas
            pagamento_boletos(usuario, usuario_manager, auditoria)
        
        elif opcao == "8":
            # HISTÓRICO - mostra todas as movimentações do usuário
            usuario_manager.mostrar_historico(usuario)
            pausar()
        
        elif opcao == "9":
            # EXPORTAR HISTÓRICO - salva o histórico em arquivo
            usuario_manager.exportar_historico(usuario)
            pausar()
        
        elif opcao == "10":
            # LOGOUT - sai da conta do usuário
            auditoria.log_acao(usuario, "LOGOUT", "Logout realizado")
            break  # Sai do loop e volta para o menu principal
        
        else:
            print("❌ Opção inválida!")
            pausar()
