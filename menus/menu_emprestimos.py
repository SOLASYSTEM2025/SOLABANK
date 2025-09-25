from utils.helpers import limpar_tela, pausar


def menu_emprestimos(usuario, emprestimo_manager, usuario_manager, auditoria):
    """
    💵 MENU DE EMPRÉSTIMOS
    
    Esta função é como o "setor de crédito" do banco.
    Aqui o usuário pode pedir dinheiro emprestado,
    ver suas dívidas e fazer pagamentos.
    """
    
    while True:
        limpar_tela()
        print(f"\n💵 EMPRÉSTIMOS - {usuario}")
        
        emprestimos = emprestimo_manager.get_emprestimos_usuario(usuario)
        total_divida = sum(emp['valor_atual'] for emp in emprestimos)  # Soma todas as dívidas
        
        print(f"💸 Total em dívida: R$ {total_divida:.2f}")
        
        print("\n1. 💰 Solicitar empréstimo")   # Pedir dinheiro emprestado
        print("2. 📊 Ver empréstimos")          # Ver dívidas atuais
        print("3. 💸 Pagar empréstimo")         # Pagar dívidas
        print("4. 🔙 Voltar")                   # Voltar ao menu anterior
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            # Chama função específica para solicitar empréstimo
            emprestimo_manager.solicitar_emprestimo(usuario, usuario_manager, auditoria)
        elif opcao == "2":
            # Mostra todos os empréstimos do usuário
            emprestimo_manager.mostrar_emprestimos(usuario)
            pausar()
        elif opcao == "3":
            # Permite pagar empréstimos
            emprestimo_manager.pagar_emprestimo(usuario, usuario_manager, auditoria)
        elif opcao == "4":
            break  # Volta ao menu anterior
        else:
            print("❌ Opção inválida!")
            pausar()
