def menu_admin(admin_manager, usuario_manager, auditoria):
    """
    🔧 MENU ADMINISTRATIVO
    
    Esta função é exclusiva para administradores do sistema.
    Aqui eles podem ver estatísticas, gerar relatórios,
    listar usuários e verificar logs de segurança.
    
    É como o "escritório da gerência" do banco.
    """
    
    while True:
        limpar_tela()
        print("\n🔧 PAINEL ADMINISTRATIVO")
        
        print("1. 👥 Lista de usuários")         # Ver todos os usuários cadastrados
        print("2. 📊 Estatísticas gerais")     # Ver números do sistema
        print("3. 📄 Gerar relatório CSV")     # Exportar dados em planilha
        print("4. 📋 Gerar relatório PDF")     # Exportar relatório em PDF
        print("5. 📝 Ver logs de auditoria")   # Ver logs de segurança
        print("6. 🚪 Sair")                    # Sair do painel admin
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            # Lista todos os usuários do sistema
            admin_manager.listar_usuarios(usuario_manager)
            pausar()
        elif opcao == "2":
            # Mostra estatísticas gerais do sistema
            admin_manager.mostrar_estatisticas(usuario_manager)
            pausar()
        elif opcao == "3":
            # Gera relatório em formato CSV (planilha)
            admin_manager.gerar_relatorio_csv(usuario_manager)
            pausar()
        elif opcao == "4":
            # Gera relatório em formato PDF
            admin_manager.gerar_relatorio_pdf(usuario_manager)
            pausar()
        elif opcao == "5":
            # Mostra todos os logs de auditoria (segurança)
            auditoria.mostrar_logs()
            pausar()
        elif opcao == "6":
            break  # Sai do painel administrativo
        else:
            print("❌ Opção inválida!")
            pausar()

# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

# Esta linha verifica se o arquivo está sendo executado diretamente
# (não se for importado como módulo)
if __name__ == "__main__":
    main()  # Chama a função principal para iniciar o sistema
