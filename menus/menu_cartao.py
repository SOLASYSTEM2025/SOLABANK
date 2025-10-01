import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from utils.helpers import limpar_tela, pausar

def menu_cartao(usuario, cartao_manager, usuario_manager, auditoria):
    """
    💳 MENU DE CARTÕES DE CRÉDITO
    
    Esta função é como o "setor de cartões" do banco.
    Aqui o usuário pode criar novos cartões, fazer compras,
    ver faturas e pagar as contas do cartão.
    """
    
    while True:
        limpar_tela()
        
        cartoes = cartao_manager.get_cartoes_usuario(usuario)
        
        print(f"\n💳 CARTÕES DE CRÉDITO - {usuario}")
        
        if not cartoes:
            print("📝 Você não possui cartões de crédito.")
            print("1. ➕ Solicitar novo cartão")
            print("2. 🔙 Voltar")
            
            opcao = input("\nEscolha uma opção: ").strip()
            if opcao == "1":
                # Cria o primeiro cartão do usuário
                if cartao_manager.criar_cartao(usuario):
                    auditoria.log_acao(usuario, "CARTAO_CRIADO", "Novo cartão de crédito criado")
                    print("✅ Cartão criado com sucesso!")
                pausar()
            elif opcao == "2":
                break  # Volta para o menu anterior
            continue  # Reinicia o loop
        
        print("\n📋 Seus cartões:")
        for i, cartao in enumerate(cartoes, 1):  # enumerate começa do 1
            print(f"{i}. Cartão {cartao['numero']} - Limite: R$ {cartao['limite']:.2f}")
        
        print(f"\n{len(cartoes) + 1}. ➕ Solicitar novo cartão")
        print(f"{len(cartoes) + 2}. ⭐ Trocar pontos por saldo")
        print(f"{len(cartoes) + 3}. 🔙 Voltar")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        try:
            opcao_num = int(opcao)  # Converte para número
            
            if 1 <= opcao_num <= len(cartoes):
                cartao_selecionado = cartoes[opcao_num - 1]  # -1 porque lista começa do 0
                # Vai para o menu específico deste cartão
                menu_cartao_individual(usuario, cartao_selecionado, cartao_manager, usuario_manager, auditoria)
            
            # Se escolheu "Solicitar novo cartão"
            elif opcao_num == len(cartoes) + 1:
                if cartao_manager.criar_cartao(usuario):
                    auditoria.log_acao(usuario, "CARTAO_CRIADO", "Novo cartão de crédito criado")
                    print("✅ Cartão criado com sucesso!")
                pausar()
            
            # Se escolheu "Trocar pontos por saldo"
            elif opcao_num == len(cartoes) + 2:
                trocar_pontos_por_saldo(usuario, usuario_manager, auditoria) # type: ignore
            
            # Se escolheu "Voltar"
            elif opcao_num == len(cartoes) + 3:
                break
                
        except ValueError:
            # Se digitou algo que não é número
            print("❌ Opção inválida!")
            pausar()


def menu_cartao_individual(usuario, cartao, cartao_manager, usuario_manager, auditoria):
    """
    💳 MENU DE UM CARTÃO ESPECÍFICO
    
    Quando o usuário seleciona um cartão específico, esta função
    mostra todas as opções para aquele cartão: fazer compras,
    ver fatura, gerar PDF, pagar conta, etc.
    """
    
    while True:
        limpar_tela()
        
        print(f"\n💳 CARTÃO {cartao['numero']}")
        print(f"💰 Limite: R$ {cartao['limite']:.2f}")           # Limite total
        print(f"💸 Usado: R$ {cartao['usado']:.2f}")             # Quanto já gastou
        print(f"✅ Disponível: R$ {cartao['limite'] - cartao['usado']:.2f}")  # Quanto ainda pode gastar
        
        print("\n1. 🛒 Fazer compra")      # Comprar algo
        print("2. 🧾 Ver fatura atual")    # Ver o que deve pagar
        print("3. 📄 Gerar fatura PDF")    # Salvar fatura em arquivo
        print("4. 💰 Pagar fatura")        # Pagar a conta do cartão
        print("5. 🔙 Voltar")              # Voltar para lista de cartões
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            # FAZER COMPRA - usar o cartão para comprar algo
            try:
                valor = float(input("💰 Valor da compra: R$ "))
                parcelas = int(input("📅 Número de parcelas (1-24): "))
                descricao = input("📝 Descrição da compra: ")
                
                # Tenta fazer a compra
                if cartao_manager.fazer_compra(usuario, cartao['numero'], valor, parcelas, descricao):
                    pontos_ganhos = int(valor // 10)  # // = divisão inteira
                    usuario_manager.adicionar_pontos(usuario, pontos_ganhos)
                    
                    # Registra a compra no log
                    auditoria.log_acao(usuario, "COMPRA_CARTAO", 
                                     f"Compra de R$ {valor:.2f} em {parcelas}x no cartão {cartao['numero']}")
                    print(f"✅ Compra realizada! Você ganhou {pontos_ganhos} pontos!")
            except ValueError:
                print("❌ Valor inválido!")
            pausar()
        
        elif opcao == "2":
            # VER FATURA - mostra tudo que deve pagar
            cartao_manager.mostrar_fatura(usuario, cartao['numero'])
            pausar()
        
        elif opcao == "3":
            # GERAR PDF - cria arquivo PDF da fatura
            cartao_manager.gerar_fatura_pdf(usuario, cartao['numero'])
            pausar()
        
        elif opcao == "4":
            # PAGAR FATURA - paga a conta do cartão
            try:
                valor = float(input("💰 Valor do pagamento: R$ "))
                if cartao_manager.pagar_fatura(usuario, cartao['numero'], valor, usuario_manager):
                    auditoria.log_acao(usuario, "PAGAMENTO_FATURA", 
                                     f"Pagamento de R$ {valor:.2f} da fatura do cartão {cartao['numero']}")
                    print("✅ Pagamento realizado!")
            except ValueError:
                print("❌ Valor inválido!")
            pausar()
        
        elif opcao == "5":
            # VOLTAR - sai deste menu
            break
        
        else:
            print("❌ Opção inválida!")
            pausar()
