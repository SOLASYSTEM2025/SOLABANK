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
        self.arquivo_usuarios = "data/usuarios.json"
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
