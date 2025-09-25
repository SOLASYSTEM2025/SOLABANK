class EmprestimoManager:
    """
    💵 GERENCIADOR DE EMPRÉSTIMOS
    
    Esta classe cuida de tudo relacionado aos empréstimos:
    - Solicitação de empréstimos
    - Cálculo de juros
    - Pagamentos e quitação
    
    É como o "setor de crédito" do banco.
    """
    
    def __init__(self):
        """
        🏗️ CONSTRUTOR
        
        Define onde salvar os dados dos empréstimos e carrega os existentes.
        """
        self.arquivo_emprestimos = "data/emprestimos.json"
        self.emprestimos = self.carregar_emprestimos()
    
    def carregar_emprestimos(self):
        """
        📂 CARREGAR EMPRÉSTIMOS DO ARQUIVO
        """
        if os.path.exists(self.arquivo_emprestimos):
            try:
                with open(self.arquivo_emprestimos, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def salvar_emprestimos(self):
        """
        💾 SALVAR EMPRÉSTIMOS NO ARQUIVO
        """
        with open(self.arquivo_emprestimos, 'w', encoding='utf-8') as f:
            json.dump(self.emprestimos, f, indent=2, ensure_ascii=False)
    
    def solicitar_emprestimo(self, usuario, usuario_manager, auditoria):
        """
        💰 SOLICITAR EMPRÉSTIMO
        
        Esta função permite que o usuário peça dinheiro emprestado.
        O limite é baseado no saldo atual do usuário.
        """
        print("\n💰 SOLICITAÇÃO DE EMPRÉSTIMO")
        
        saldo_atual = usuario_manager.get_saldo(usuario)
        limite_emprestimo = saldo_atual * 5  # Pode pedir até 5x o saldo
        
        print(f"💰 Seu saldo atual: R$ {saldo_atual:.2f}")
        print(f"📊 Limite para empréstimo: R$ {limite_emprestimo:.2f}")
        print("💹 Taxa de juros: 2% ao mês")
        
        if limite_emprestimo < 100:
            print("❌ Você precisa ter pelo menos R$ 20,00 de saldo para solicitar empréstimo!")
            pausar()
            return
        
        try:
            valor = float(input("💰 Valor do empréstimo: R$ "))
            parcelas = int(input("📅 Número de parcelas (1-36): "))
            
            if valor <= 0:
                print("❌ Valor deve ser positivo!")
                pausar()
                return
            
            if valor > limite_emprestimo:
                print(f"❌ Valor excede o limite de R$ {limite_emprestimo:.2f}!")
                pausar()
                return
            
            if parcelas < 1 or parcelas > 36:
                print("❌ Número de parcelas deve ser entre 1 e 36!")
                pausar()
                return
            
            # Calcula o valor total com juros (2% ao mês)
            valor_total = valor * ((1.02) ** parcelas)
            valor_parcela = valor_total / parcelas
            
            print(f"\n📊 SIMULAÇÃO DO EMPRÉSTIMO")
            print(f"💰 Valor solicitado: R$ {valor:.2f}")
            print(f"💸 Valor total a pagar: R$ {valor_total:.2f}")
            print(f"📅 {parcelas}x de R$ {valor_parcela:.2f}")
            print(f"💹 Total de juros: R$ {valor_total - valor:.2f}")
            
            confirma = input("\nConfirma o empréstimo? (s/n): ").strip().lower()
            
            if confirma != 's':
                print("❌ Empréstimo cancelado!")
                pausar()
                return
            
            # Cria o empréstimo
            emprestimo_id = f"{usuario}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            self.emprestimos[emprestimo_id] = {
                "usuario": usuario,
                "valor_original": valor,
                "valor_total": valor_total,
                "valor_atual": valor_total,  # Quanto ainda deve
                "parcelas_total": parcelas,
                "parcelas_pagas": 0,
                "valor_parcela": valor_parcela,
                "data_emprestimo": datetime.now().isoformat(),
                "status": "ativo"
            }
            
            # Adiciona o dinheiro na conta do usuário
            usuario_manager.depositar(usuario, valor)
            
            self.salvar_emprestimos()
            
            # Registra no histórico e auditoria
            usuario_manager.adicionar_historico(usuario, f"EMPRÉSTIMO: R$ {valor:.2f} em {parcelas}x")
            auditoria.log_acao(usuario, "EMPRESTIMO", f"Empréstimo de R$ {valor:.2f} em {parcelas}x")
            
            print(f"✅ Empréstimo aprovado e creditado na sua conta!")
            
        except ValueError:
            print("❌ Valor inválido!")
        
        pausar()
    
    def get_emprestimos_usuario(self, usuario):
        """
        📊 OBTER EMPRÉSTIMOS DO USUÁRIO
        
        Esta função retorna todos os empréstimos ativos de um usuário.
        """
        emprestimos_usuario = []
        
        for emp_id, dados in self.emprestimos.items():
            if dados["usuario"] == usuario and dados["status"] == "ativo":
                emprestimos_usuario.append({
                    "id": emp_id,
                    "valor_original": dados["valor_original"],
                    "valor_atual": dados["valor_atual"],
                    "parcelas_restantes": dados["parcelas_total"] - dados["parcelas_pagas"],
                    "valor_parcela": dados["valor_parcela"],
                    "data_emprestimo": datetime.fromisoformat(dados["data_emprestimo"]).strftime("%d/%m/%Y")
                })
        
        return emprestimos_usuario
    
    def mostrar_emprestimos(self, usuario):
        """
        📊 MOSTRAR EMPRÉSTIMOS
        
        Esta função exibe todos os empréstimos ativos do usuário.
        """
        emprestimos = self.get_emprestimos_usuario(usuario)
        
        print(f"\n📊 SEUS EMPRÉSTIMOS - {usuario}")
        print("=" * 60)
        
        if not emprestimos:
            print("✅ Você não possui empréstimos ativos.")
            return
        
        total_devido = 0
        
        for emp in emprestimos:
            print(f"\n💰 Empréstimo de {emp['data_emprestimo']}")
            print(f"   Valor original: R$ {emp['valor_original']:.2f}")
            print(f"   Valor atual devido: R$ {emp['valor_atual']:.2f}")
            print(f"   Parcelas restantes: {emp['parcelas_restantes']}")
            print(f"   Valor da parcela: R$ {emp['valor_parcela']:.2f}")
            
            total_devido += emp['valor_atual']
        
        print("\n" + "=" * 60)
        print(f"💸 Total devido: R$ {total_devido:.2f}")
    
    def pagar_emprestimo(self, usuario, usuario_manager, auditoria):
        """
        💸 PAGAR EMPRÉSTIMO
        
        Esta função permite que o usuário pague parcelas
        ou quite completamente um empréstimo.
        """
        emprestimos = self.get_emprestimos_usuario(usuario)
        
        if not emprestimos:
            print("✅ Você não possui empréstimos para pagar!")
            pausar()
            return
        
        print("\n💸 PAGAR EMPRÉSTIMO")
        print("\nSeus empréstimos:")
        
        for i, emp in enumerate(emprestimos, 1):
            print(f"{i}. Empréstimo de {emp['data_emprestimo']} - Devido: R$ {emp['valor_atual']:.2f}")
        
        try:
            escolha = int(input("\nEscolha o empréstimo para pagar: ")) - 1
            
            if escolha < 0 or escolha >= len(emprestimos):
                print("❌ Opção inválida!")
                pausar()
                return
            
            emprestimo = emprestimos[escolha]
            
            print(f"\n💰 Valor devido: R$ {emprestimo['valor_atual']:.2f}")
            print(f"📅 Valor da parcela: R$ {emprestimo['valor_parcela']:.2f}")
            print(f"🔢 Parcelas restantes: {emprestimo['parcelas_restantes']}")
            
            print("\n1. Pagar uma parcela")
            print("2. Quitar completamente")
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                # Pagar uma parcela
                valor_pagamento = emprestimo['valor_parcela']
                
                if not usuario_manager.sacar(usuario, valor_pagamento):
                    pausar()
                    return
                
                # Atualiza o empréstimo
                emp_dados = self.emprestimos[emprestimo['id']]
                emp_dados['valor_atual'] -= valor_pagamento
                emp_dados['parcelas_pagas'] += 1
                
                # Se pagou todas as parcelas, marca como quitado
                if emp_dados['parcelas_pagas'] >= emp_dados['parcelas_total']:
                    emp_dados['status'] = "quitado"
                    print("🎉 Empréstimo quitado completamente!")
                
                self.salvar_emprestimos()
                
                # Registra no histórico e auditoria
                usuario_manager.adicionar_historico(usuario, f"PAGAMENTO EMPRÉSTIMO: R$ {valor_pagamento:.2f}")
                auditoria.log_acao(usuario, "PAGAMENTO_EMPRESTIMO", f"Pagamento de parcela - R$ {valor_pagamento:.2f}")
                
                print(f"✅ Parcela paga com sucesso!")
                print(f"💰 Valor pago: R$ {valor_pagamento:.2f}")
                
            elif opcao == "2":
                # Quitar completamente
                valor_quitacao = emprestimo['valor_atual']
                
                if not usuario_manager.sacar(usuario, valor_quitacao):
                    pausar()
                    return
                
                # Marca como quitado
                self.emprestimos[emprestimo['id']]['status'] = "quitado"
                self.emprestimos[emprestimo['id']]['valor_atual'] = 0
                
                self.salvar_emprestimos()
                
                # Registra no histórico e auditoria
                usuario_manager.adicionar_historico(usuario, f"QUITAÇÃO EMPRÉSTIMO: R$ {valor_quitacao:.2f}")
                auditoria.log_acao(usuario, "QUITACAO_EMPRESTIMO", f"Quitação completa - R$ {valor_quitacao:.2f}")
                
                print(f"🎉 Empréstimo quitado completamente!")
                print(f"💰 Valor pago: R$ {valor_quitacao:.2f}")
            
            else:
                print("❌ Opção inválida!")
        
        except ValueError:
            print("❌ Opção inválida!")
        
        pausar()

# ============================================================================
# CLASSE GERENCIADOR ADMINISTRATIVO
# ============================================================================
