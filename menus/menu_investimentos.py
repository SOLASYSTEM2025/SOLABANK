def menu_investimentos(usuario, investimento_manager, usuario_manager, auditoria):
    """
    📈 MENU DE INVESTIMENTOS
    
    Esta função é como a "corretora" do banco.
    Aqui o usuário pode aplicar dinheiro em diferentes tipos
    de investimento para fazer o dinheiro render.
    """
    
    while True:
        limpar_tela()
        print(f"\n📈 INVESTIMENTOS - {usuario}")
        
        investimentos = investimento_manager.get_investimentos_usuario(usuario)
        total_investido = sum(inv['valor_atual'] for inv in investimentos)  # Soma todos os investimentos
        
        print(f"💰 Total investido: R$ {total_investido:.2f}")
        
        print("\n1. 💰 Nova aplicação")        # Investir dinheiro
        print("2. 📊 Ver investimentos")       # Ver aplicações atuais
        print("3. 💸 Resgatar investimento")   # Tirar dinheiro investido
        print("4. 🔙 Voltar")                  # Voltar ao menu anterior
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            # Chama função específica para nova aplicação
            investimento_manager.nova_aplicacao(usuario, usuario_manager, auditoria)
        elif opcao == "2":
            # Mostra todos os investimentos do usuário
            investimento_manager.mostrar_investimentos(usuario)
            pausar()
        elif opcao == "3":
            # Permite resgatar (tirar) dinheiro dos investimentos
            investimento_manager.resgatar_investimento(usuario, usuario_manager, auditoria)
        elif opcao == "4":
            break  # Volta ao menu anterior
        else:
            print("❌ Opção inválida!")
            pausar()
