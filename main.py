"""
                🏦 SOLABANK
=============================================
"""

import json
import os
import csv
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import random

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

class UsuarioManager:
    """
    👥 GERENCIADOR DE USUÁRIOS
    
    Esta classe é responsável por tudo relacionado aos usuários:
    - Cadastro e login
    - Controle de saldo e pontos
    - Histórico de transações
    - Operações bancárias básicas
    
    É como o "departamento de contas" do banco.
    """
    
    def __init__(self):
        """
        🏗️ CONSTRUTOR
        
        Quando criamos um UsuarioManager, ele automaticamente:
        - Define onde salvar os dados dos usuários (arquivo JSON)
        - Carrega os usuários já cadastrados
        """
        self.arquivo_usuarios = "usuarios.json"
        self.usuarios = self.carregar_usuarios()
    
    def carregar_usuarios(self):
        """
        📂 CARREGAR USUÁRIOS DO ARQUIVO
        
        Esta função lê o arquivo JSON onde estão salvos todos os usuários.
        Se o arquivo não existir ou estiver corrompido, retorna um dicionário vazio.
        """
        if os.path.exists(self.arquivo_usuarios):
            try:
                with open(self.arquivo_usuarios, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                # Se der erro ao ler o arquivo, retorna dicionário vazio
                return {}
        return {}
    
    def salvar_usuarios(self):
        """
        💾 SALVAR USUÁRIOS NO ARQUIVO
        
        Esta função salva todos os dados dos usuários no arquivo JSON.
        É chamada sempre que algum dado é alterado (saldo, histórico, etc.).
        """
        with open(self.arquivo_usuarios, 'w', encoding='utf-8') as f:
            json.dump(self.usuarios, f, indent=2, ensure_ascii=False)
    
    def cadastrar(self):
        """
        📝 CADASTRAR NOVO USUÁRIO
        
        Esta função permite que uma nova pessoa se cadastre no sistema.
        Ela pede: nome de usuário, senha, pergunta secreta e resposta.
        A pergunta secreta serve para recuperar a senha se esquecer.
        """
        print("\n📝 CADASTRO DE USUÁRIO")
        
        # Pede o nome de usuário
        usuario = input("👤 Nome de usuário: ").strip()
        if not usuario or usuario in self.usuarios:
            print("❌ Usuário inválido ou já existe!")
            pausar()
            return False
        
        # Pede a senha
        senha = input("🔒 Senha: ").strip()
        if not senha:
            print("❌ Senha não pode estar vazia!")
            pausar()
            return False
        
        # Pede pergunta e resposta secreta para recuperação de senha
        pergunta = input("❓ Pergunta secreta: ").strip()
        resposta = input("💬 Resposta secreta: ").strip()
        
        # Cria o registro do usuário com todos os dados iniciais
        self.usuarios[usuario] = {
            "senha": senha,
            "pergunta_secreta": pergunta,
            "resposta_secreta": resposta,
            "saldo": 0.0,                    # Começa com saldo zero
            "pontos": 0,                     # Começa sem pontos
            "historico": [],                 # Lista vazia de transações
            "data_cadastro": datetime.now().isoformat()  # Data de quando se cadastrou
        }
        
        self.salvar_usuarios()  # Salva no arquivo
        return True
    
    def login(self):
        """
        👤 FAZER LOGIN
        
        Esta função permite que um usuário já cadastrado entre no sistema.
        Se errar a senha, pode tentar responder a pergunta secreta.
        """
        print("\n👤 LOGIN")
        
        # Pede o nome de usuário
        usuario = input("👤 Usuário: ").strip()
        if usuario not in self.usuarios:
            print("❌ Usuário não encontrado!")
            pausar()
            return None
        
        # Pede a senha
        senha = input("🔒 Senha: ").strip()
        if self.usuarios[usuario]["senha"] != senha:
            print("❌ Senha incorreta!")
            
            # Se errou a senha, oferece a pergunta secreta como alternativa
            print(f"\n❓ {self.usuarios[usuario]['pergunta_secreta']}")
            resposta = input("💬 Resposta: ").strip()
            
            # Compara as respostas (ignora maiúsculas/minúsculas)
            if self.usuarios[usuario]["resposta_secreta"].lower() != resposta.lower():
                print("❌ Resposta incorreta!")
                pausar()
                return None
        
        print("✅ Login realizado com sucesso!")
        pausar()
        return usuario  # Retorna o nome do usuário logado
    
    def get_saldo(self, usuario):
        """
        💰 CONSULTAR SALDO
        
        Esta função retorna quanto dinheiro o usuário tem na conta.
        """
        return self.usuarios[usuario]["saldo"]
    
    def get_pontos(self, usuario):
        """
        ⭐ CONSULTAR PONTOS
        
        Esta função retorna quantos pontos de recompensa o usuário tem.
        Os pontos são ganhos fazendo compras no cartão de crédito.
        """
        return self.usuarios[usuario].get("pontos", 0)
    
    def adicionar_pontos(self, usuario, pontos):
        """
        ⭐ ADICIONAR PONTOS
        
        Esta função adiciona pontos de recompensa ao usuário.
        É chamada quando ele faz compras no cartão de crédito.
        """
        if "pontos" not in self.usuarios[usuario]:
            self.usuarios[usuario]["pontos"] = 0
        self.usuarios[usuario]["pontos"] += pontos
        self.salvar_usuarios()
    
    def remover_pontos(self, usuario, pontos):
        """
        ⭐ REMOVER PONTOS
        
        Esta função remove pontos do usuário (quando ele troca por dinheiro).
        Garante que os pontos nunca fiquem negativos.
        """
        if "pontos" not in self.usuarios[usuario]:
            self.usuarios[usuario]["pontos"] = 0
        self.usuarios[usuario]["pontos"] = max(0, self.usuarios[usuario]["pontos"] - pontos)
        self.salvar_usuarios()
    
    def depositar(self, usuario, valor):
        """
        💰 FAZER DEPÓSITO
        
        Esta função adiciona dinheiro na conta do usuário.
        É como colocar dinheiro no banco.
        """
        if valor <= 0:
            print("❌ Valor deve ser positivo!")
            return False
        
        self.usuarios[usuario]["saldo"] += valor
        self.adicionar_historico(usuario, f"DEPÓSITO: +R$ {valor:.2f}")
        self.salvar_usuarios()
        return True
    
    def sacar(self, usuario, valor):
        """
        💸 FAZER SAQUE
        
        Esta função remove dinheiro da conta do usuário.
        Só funciona se ele tiver saldo suficiente.
        """
        if valor <= 0:
            print("❌ Valor deve ser positivo!")
            return False
        
        if self.usuarios[usuario]["saldo"] < valor:
            print("❌ Saldo insuficiente!")
            return False
        
        self.usuarios[usuario]["saldo"] -= valor
        self.adicionar_historico(usuario, f"SAQUE: -R$ {valor:.2f}")
        self.salvar_usuarios()
        return True
    
    def transferir(self, origem, destino, valor):
        """
        🔄 FAZER TRANSFERÊNCIA
        
        Esta função transfere dinheiro de um usuário para outro.
        Remove dinheiro da conta de origem e adiciona na conta de destino.
        """
        if destino not in self.usuarios:
            print("❌ Usuário de destino não encontrado!")
            return False
        
        if valor <= 0:
            print("❌ Valor deve ser positivo!")
            return False
        
        if self.usuarios[origem]["saldo"] < valor:
            print("❌ Saldo insuficiente!")
            return False
        
        # Remove da conta de origem
        self.usuarios[origem]["saldo"] -= valor
        # Adiciona na conta de destino
        self.usuarios[destino]["saldo"] += valor
        
        # Registra no histórico de ambos os usuários
        self.adicionar_historico(origem, f"TRANSFERÊNCIA ENVIADA para {destino}: -R$ {valor:.2f}")
        self.adicionar_historico(destino, f"TRANSFERÊNCIA RECEBIDA de {origem}: +R$ {valor:.2f}")
        
        self.salvar_usuarios()
        return True
    
    def adicionar_historico(self, usuario, transacao):
        """
        📊 ADICIONAR AO HISTÓRICO
        
        Esta função registra uma transação no histórico do usuário.
        Cada registro inclui data, hora e descrição da operação.
        """
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.usuarios[usuario]["historico"].append(f"[{timestamp}] {transacao}")
        self.salvar_usuarios()
    
    def mostrar_historico(self, usuario):
        """
        📊 MOSTRAR HISTÓRICO
        
        Esta função exibe as últimas 20 transações do usuário.
        É como um "extrato bancário".
        """
        print(f"\n📊 HISTÓRICO - {usuario}")
        historico = self.usuarios[usuario]["historico"]
        
        if not historico:
            print("📝 Nenhuma transação encontrada.")
            return
        
        # Mostra apenas as últimas 20 transações
        for transacao in historico[-20:]:
            print(transacao)
    
    def exportar_historico(self, usuario):
        """
        📄 EXPORTAR HISTÓRICO
        
        Esta função salva o histórico completo do usuário em um arquivo de texto.
        O arquivo é salvo com data e hora no nome para não sobrescrever.
        """
        historico = self.usuarios[usuario]["historico"]
        nome_arquivo = f"historico_{usuario}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(f"HISTÓRICO DE TRANSAÇÕES - {usuario}\n")
                f.write("=" * 50 + "\n\n")
                
                for transacao in historico:
                    f.write(transacao + "\n")
            
            print(f"✅ Histórico exportado para: {nome_arquivo}")
        except Exception as e:
            print(f"❌ Erro ao exportar: {e}")
    
    def get_todos_usuarios(self):
        """
        👥 OBTER TODOS OS USUÁRIOS
        
        Esta função retorna o dicionário com todos os usuários.
        É usada principalmente pelo painel administrativo.
        """
        return self.usuarios

# ============================================================================
# CLASSE GERENCIADOR DE CARTÕES
# ============================================================================

class CartaoManager:
    """
    💳 GERENCIADOR DE CARTÕES DE CRÉDITO
    
    Esta classe cuida de tudo relacionado aos cartões de crédito:
    - Criação de novos cartões
    - Compras e parcelamentos
    - Faturas e pagamentos
    - Geração de PDF das faturas
    
    É como o "departamento de cartões" do banco.
    """
    
    def __init__(self):
        """
        🏗️ CONSTRUTOR
        
        Quando criamos um CartaoManager, ele define onde salvar
        os dados dos cartões e carrega os cartões existentes.
        """
        self.arquivo_cartoes = "cartoes.json"
        self.cartoes = self.carregar_cartoes()
    
    def carregar_cartoes(self):
        """
        📂 CARREGAR CARTÕES DO ARQUIVO
        
        Esta função lê o arquivo JSON onde estão salvos todos os cartões.
        """
        if os.path.exists(self.arquivo_cartoes):
            try:
                with open(self.arquivo_cartoes, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def salvar_cartoes(self):
        """
        💾 SALVAR CARTÕES NO ARQUIVO
        
        Esta função salva todos os dados dos cartões no arquivo JSON.
        """
        with open(self.arquivo_cartoes, 'w', encoding='utf-8') as f:
            json.dump(self.cartoes, f, indent=2, ensure_ascii=False)
    
    def criar_cartao(self, usuario):
        """
        ➕ CRIAR NOVO CARTÃO
        
        Esta função cria um novo cartão de crédito para o usuário.
        O limite inicial é baseado em quantos cartões ele já tem:
        - 1º cartão: R$ 1.000
        - 2º cartão: R$ 2.000
        - 3º cartão: R$ 3.000
        - E assim por diante...
        """
        print("\n➕ SOLICITAÇÃO DE NOVO CARTÃO")
        
        # Conta quantos cartões o usuário já tem
        cartoes_usuario = self.get_cartoes_usuario(usuario)
        num_cartoes = len(cartoes_usuario)
        
        # Limite máximo de 5 cartões por usuário
        if num_cartoes >= 5:
            print("❌ Você já possui o máximo de 5 cartões!")
            pausar()
            return False
        
        # Calcula o limite baseado no número de cartões
        limite_inicial = (num_cartoes + 1) * 1000
        
        # Gera um número único para o cartão
        numero_cartao = gerar_numero_cartao()
        
        # Cria o registro do cartão
        self.cartoes[numero_cartao] = {
            "usuario": usuario,
            "limite": limite_inicial,
            "usado": 0.0,                    # Quanto já gastou
            "fatura_atual": 0.0,             # Valor da fatura atual
            "compras": [],                   # Lista de compras
            "parcelas": [],                  # Lista de parcelas pendentes
            "data_criacao": datetime.now().isoformat()
        }
        
        self.salvar_cartoes()
        print(f"✅ Cartão criado com sucesso!")
        print(f"💳 Número: {numero_cartao}")
        print(f"💰 Limite: R$ {limite_inicial:.2f}")
        pausar()
        return True
    
    def get_cartoes_usuario(self, usuario):
        """
        💳 OBTER CARTÕES DO USUÁRIO
        
        Esta função retorna uma lista com todos os cartões de um usuário.
        """
        cartoes_usuario = []
        for numero, dados in self.cartoes.items():
            if dados["usuario"] == usuario:
                cartoes_usuario.append({
                    "numero": numero,
                    "limite": dados["limite"],
                    "usado": dados["usado"],
                    "disponivel": dados["limite"] - dados["usado"]
                })
        return cartoes_usuario
    
    def fazer_compra(self, usuario, numero_cartao, valor, parcelas, descricao):
        """
        🛒 FAZER COMPRA NO CARTÃO
        
        Esta função processa uma compra no cartão de crédito.
        Pode ser à vista (1x) ou parcelada (até 24x).
        Aplica juros para parcelamentos acima de 6x.
        """
        if numero_cartao not in self.cartoes:
            print("❌ Cartão não encontrado!")
            return False
        
        cartao = self.cartoes[numero_cartao]
        
        if cartao["usuario"] != usuario:
            print("❌ Este cartão não pertence a você!")
            return False
        
        if valor <= 0:
            print("❌ Valor deve ser positivo!")
            return False
        
        if parcelas < 1 or parcelas > 24:
            print("❌ Número de parcelas deve ser entre 1 e 24!")
            return False
        
        # Calcula juros baseado no número de parcelas
        valor_final = valor
        if parcelas > 6:
            if parcelas <= 12:
                # 7-12 parcelas: 8% de juros
                valor_final = valor * 1.08
            else:
                # 13-24 parcelas: 12% de juros
                valor_final = valor * 1.12
        
        # Verifica se tem limite disponível
        if cartao["usado"] + valor_final > cartao["limite"]:
            print("❌ Limite insuficiente!")
            print(f"💰 Disponível: R$ {cartao['limite'] - cartao['usado']:.2f}")
            print(f"💸 Necessário: R$ {valor_final:.2f}")
            return False
        
        # Registra a compra
        compra = {
            "data": datetime.now().isoformat(),
            "descricao": descricao,
            "valor_original": valor,
            "valor_final": valor_final,
            "parcelas": parcelas,
            "valor_parcela": valor_final / parcelas
        }
        
        cartao["compras"].append(compra)
        cartao["usado"] += valor_final
        
        # Cria as parcelas
        for i in range(parcelas):
            data_vencimento = datetime.now() + timedelta(days=30 * i)  # 30 dias entre parcelas
            parcela = {
                "numero": i + 1,
                "valor": valor_final / parcelas,
                "descricao": descricao,
                "data_vencimento": data_vencimento.isoformat(),
                "paga": False,
                "moved_to_bill": i == 0  # Primeira parcela já vai para a fatura
            }
            cartao["parcelas"].append(parcela)
        
        # Primeira parcela já entra na fatura atual
        cartao["fatura_atual"] += valor_final / parcelas
        
        self.salvar_cartoes()
        
        if valor_final > valor:
            print(f"💰 Valor original: R$ {valor:.2f}")
            print(f"💸 Valor com juros: R$ {valor_final:.2f}")
            print(f"📊 Juros aplicados: {((valor_final/valor - 1) * 100):.1f}%")
        
        print(f"✅ Compra realizada em {parcelas}x de R$ {valor_final/parcelas:.2f}")
        return True
    
    def mostrar_fatura(self, usuario, numero_cartao):
        """
        🧾 MOSTRAR FATURA ATUAL
        
        Esta função exibe a fatura atual do cartão, mostrando
        todas as parcelas que vencem neste mês.
        """
        if numero_cartao not in self.cartoes:
            print("❌ Cartão não encontrado!")
            return
        
        cartao = self.cartoes[numero_cartao]
        
        if cartao["usuario"] != usuario:
            print("❌ Este cartão não pertence a você!")
            return
        
        print(f"\n🧾 FATURA DO CARTÃO {numero_cartao}")
        print("=" * 50)
        
        # Atualiza a fatura com parcelas vencidas
        self.atualizar_fatura(numero_cartao)
        
        if cartao["fatura_atual"] == 0:
            print("✅ Nenhuma fatura pendente!")
            return
        
        print(f"💰 Valor total da fatura: R$ {cartao['fatura_atual']:.2f}")
        print(f"📅 Data de vencimento: {(datetime.now() + timedelta(days=10)).strftime('%d/%m/%Y')}")
        
        print("\n📋 Itens da fatura:")
        for parcela in cartao["parcelas"]:
            if parcela["moved_to_bill"] and not parcela["paga"]:
                print(f"• {parcela['descricao']} - Parcela {parcela['numero']} - R$ {parcela['valor']:.2f}")
    
    def atualizar_fatura(self, numero_cartao):
        """
        🔄 ATUALIZAR FATURA
        
        Esta função verifica se há parcelas que venceram e devem
        ser adicionadas à fatura atual.
        """
        cartao = self.cartoes[numero_cartao]
        hoje = datetime.now()
        
        for parcela in cartao["parcelas"]:
            data_vencimento = datetime.fromisoformat(parcela["data_vencimento"])
            
            # Se a parcela venceu e ainda não foi movida para a fatura
            if data_vencimento <= hoje and not parcela["moved_to_bill"] and not parcela["paga"]:
                cartao["fatura_atual"] += parcela["valor"]
                parcela["moved_to_bill"] = True
        
        self.salvar_cartoes()
    
    def pagar_fatura(self, usuario, numero_cartao, valor, usuario_manager):
        """
        💰 PAGAR FATURA DO CARTÃO
        
        Esta função permite pagar a fatura do cartão usando
        o saldo da conta corrente.
        """
        if numero_cartao not in self.cartoes:
            print("❌ Cartão não encontrado!")
            return False
        
        cartao = self.cartoes[numero_cartao]
        
        if cartao["usuario"] != usuario:
            print("❌ Este cartão não pertence a você!")
            return False
        
        if valor <= 0:
            print("❌ Valor deve ser positivo!")
            return False
        
        if valor > cartao["fatura_atual"]:
            print(f"❌ Valor maior que a fatura! Fatura atual: R$ {cartao['fatura_atual']:.2f}")
            return False
        
        # Verifica se tem saldo na conta
        if not usuario_manager.sacar(usuario, valor):
            return False
        
        # Paga as parcelas proporcionalmente
        valor_restante = valor
        for parcela in cartao["parcelas"]:
            if parcela["moved_to_bill"] and not parcela["paga"] and valor_restante > 0:
                if valor_restante >= parcela["valor"]:
                    # Paga a parcela inteira
                    valor_restante -= parcela["valor"]
                    parcela["paga"] = True
                    cartao["usado"] -= parcela["valor"]
                else:
                    # Paga parcialmente
                    break
        
        cartao["fatura_atual"] -= valor
        if cartao["fatura_atual"] < 0.01:  # Evita valores muito pequenos
            cartao["fatura_atual"] = 0
        
        self.salvar_cartoes()
        usuario_manager.adicionar_historico(usuario, f"PAGAMENTO CARTÃO {numero_cartao}: -R$ {valor:.2f}")
        return True
    
    def gerar_fatura_pdf(self, usuario, numero_cartao):
        """
        📄 GERAR FATURA EM PDF
        
        Esta função cria um arquivo PDF com a fatura do cartão.
        O PDF inclui todas as informações da fatura de forma organizada.
        """
        if numero_cartao not in self.cartoes:
            print("❌ Cartão não encontrado!")
            return
        
        cartao = self.cartoes[numero_cartao]
        
        if cartao["usuario"] != usuario:
            print("❌ Este cartão não pertence a você!")
            return
        
        # Nome do arquivo PDF
        nome_arquivo = f"fatura_{numero_cartao}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        try:
            # Cria o documento PDF
            doc = SimpleDocTemplate(nome_arquivo, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Título
            titulo = Paragraph("FATURA DO CARTÃO DE CRÉDITO", styles['Title'])
            story.append(titulo)
            story.append(Spacer(1, 12))
            
            # Informações do cartão
            info_cartao = f"""
            <b>Número do Cartão:</b> {numero_cartao}<br/>
            <b>Titular:</b> {usuario}<br/>
            <b>Data da Fatura:</b> {datetime.now().strftime('%d/%m/%Y')}<br/>
            <b>Vencimento:</b> {(datetime.now() + timedelta(days=10)).strftime('%d/%m/%Y')}<br/>
            <b>Valor Total:</b> R$ {cartao['fatura_atual']:.2f}
            """
            
            info_para = Paragraph(info_cartao, styles['Normal'])
            story.append(info_para)
            story.append(Spacer(1, 20))
            
            # Tabela com os itens da fatura
            dados_tabela = [['Descrição', 'Parcela', 'Valor']]
            
            for parcela in cartao["parcelas"]:
                if parcela["moved_to_bill"] and not parcela["paga"]:
                    dados_tabela.append([
                        parcela['descricao'],
                        f"{parcela['numero']}",
                        f"R$ {parcela['valor']:.2f}"
                    ])
            
            if len(dados_tabela) > 1:  # Se tem itens além do cabeçalho
                tabela = Table(dados_tabela)
                tabela.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(tabela)
            
            # Gera o PDF
            doc.build(story)
            print(f"✅ Fatura PDF gerada: {nome_arquivo}")
            
        except Exception as e:
            print(f"❌ Erro ao gerar PDF: {e}")

# ============================================================================
# CLASSE GERENCIADOR DE INVESTIMENTOS
# ============================================================================

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
        self.arquivo_investimentos = "investimentos.json"
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
        self.arquivo_emprestimos = "emprestimos.json"
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

class AdminManager:
    """
    🔧 GERENCIADOR ADMINISTRATIVO
    
    Esta classe cuida das funções administrativas do sistema:
    - Login de administradores
    - Relatórios e estatísticas
    - Exportação de dados
    
    É como a "gerência" do banco.
    """
    
    def __init__(self):
        """
        🏗️ CONSTRUTOR
        
        Define a senha padrão do administrador.
        Em um sistema real, isso seria mais seguro.
        """
        self.senha_admin = "admin123"  # Senha padrão do administrador
    
    def login_admin(self):
        """
        🔐 LOGIN ADMINISTRATIVO
        
        Esta função permite que administradores façam login
        no painel administrativo.
        """
        print("\n🔐 LOGIN ADMINISTRATIVO")
        
        senha = input("🔒 Senha de administrador: ").strip()
        
        if senha != self.senha_admin:
            print("❌ Senha incorreta!")
            pausar()
            return False
        
        print("✅ Login administrativo realizado com sucesso!")
        pausar()
        return True
    
    def listar_usuarios(self, usuario_manager):
        """
        👥 LISTAR TODOS OS USUÁRIOS
        
        Esta função mostra uma lista de todos os usuários
        cadastrados no sistema com suas informações básicas.
        """
        usuarios = usuario_manager.get_todos_usuarios()
        
        print("\n👥 LISTA DE USUÁRIOS")
        print("=" * 80)
        
        if not usuarios:
            print("📝 Nenhum usuário cadastrado.")
            return
        
        for nome, dados in usuarios.items():
            data_cadastro = datetime.fromisoformat(dados["data_cadastro"]).strftime("%d/%m/%Y")
            print(f"👤 {nome}")
            print(f"   💰 Saldo: R$ {dados['saldo']:.2f}")
            print(f"   ⭐ Pontos: {dados.get('pontos', 0)}")
            print(f"   📅 Cadastro: {data_cadastro}")
            print(f"   📊 Transações: {len(dados['historico'])}")
            print()
    
    def mostrar_estatisticas(self, usuario_manager):
        """
        📊 MOSTRAR ESTATÍSTICAS GERAIS
        
        Esta função calcula e exibe estatísticas gerais do sistema:
        total de usuários, saldo total, transações, etc.
        """
        usuarios = usuario_manager.get_todos_usuarios()
        
        print("\n📊 ESTATÍSTICAS GERAIS DO SISTEMA")
        print("=" * 50)
        
        if not usuarios:
            print("📝 Nenhum dado disponível.")
            return
        
        # Calcula estatísticas
        total_usuarios = len(usuarios)
        saldo_total = sum(dados['saldo'] for dados in usuarios.values())
        pontos_total = sum(dados.get('pontos', 0) for dados in usuarios.values())
        transacoes_total = sum(len(dados['historico']) for dados in usuarios.values())
        
        # Usuário com maior saldo
        usuario_maior_saldo = max(usuarios.items(), key=lambda x: x[1]['saldo'])
        
        # Usuário mais ativo (mais transações)
        usuario_mais_ativo = max(usuarios.items(), key=lambda x: len(x[1]['historico']))
        
        print(f"👥 Total de usuários: {total_usuarios}")
        print(f"💰 Saldo total do sistema: R$ {saldo_total:.2f}")
        print(f"⭐ Pontos totais distribuídos: {pontos_total}")
        print(f"📊 Total de transações: {transacoes_total}")
        print(f"📈 Média de saldo por usuário: R$ {saldo_total/total_usuarios:.2f}")
        print(f"🏆 Usuário com maior saldo: {usuario_maior_saldo[0]} (R$ {usuario_maior_saldo[1]['saldo']:.2f})")
        print(f"🎯 Usuário mais ativo: {usuario_mais_ativo[0]} ({len(usuario_mais_ativo[1]['historico'])} transações)")
    
    def gerar_relatorio_csv(self, usuario_manager):
        """
        📄 GERAR RELATÓRIO CSV
        
        Esta função gera um arquivo CSV (planilha) com dados
        de todos os usuários do sistema.
        """
        usuarios = usuario_manager.get_todos_usuarios()
        nome_arquivo = f"relatorio_usuarios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Cabeçalho
                writer.writerow(['Usuario', 'Saldo', 'Pontos', 'Data_Cadastro', 'Total_Transacoes'])
                
                # Dados dos usuários
                for nome, dados in usuarios.items():
                    writer.writerow([
                        nome,
                        dados['saldo'],
                        dados.get('pontos', 0),
                        dados['data_cadastro'],
                        len(dados['historico'])
                    ])
            
            print(f"✅ Relatório CSV gerado: {nome_arquivo}")
            
        except Exception as e:
            print(f"❌ Erro ao gerar relatório CSV: {e}")
    
    def gerar_relatorio_pdf(self, usuario_manager):
        """
        📄 GERAR RELATÓRIO PDF
        
        Esta função gera um relatório completo em PDF
        com estatísticas e dados dos usuários.
        """
        usuarios = usuario_manager.get_todos_usuarios()
        nome_arquivo = f"relatorio_sistema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        try:
            doc = SimpleDocTemplate(nome_arquivo, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Título
            titulo = Paragraph("RELATÓRIO ADMINISTRATIVO DO SISTEMA BANCÁRIO", styles['Title'])
            story.append(titulo)
            story.append(Spacer(1, 12))
            
            # Data do relatório
            data_relatorio = Paragraph(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal'])
            story.append(data_relatorio)
            story.append(Spacer(1, 20))
            
            # Estatísticas gerais
            if usuarios:
                total_usuarios = len(usuarios)
                saldo_total = sum(dados['saldo'] for dados in usuarios.values())
                pontos_total = sum(dados.get('pontos', 0) for dados in usuarios.values())
                
                estatisticas = f"""
                <b>ESTATÍSTICAS GERAIS</b><br/>
                <br/>
                Total de usuários: {total_usuarios}<br/>
                Saldo total do sistema: R$ {saldo_total:.2f}<br/>
                Pontos totais distribuídos: {pontos_total}<br/>
                Média de saldo por usuário: R$ {saldo_total/total_usuarios:.2f}<br/>
                """
                
                stats_para = Paragraph(estatisticas, styles['Normal'])
                story.append(stats_para)
                story.append(Spacer(1, 20))
                
                # Tabela com dados dos usuários
                dados_tabela = [['Usuário', 'Saldo', 'Pontos', 'Transações']]
                
                for nome, dados in usuarios.items():
                    dados_tabela.append([
                        nome,
                        f"R$ {dados['saldo']:.2f}",
                        str(dados.get('pontos', 0)),
                        str(len(dados['historico']))
                    ])
                
                tabela = Table(dados_tabela)
                tabela.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(tabela)
            
            doc.build(story)
            print(f"✅ Relatório PDF gerado: {nome_arquivo}")
            
        except Exception as e:
            print(f"❌ Erro ao gerar relatório PDF: {e}")

# ============================================================================
# CLASSE GERENCIADOR DE AUDITORIA
# ============================================================================

class AuditoriaManager:
    """
    📝 GERENCIADOR DE AUDITORIA
    
    Esta classe cuida dos logs de segurança do sistema:
    - Registro de todas as ações dos usuários
    - Controle de acesso e segurança
    - Histórico de operações
    
    É como o "departamento de segurança" do banco.
    """
    
    def __init__(self):
        """
        🏗️ CONSTRUTOR
        
        Define onde salvar os logs de auditoria e carrega os existentes.
        """
        self.arquivo_logs = "auditoria.json"
        self.logs = self.carregar_logs()
    
    def carregar_logs(self):
        """
        📂 CARREGAR LOGS DO ARQUIVO
        """
        if os.path.exists(self.arquivo_logs):
            try:
                with open(self.arquivo_logs, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def salvar_logs(self):
        """
        💾 SALVAR LOGS NO ARQUIVO
        """
        with open(self.arquivo_logs, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, indent=2, ensure_ascii=False)
    
    def log_acao(self, usuario, acao, detalhes):
        """
        📝 REGISTRAR AÇÃO NO LOG
        
        Esta função registra uma ação do usuário no log de auditoria.
        Cada registro inclui: usuário, ação, detalhes, data e hora.
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "usuario": usuario,
            "acao": acao,
            "detalhes": detalhes,
            "ip": "127.0.0.1"  # Em um sistema real, seria o IP real do usuário
        }
        
        self.logs.append(log_entry)
        self.salvar_logs()
        
        # Mantém apenas os últimos 1000 logs para não ocupar muito espaço
        if len(self.logs) > 1000:
            self.logs = self.logs[-1000:]
            self.salvar_logs()
    
    def mostrar_logs(self, limite=50):
        """
        📋 MOSTRAR LOGS DE AUDITORIA
        
        Esta função exibe os logs mais recentes do sistema.
        É útil para administradores verificarem atividades suspeitas.
        """
        print(f"\n📋 LOGS DE AUDITORIA (Últimos {limite})")
        print("=" * 80)
        
        if not self.logs:
            print("📝 Nenhum log encontrado.")
            return
        
        # Mostra os logs mais recentes primeiro
        logs_recentes = self.logs[-limite:]
        logs_recentes.reverse()
        
        for log in logs_recentes:
            timestamp = datetime.fromisoformat(log["timestamp"]).strftime("%d/%m/%Y %H:%M:%S")
            print(f"[{timestamp}] {log['usuario']} - {log['acao']}: {log['detalhes']}")

# ============================================================================
# FUNÇÕES DO MENU PRINCIPAL
# ============================================================================

def main():
    """
    🚀 FUNÇÃO PRINCIPAL DO SISTEMA
    
    Esta é a primeira função que roda quando o programa inicia.
    É como a "porta de entrada" do banco - aqui o cliente decide
    se quer fazer login, se cadastrar ou se é um administrador.
    """
    
    # Limpa a tela para começar "limpo"
    limpar_tela()
    
    # Mostra o título bonito do sistema
    print("=" * 50)
    print("🏦 SISTEMA BANCÁRIO AVANÇADO")
    print("=" * 50)
    
    # Cada manager é responsável por uma área específica
    usuario_manager = UsuarioManager()           # Gerente de usuários
    cartao_manager = CartaoManager()             # Gerente de cartões
    admin_manager = AdminManager()               # Gerente administrativo
    investimento_manager = InvestimentoManager() # Gerente de investimentos
    emprestimo_manager = EmprestimoManager()     # Gerente de empréstimos
    auditoria = AuditoriaManager()               # Gerente de segurança/logs
    
    # Loop infinito - o sistema só para quando o usuário escolhe "Sair"
    while True:
        # Sempre limpa a tela antes de mostrar o menu
        limpar_tela()
        
        print("\n🏠 MENU PRINCIPAL")
        print("1. 👤 Login")           # Para usuários já cadastrados
        print("2. 📝 Cadastrar")       # Para novos usuários
        print("3. 🔧 Painel Administrativo")  # Para administradores
        print("4. 🚪 Sair")           # Para fechar o programa
        
        # Pede para o usuário escolher uma opção
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            # Tenta fazer login do usuário
            usuario_logado = usuario_manager.login()
            
            # Se o login deu certo, registra no log e vai para o menu do usuário
            if usuario_logado:
                auditoria.log_acao(usuario_logado, "LOGIN", "Login realizado com sucesso")
                # Chama o menu específico do usuário logado
                menu_usuario(usuario_logado, usuario_manager, cartao_manager, 
                           investimento_manager, emprestimo_manager, auditoria)
        
        elif opcao == "2":
            # Tenta cadastrar um novo usuário
            if usuario_manager.cadastrar():
                print("✅ Usuário cadastrado com sucesso!")
                pausar()  # Pausa para o usuário ler a mensagem
        
        elif opcao == "3":
            # Tenta fazer login como administrador
            if admin_manager.login_admin():
                # Se deu certo, vai para o menu administrativo
                menu_admin(admin_manager, usuario_manager, auditoria)
        
        elif opcao == "4":
            # Usuário quer sair - encerra o programa
            print("👋 Obrigado por usar nosso sistema!")
            break  # Sai do loop infinito
        
        else:
            # Opção inválida - mostra erro e continua no loop
            print("❌ Opção inválida!")
            pausar()

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
                trocar_pontos_por_saldo(usuario, usuario_manager, auditoria)
            
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

def trocar_pontos_por_saldo(usuario, usuario_manager, auditoria):
    """
    ⭐ SISTEMA DE TROCA DE PONTOS
    
    Esta função permite que o usuário troque seus pontos de recompensa
    por dinheiro real na conta. É como um "programa de fidelidade".
    
    Taxa de conversão: 100 pontos = R$ 5,00
    """
    
    pontos = usuario_manager.get_pontos(usuario)
    print(f"\n⭐ Você tem {pontos} pontos")
    print("💰 Taxa de conversão: 100 pontos = R$ 5,00")
    
    # Se não tem pontos suficientes para trocar
    if pontos < 100:
        print("❌ Você precisa de pelo menos 100 pontos para trocar!")
        pausar()
        return  # Sai da função
    
    max_conversao = pontos // 100  # Quantos grupos de 100 pontos tem
    print(f"🔄 Você pode converter até {max_conversao * 100} pontos (R$ {max_conversao * 5:.2f})")
    
    try:
        pontos_converter = int(input("Quantos pontos deseja converter? "))
        
        if pontos_converter % 100 != 0:  # Tem que ser múltiplo de 100
            print("❌ Você deve converter múltiplos de 100 pontos!")
            pausar()
            return
        
        if pontos_converter > pontos:  # Não pode converter mais do que tem
            print("❌ Você não tem pontos suficientes!")
            pausar()
            return
        
        valor_saldo = (pontos_converter // 100) * 5  # Cada 100 pontos = R$ 5
        usuario_manager.remover_pontos(usuario, pontos_converter)  # Remove os pontos
        usuario_manager.depositar(usuario, valor_saldo)           # Adiciona o dinheiro
        
        # Registra a operação
        auditoria.log_acao(usuario, "TROCA_PONTOS", 
                         f"Converteu {pontos_converter} pontos em R$ {valor_saldo:.2f}")
        print(f"✅ Conversão realizada! R$ {valor_saldo:.2f} adicionados ao seu saldo!")
        
    except ValueError:
        print("❌ Valor inválido!")
    
    pausar()

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
        
        print("1. 👥 Listar usuários")         # Ver todos os usuários cadastrados
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
