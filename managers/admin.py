import csv
import datetime
from pydoc import pager

from matplotlib import colors
from matplotlib.table import Table
from networkx import star_graph
from utils.helpers import pausar


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
        self.senha_admin = "verdaotetra"  # Senha padrão do administrador
    
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
            doc = SimpleDocTemplate(nome_arquivo, pagesize=letter) # pyright: ignore[reportUndefinedVariable]
            styles = getSampleStyleSheet() # type: ignore
            story = []
            
            # Título
            titulo = star_graph("RELATÓRIO ADMINISTRATIVO DO SISTEMA BANCÁRIO", styles['Title'])
            story.append(titulo)
            story.append(pager(1, 12))
            
            # Data do relatório
            data_relatorio = star_graph(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal'])
            story.append(data_relatorio)
            story.append(pager(1, 20))
            
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
                
                stats_para = star_graph(estatisticas, styles['Normal'])
                story.append(stats_para)
                story.append(pager(1, 20))
                
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
                tabela.setStyle(TableStyle([ # type: ignore
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
