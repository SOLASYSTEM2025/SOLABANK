from managers.usuarios import UsuarioManager
from managers.cartoes import CartaoManager
from managers.investimentos import InvestimentoManager
from managers.emprestimos import EmprestimoManager
from managers.admin import AdminManager
from managers.auditoria import AuditoriaManager

from menus.menu_usuario import menu_usuario
from menus.menu_admin import menu_admin

from utils.helpers import limpar_tela, pausar

def main():
    """
    🚀 FUNÇÃO PRINCIPAL DO SISTEMA
    """
    limpar_tela()
    print("=" * 50)
    print("🏦 SOLABANK, O BANCO IDEAL PARA VOCÊ!")
    print("=" * 50)

    usuario_manager = UsuarioManager()
    cartao_manager = CartaoManager()
    admin_manager = AdminManager()
    investimento_manager = InvestimentoManager()
    emprestimo_manager = EmprestimoManager()
    auditoria = AuditoriaManager()

    while True:
        limpar_tela()
        print("\n🏠 MENU PRINCIPAL")
        print("1. 👤 Login")
        print("2. 📝 Cadastrar")
        print("3. 🔧 Painel Administrativo")
        print("4. 🚪 Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            usuario_logado = usuario_manager.login()
            if usuario_logado:
                auditoria.log_acao(usuario_logado, "LOGIN", "Login realizado com sucesso")
                menu_usuario(usuario_logado, usuario_manager, cartao_manager,
                             investimento_manager, emprestimo_manager, auditoria)

        elif opcao == "2":
            if usuario_manager.cadastrar():
                print("✅ Usuário cadastrado com sucesso!")
                pausar()

        elif opcao == "3":
            if admin_manager.login_admin():
                menu_admin(admin_manager, usuario_manager, auditoria)

        elif opcao == "4":
            print("👋 Obrigado por usar nosso sistema!")
            break

        else:
            print("❌ Opção inválida!")
            pausar()

if __name__ == "__main__":
    main()
