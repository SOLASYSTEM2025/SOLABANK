from datetime import datetime
import json
import os

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
        self.arquivo_logs = "data/auditoria.json"
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
