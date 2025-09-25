import datetime
import json
import os

from utils.helpers import pausar

class InvestimentoManager:
    """
    📈 GERENCIADOR DE INVESTIMENTOS
    
    Esta classe cuida de tudo relacionado aos investimentos:
    - Aplicações em diferentes tipos de investimento
    - Simulação de rendimentos
    - Resgate de investimentos
    
    É como a "corretora" do banco.
    """
    
    def __init__(self):
        """
        🏗️ CONSTRUTOR
        
        Define onde salvar os dados dos investimentos e carrega os existentes.
        """
        self.arquivo_investimentos = "data/investimentos.json"
        self.investimentos = self.carregar_investimentos()
        
        # Tipos de investimento disponíveis com suas características
        self.tipos_investimento = {
            "poupanca": {"nome": "Poupança", "rendimento_mensal": 0.005, "risco": "Baixo"},
            "cdb": {"nome": "CDB", "rendimento_mensal": 0.008, "risco": "Baixo"},
            "tesouro": {"nome": "Tesouro Direto", "rendimento_mensal": 0.01, "risco": "Médio"},
            "acoes": {"nome": "Ações", "rendimento_mensal": 0.015, "risco": "Alto"},
            "bitcoin": {"nome": "Bitcoin", "rendimento_mensal": 0.02, "risco": "Muito Alto"}
        }
    
    def carregar_investimentos(self):
        """
        📂 CARREGAR INVESTIMENTOS DO ARQUIVO
        """
        if os.path.exists(self.arquivo_investimentos):
            try:
                with open(self.arquivo_investimentos, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def salvar_investimentos(self):
        """
        💾 SALVAR INVESTIMENTOS NO ARQUIVO
        """
        with open(self.arquivo_investimentos, 'w', encoding='utf-8') as f:
            json.dump(self.investimentos, f, indent=2, ensure_ascii=False)
    
    def nova_aplicacao(self, usuario, usuario_manager, auditoria):
        """
        💰 FAZER NOVA APLICAÇÃO
        
        Esta função permite que o usuário invista dinheiro
        em diferentes tipos de investimento.
        """
        print("\n💰 NOVA APLICAÇÃO")
        
        # Mostra os tipos de investimento disponíveis
        print("\n📊 Tipos de investimento disponíveis:")
        for codigo, info in self.tipos_investimento.items():
            rendimento_anual = (info["rendimento_mensal"] * 12) * 100
            print(f"{codigo}: {info['nome']} - {rendimento_anual:.1f}% ao ano - Risco: {info['risco']}")
        
        tipo = input("\nEscolha o tipo de investimento: ").strip().lower()
        
        if tipo not in self.tipos_investimento:
            print("❌ Tipo de investimento inválido!")
            pausar()
            return
        
        try:
            valor = float(input("💰 Valor a investir: R$ "))
            
            if valor <= 0:
                print("❌ Valor deve ser positivo!")
                pausar()
                return
            
            # Verifica se tem saldo suficiente
            if not usuario_manager.sacar(usuario, valor):
                pausar()
                return
            
            # Cria o investimento
            investimento_id = f"{usuario}_{tipo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            self.investimentos[investimento_id] = {
                "usuario": usuario,
                "tipo": tipo,
                "valor_inicial": valor,
                "valor_atual": valor,
                "data_aplicacao": datetime.now().isoformat(),
                "rendimento_mensal": self.tipos_investimento[tipo]["rendimento_mensal"]
            }
            
            self.salvar_investimentos()
            
            # Registra no histórico e auditoria
            usuario_manager.adicionar_historico(usuario, f"INVESTIMENTO: {self.tipos_investimento[tipo]['nome']} - R$ {valor:.2f}")
            auditoria.log_acao(usuario, "INVESTIMENTO", f"Aplicação em {self.tipos_investimento[tipo]['nome']} - R$ {valor:.2f}")
            
            print(f"✅ Investimento realizado com sucesso!")
            print(f"📈 Tipo: {self.tipos_investimento[tipo]['nome']}")
            print(f"💰 Valor: R$ {valor:.2f}")
            
        except ValueError:
            print("❌ Valor inválido!")
        
        pausar()
    
    def get_investimentos_usuario(self, usuario):
        """
        📊 OBTER INVESTIMENTOS DO USUÁRIO
        
        Esta função retorna todos os investimentos de um usuário,
        atualizando os rendimentos baseado no tempo decorrido.
        """
        investimentos_usuario = []
        hoje = datetime.now()
        
        for inv_id, dados in self.investimentos.items():
            if dados["usuario"] == usuario:
                # Calcula o rendimento baseado no tempo decorrido
                data_aplicacao = datetime.fromisoformat(dados["data_aplicacao"])
                meses_decorridos = (hoje - data_aplicacao).days / 30  # Aproximação
                
                # Aplica o rendimento composto
                valor_atual = dados["valor_inicial"] * ((1 + dados["rendimento_mensal"]) ** meses_decorridos)
                
                # Atualiza o valor atual no arquivo
                self.investimentos[inv_id]["valor_atual"] = valor_atual
                
                investimentos_usuario.append({
                    "id": inv_id,
                    "tipo": self.tipos_investimento[dados["tipo"]]["nome"],
                    "valor_inicial": dados["valor_inicial"],
                    "valor_atual": valor_atual,
                    "rendimento": valor_atual - dados["valor_inicial"],
                    "data_aplicacao": data_aplicacao.strftime("%d/%m/%Y")
                })
        
        self.salvar_investimentos()
        return investimentos_usuario
    
    def mostrar_investimentos(self, usuario):
        """
        📊 MOSTRAR INVESTIMENTOS
        
        Esta função exibe todos os investimentos do usuário
        com seus valores atuais e rendimentos.
        """
        investimentos = self.get_investimentos_usuario(usuario)
        
        print(f"\n📊 SEUS INVESTIMENTOS - {usuario}")
        print("=" * 60)
        
        if not investimentos:
            print("📝 Você não possui investimentos.")
            return
        
        total_investido = 0
        total_atual = 0
        
        for inv in investimentos:
            print(f"\n💰 {inv['tipo']}")
            print(f"   Valor inicial: R$ {inv['valor_inicial']:.2f}")
            print(f"   Valor atual: R$ {inv['valor_atual']:.2f}")
            print(f"   Rendimento: R$ {inv['rendimento']:.2f}")
            print(f"   Data: {inv['data_aplicacao']}")
            
            total_investido += inv['valor_inicial']
            total_atual += inv['valor_atual']
        
        print("\n" + "=" * 60)
        print(f"💰 Total investido: R$ {total_investido:.2f}")
        print(f"📈 Valor atual: R$ {total_atual:.2f}")
        print(f"💹 Rendimento total: R$ {total_atual - total_investido:.2f}")
    
    def resgatar_investimento(self, usuario, usuario_manager, auditoria):
        """
        💸 RESGATAR INVESTIMENTO
        
        Esta função permite que o usuário retire dinheiro
        dos seus investimentos.
        """
        investimentos = self.get_investimentos_usuario(usuario)
        
        if not investimentos:
            print("❌ Você não possui investimentos para resgatar!")
            pausar()
            return
        
        print("\n💸 RESGATAR INVESTIMENTO")
        print("\nSeus investimentos:")
        
        for i, inv in enumerate(investimentos, 1):
            print(f"{i}. {inv['tipo']} - R$ {inv['valor_atual']:.2f} (Rendimento: R$ {inv['rendimento']:.2f})")
        
        try:
            escolha = int(input("\nEscolha o investimento para resgatar: ")) - 1
            
            if escolha < 0 or escolha >= len(investimentos):
                print("❌ Opção inválida!")
                pausar()
                return
            
            investimento = investimentos[escolha]
            
            # Confirma o resgate
            print(f"\n💰 Valor a resgatar: R$ {investimento['valor_atual']:.2f}")
            confirma = input("Confirma o resgate? (s/n): ").strip().lower()
            
            if confirma != 's':
                print("❌ Resgate cancelado!")
                pausar()
                return
            
            # Adiciona o dinheiro na conta
            usuario_manager.depositar(usuario, investimento['valor_atual'])
            
            # Remove o investimento
            del self.investimentos[investimento['id']]
            self.salvar_investimentos()
            
            # Registra no histórico e auditoria
            usuario_manager.adicionar_historico(usuario, f"RESGATE: {investimento['tipo']} - R$ {investimento['valor_atual']:.2f}")
            auditoria.log_acao(usuario, "RESGATE", f"Resgate de {investimento['tipo']} - R$ {investimento['valor_atual']:.2f}")
            
            print(f"✅ Resgate realizado com sucesso!")
            print(f"💰 Valor creditado: R$ {investimento['valor_atual']:.2f}")
            
        except ValueError:
            print("❌ Opção inválida!")
        
        pausar()

# ============================================================================
# CLASSE GERENCIADOR DE EMPRÉSTIMOS
# ============================================================================
