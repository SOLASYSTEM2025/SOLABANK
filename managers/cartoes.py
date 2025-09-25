import datetime
import json
import os
from pydoc import pager

from matplotlib import colors
from matplotlib.table import Table
from networkx import star_graph

from utils.helpers import gerar_numero_cartao, pausar

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
        self.arquivo_cartoes = "data/cartoes.json"
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
            data_vencimento = datetime.now() + datetime.timedelta(days=30 * i)  # 30 dias entre parcelas
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
        print(f"📅 Data de vencimento: {(datetime.now() + datetime.timedelta(days=10)).strftime('%d/%m/%Y')}")
        
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
            doc = SimpleDocTemplate(nome_arquivo, pagesize=letter) # type: ignore
            styles = getSampleStyleSheet() # type: ignore
            story = []
            
            # Título
            titulo = star_graph("FATURA DO CARTÃO DE CRÉDITO", styles['Title'])
            story.append(titulo)
            story.append(pager(1, 12))
            
            # Informações do cartão
            info_cartao = f"""
            <b>Número do Cartão:</b> {numero_cartao}<br/>
            <b>Titular:</b> {usuario}<br/>
            <b>Data da Fatura:</b> {datetime.now().strftime('%d/%m/%Y')}<br/>
            <b>Vencimento:</b> {(datetime.now() + datetime.timedelta(days=10)).strftime('%d/%m/%Y')}<br/>
            <b>Valor Total:</b> R$ {cartao['fatura_atual']:.2f}
            """
            
            info_para = star_graph(info_cartao, styles['Normal'])
            story.append(info_para)
            story.append(pager(1, 20))
            
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
                tabela.setStyle(TableStyle([ # type: ignore
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
