# ===================================================================
# SISTEMA BANCÁRIO COMPLETO EM PYTHON
# ===================================================================

import json
import os
import random
from datetime import datetime, timedelta
import csv

# --- CONSTANTES DO SISTEMA ---
ADMIN_USERNAME = "admin"  # Nome de usuário do administrador
ADMIN_PASSWORD = "admin_password"  # Senha do administrador

# Taxa de desconto ao quitar dívida (10% por padrão)
QUIT_DISCOUNT = 0.10

# Lista de perguntas secretas disponíveis para os usuários
SECRET_QUESTIONS = [
    "Qual o nome do seu primeiro pet?",
    "Qual o nome da sua cidade natal?",
    "Qual o nome da sua mãe?",
    "Qual o nome da sua escola primária?",
    "Qual o seu filme favorito?",
    "Qual a sua cor favorita?",
    "Qual o seu esporte favorito?",
    "Qual o nome do seu melhor amigo de infância?",
    "Qual o nome do seu professor favorito?",
    "Qual o nome da sua banda favorita?",
]

# --- FUNÇÕES AUXILIARES ---

def formatar_moeda(valor):
    """
    Formata um valor numérico para o formato de moeda brasileira (R$)
    Exemplo: 1234.56 -> R$1.234,56
    """
    return f"R${valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def gerar_numero_cartao():
    """
    Gera um número de cartão de crédito aleatório com 16 dígitos
    """
    return ''.join([str(random.randint(0, 9)) for _ in range(16)])

def gerar_cvv():
    """
    Gera um código CVV aleatório com 3 dígitos
    """
    return ''.join([str(random.randint(0, 9)) for _ in range(3)])

def gerar_data_vencimento():
    """
    Gera uma data de vencimento do cartão (4 anos no futuro)
    Formato: MM/YY
    """
    future_date = datetime.now() + timedelta(days=4 * 365)
    return future_date.strftime("%m/%y")

def gerar_limite_inicial():
    """
    Gera um limite inicial aleatório para o cartão de crédito
    Entre R$100,00 e R$500,00
    """
    return round(random.uniform(100.00, 500.00), 2)

def gerar_pergunta_secreta_aleatoria():
    """
    Seleciona uma pergunta secreta aleatória da lista disponível
    """
    return random.choice(SECRET_QUESTIONS)

def calcular_juros_fatura(valor_fatura, dias_atraso, is_negativado=False):
    """
    Calcula juros sobre fatura em atraso
    Taxa normal: 0.1% ao dia
    Taxa para negativado: 0.3% ao dia (3x maior)
    """
    if is_negativado:
        juros_diario = 0.003  # 0.3% ao dia para negativados
    else:
        juros_diario = 0.001  # 0.1% ao dia normal

    juros_total = valor_fatura * juros_diario * dias_atraso
    return round(juros_total, 2)

def calcular_juros_parcela(valor, parcelas):
    """
    Calcula juros baseado no número de parcelas
    - 1 parcela: 0% de juros
    - 2-3 parcelas: 2% de juros
    - 4-6 parcelas: 5% de juros
    - 7-12 parcelas: 8% de juros
    - Mais de 12 parcelas: 12% de juros
    """
    if parcelas <= 1:
        juros_percentual = 0.0
    elif parcelas <= 3:
        juros_percentual = 0.02
    elif parcelas <= 6:
        juros_percentual = 0.05
    elif parcelas <= 12:
        juros_percentual = 0.08
    else:
        juros_percentual = 0.12

    juros_total = valor * juros_percentual
    return round(juros_total, 2)

def calcular_limite_disponivel(cc_data):
    """
    Calcula o limite disponível real do cartão
    Limite disponível = Limite total - Fatura atual - Valor das parcelas futuras (não lançadas)
    """
    limite_total = cc_data['limit']
    fatura_atual = cc_data['current_bill']

    # Soma o valor de todas as parcelas futuras NÃO PAGAS e NÃO LANÇADAS na fatura
    valor_parcelas_futuras = 0
    for parcela in cc_data.get('installments', []):
        # se parcela ainda não foi paga e não foi movida para a fatura (moved_to_bill == False), conta-a como futura
        if not parcela.get('paid', False) and not parcela.get('moved_to_bill', False):
            valor_parcelas_futuras += parcela['amount']

        # se parcela não paga mas já foi movida_to_bill, seu valor já está dentro de fatura_atual
        # então não somamos aqui para evitar duplicidade

    limite_disponivel = limite_total - fatura_atual - valor_parcelas_futuras
    return round(limite_disponivel, 2)

def verificar_negativacao(cc_data):
    """
    Verifica se o cartão está negativado
    Negativado = quando a fatura atual + parcelas futuras > limite total
    """
    limite_total = cc_data['limit']
    fatura_atual = cc_data['current_bill']

    valor_parcelas_futuras = 0
    for parcela in cc_data.get('installments', []):
        if not parcela.get('paid', False) and not parcela.get('moved_to_bill', False):
            valor_parcelas_futuras += parcela['amount']

    total_devido = fatura_atual + valor_parcelas_futuras
    return total_devido > limite_total

def exportar_historico_csv(username, periodo):
    """
    Exporta o histórico de transações para um arquivo CSV
    Períodos disponíveis:
    1 - Último mês
    2 - Últimos 5 meses
    3 - Desde uma data específica
    4 - Todas as transações
    """
    historico_path = f"{username}_historico.txt"

    # Verifica se existe histórico para o usuário
    if not os.path.exists(historico_path):
        print("\nNenhuma transação registrada ainda para exportar.")
        return

    # Lê e processa todas as transações do arquivo
    transacoes = []
    with open(historico_path, "r") as f:
        for line in f:
            try:
                # Separa data e descrição da transação
                parts = line.strip().split('] ', 1)
                date_str = parts[0][1:]  # Remove o '[' inicial
                description = parts[1]

                # Converte string de data para objeto datetime
                transacao_data = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
                transacoes.append({'data': transacao_data, 'descricao': description})
            except Exception as e:
                print(f"Erro ao parsear linha do histórico: {line.strip()} - {e}")
                continue

    # Filtra transações baseado no período selecionado
    transacoes_filtradas = []
    data_limite = None

    if periodo == '1':  # Último mês
        data_limite = datetime.now() - timedelta(days=30)
    elif periodo == '2':  # Últimos 5 meses
        data_limite = datetime.now() - timedelta(days=5 * 30)
    elif periodo == '3':  # Data específica
        while True:
            data_str_input = input("Digite a data inicial (DD/MM/AAAA): ")
            try:
                data_limite = datetime.strptime(data_str_input, "%d/%m/%Y")
                break
            except ValueError:
                print("Formato de data inválido. Use DD/MM/AAAA.")
    # Para período '4', data_limite permanece None (todas as transações)

    # Aplica o filtro de data
    for t in transacoes:
        if data_limite is None or t['data'] >= data_limite:
            transacoes_filtradas.append(t)

    # Verifica se há transações para exportar
    if not transacoes_filtradas:
        print("\nNenhuma transação encontrada para o período selecionado.")
        return

    # Cria o arquivo CSV
    output_filename = f"{username}_historico_{periodo}.csv"
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Data', 'Descrição']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Escreve cabeçalho e dados
        writer.writeheader()
        for t in transacoes_filtradas:
            writer.writerow({
                'Data': t['data'].strftime("%d/%m/%Y %H:%M:%S"),
                'Descrição': t['descricao']
            })
    print(f"\nHistórico exportado para '{output_filename}' com sucesso!")

def roll_over_installments(cc_data):
    """
    Processa o ciclo mensal do cartão de crédito:
    - Verifica parcelas cujo due_date <= hoje e que ainda não foram movidas para a fatura (moved_to_bill == False)
    - Move cada parcela vencida para a fatura atual e marca como moved_to_bill = True
    - Aplica juros na fatura em atraso (se aplicável)
    """
    # Garante estrutura padrão
    if 'installments' not in cc_data:
        cc_data['installments'] = []
    if 'last_bill_date' not in cc_data or not cc_data['last_bill_date']:
        cc_data['last_bill_date'] = datetime.now().strftime("%Y-%m-%d")
        return

    # Calcula dias desde a última fatura para possíveis juros
    last_bill_date = datetime.strptime(cc_data['last_bill_date'], "%Y-%m-%d")
    days_since_last_bill = (datetime.now() - last_bill_date).days

    # Aplica juros se há fatura pendente (antes de mover novas parcelas para a fatura)
    if cc_data.get('current_bill', 0) > 0 and days_since_last_bill > 0:
        is_negativado = verificar_negativacao(cc_data)
        juros_aplicado = calcular_juros_fatura(cc_data['current_bill'], days_since_last_bill, is_negativado)
        if juros_aplicado > 0:
            cc_data['current_bill'] += juros_aplicado
            if is_negativado:
                print(f"⚠️ Juros majorados por negativação aplicados: {formatar_moeda(juros_aplicado)}")
            else:
                print(f"⚠️ Juros aplicados à fatura em atraso: {formatar_moeda(juros_aplicado)}")

    # Move parcelas vencidas (ou com due_date <= hoje) para a fatura atual
    hoje = datetime.now().date()
    moved_any = False
    for parcela in cc_data.get('installments', []):
        if parcela.get('paid', False):
            continue  # já paga

        # Parse due_date
        due_date_str = parcela.get('due_date')
        if not due_date_str:
            continue

        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except Exception:
            # se formato inesperado, ignore
            continue

        if due_date <= hoje and not parcela.get('moved_to_bill', False):
            # Lança essa parcela na fatura atual
            cc_data['current_bill'] += parcela['amount']
            parcela['moved_to_bill'] = True
            moved_any = True
            print(f"➡️ Parcela {parcela['installment_number']}/{parcela['total_installments']} de {formatar_moeda(parcela['amount'])} lançada na fatura (vencimento {parcela['due_date']}).")

    if moved_any:
        # Atualiza last_bill_date se movemos parcelas hoje (indicando novo ciclo)
        cc_data['last_bill_date'] = datetime.now().strftime("%Y-%m-%d")

# --- OPERAÇÕES DE BANCO DE DADOS ---

def carregar_usuarios():
    """
    Carrega dados dos usuários do arquivo JSON
    Se o arquivo não existir, cria um novo
    Também atualiza estruturas antigas para incluir novos campos
    """
    # Cria arquivo se não existir
    if not os.path.exists("usuarios.json"):
        with open("usuarios.json", "w") as f:
            json.dump({}, f)

    # Carrega dados existentes
    with open("usuarios.json", "r") as f:
        usuarios = json.load(f)

    # Atualiza estruturas antigas para incluir novos campos
    for user_data in usuarios.values():
        # Adiciona cartão de crédito se não existir
        if 'credit_card' not in user_data:
            user_data['credit_card'] = {
                'number': gerar_numero_cartao(),
                'cvv': gerar_cvv(),
                'expiry_date': gerar_data_vencimento(),
                'limit': gerar_limite_inicial(),
                'current_bill': 0.0,
                'last_bill_date': datetime.now().strftime("%Y-%m-%d"),
                'installments': []
            }

        # Adiciona pergunta secreta se não existir
        if 'pergunta' not in user_data:
            user_data['pergunta'] = gerar_pergunta_secreta_aleatoria()

        # Adiciona resposta secreta se não existir
        if 'resposta' not in user_data:
            user_data['resposta'] = ""

        # Adiciona contadores de atividade para aumento de limite
        if 'last_activity_deposit' not in user_data:
            user_data['last_activity_deposit'] = 0.0
        if 'last_activity_transfer' not in user_data:
            user_data['last_activity_transfer'] = 0.0

        # Garante histórico
        if 'historico' not in user_data:
            user_data['historico'] = []

    return usuarios

def salvar_usuarios(usuarios):
    """
    Salva dados dos usuários no arquivo JSON
    """
    with open("usuarios.json", "w") as f:
        json.dump(usuarios, f, indent=4)

def registrar_transacao(username, tipo, valor):
    """
    Registra uma transação no histórico do usuário
    Cria um arquivo de texto com timestamp para cada transação
    Além disso, adiciona ao campo 'historico' no JSON para referências futuras.
    """
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log = f"[{data}] {tipo} de {formatar_moeda(valor)}\n"

    # Adiciona ao arquivo de histórico do usuário
    with open(f"{username}_historico.txt", "a") as f:
        f.write(log)

    # Também registra no JSON (se usuário existir)
    try:
        with open("usuarios.json", "r") as f:
            usuarios = json.load(f)
        if username in usuarios:
            usuarios[username].setdefault('historico', [])
            usuarios[username]['historico'].append(log.strip())
            with open("usuarios.json", "w") as f:
                json.dump(usuarios, f, indent=4)
    except Exception:
        pass  # se algo falhar aqui, não é crítico

def resetar_banco_de_dados():
    """
    Reseta completamente o banco de dados
    Remove todos os usuários e históricos
    Requer confirmação do administrador
    """
    confirmacao = input("❗ Deseja realmente resetar o banco de dados e apagar todos os usuários? (s/n): ").strip().lower()

    if confirmacao == 's':
        # Remove arquivo principal de usuários
        if os.path.exists("usuarios.json"):
            os.remove("usuarios.json")
            print("✅ Banco de dados apagado com sucesso!")
        else:
            print("⚠️ Arquivo de banco de dados não encontrado.")

        # Remove todos os arquivos de histórico e CSV
        for arquivo in os.listdir():
            if arquivo.endswith("_historico.txt") or arquivo.endswith(".csv"):
                os.remove(arquivo)

        print("✅ Todos os históricos de transações e arquivos exportados também foram apagados.")
        return True

    return False

# --- PAINEL ADMINISTRATIVO ---

def admin_panel(usuarios):
    """
    Interface administrativa do sistema
    Permite visualizar dados de todos os usuários e resetar o banco
    """
    while True:
        print("\n==================== PAINEL ADMINISTRATIVO ====================")
        print("1 - Ver todos os dados dos clientes")
        print("2 - Resetar banco de dados")
        print("3 - Sair do painel administrativo")
        print("===============================================================")
        opcao_admin = input("Escolha uma opção: ")

        if opcao_admin == '1':
            # Exibe dados completos de todos os usuários
            print("\n===== DADOS DE TODOS OS CLIENTES =====")
            if not usuarios:
                print("Nenhum usuário cadastrado.")
            else:
                for username, data in usuarios.items():
                    print(f"\n--- Usuário: {username} ---")
                    print(f"  Saldo: {formatar_moeda(data.get('saldo', 0))}")
                    print(f"  Senha (hash): {'*' * len(data.get('senha', ''))}")
                    print(f"  Pergunta Secreta: {data.get('pergunta', 'N/A')}")
                    print(f"  Resposta Secreta: {data.get('resposta', 'N/A')}")

                    # Dados do cartão de crédito
                    cc = data.get('credit_card', {})
                    print(f"  Cartão de Crédito:")
                    print(f"    Número: {cc.get('number', 'N/A')}")
                    print(f"    CVV: {cc.get('cvv', 'N/A')}")
                    print(f"    Vencimento: {cc.get('expiry_date', 'N/A')}")
                    print(f"    Limite Total: {formatar_moeda(cc.get('limit', 0))}")
                    print(f"    Fatura Atual: {formatar_moeda(cc.get('current_bill', 0))}")
                    print(f"    Limite Disponível: {formatar_moeda(calcular_limite_disponivel(cc))}")
                    print(f"    Status: {'NEGATIVADO' if verificar_negativacao(cc) else 'NORMAL'}")
                    print(f"    Última Fatura: {cc.get('last_bill_date', 'N/A')}")
                    print(f"    Parcelas Totais: {len(cc.get('installments', []))}")
                    if cc.get('installments'):
                        for p in cc['installments']:
                            status = 'Pago' if p.get('paid', False) else ('Na fatura' if p.get('moved_to_bill', False) else 'Futura')
                            print(f"      - Parc {p.get('installment_number')}/{p.get('total_installments')}: {formatar_moeda(p.get('amount'))} - {status} - Venc: {p.get('due_date')}")
                    # Atividade para cálculo de limite
                    print(f"  Atividade Depósito (para limite): {formatar_moeda(data.get('last_activity_deposit', 0))}")
                    print(f"  Atividade Transferência (para limite): {formatar_moeda(data.get('last_activity_transfer', 0))}")
            print("========================================")

        elif opcao_admin == '2':
            # Opção para resetar banco de dados
            if resetar_banco_de_dados():
                return True  # Indica que o banco foi resetado

        elif opcao_admin == '3':
            # Sair do painel administrativo
            print("\nSaindo do painel administrativo.")
            break

        else:
            print("\nOpção inválida. Tente novamente.")

    return False  # Indica que o banco não foi resetado

# --- LÓGICA DO CARTÃO DE CRÉDITO ---

def pagar_fatura_e_alocar_a_parcelas(username, user_data, cc_data, valor_a_pagar):
    """
    Processa o pagamento da fatura:
    - Deduz do saldo do usuário
    - Aloca o pagamento para parcelas que já foram movidas para a fatura (moved_to_bill==True)
      preenchendo o campo 'paid_amount' por parcela e marcando 'paid' quando completada.
    - Reduz cc_data['current_bill'] conforme o valor pago.
    - Registra a transação e salva os usuários.
    """
    if valor_a_pagar <= 0:
        print("Valor inválido para pagamento.")
        return False

    if user_data['saldo'] < valor_a_pagar:
        print("\nSaldo insuficiente para pagar o valor desejado.")
        return False

    restante = valor_a_pagar
    # Deduz do saldo imediatamente
    user_data['saldo'] -= valor_a_pagar

    # Ordena parcelas por due_date que já foram movidas para a fatura e não pagas
    parcelas_ord = sorted(
        [p for p in cc_data.get('installments', []) if p.get('moved_to_bill', False) and not p.get('paid', False)],
        key=lambda x: x.get('due_date', '')
    )

    for p in parcelas_ord:
        if restante <= 0:
            break
        paid_amount = p.get('paid_amount', 0.0)
        need = p['amount'] - paid_amount
        if need <= 0:
            p['paid'] = True
            continue
        if restante >= need:
            # Quite essa parcela
            restante -= need
            p['paid_amount'] = p.get('paid_amount', 0.0) + need
            p['paid'] = True
            cc_data['current_bill'] -= need
        else:
            # Pagamento parcial da parcela
            p['paid_amount'] = p.get('paid_amount', 0.0) + restante
            cc_data['current_bill'] -= restante
            restante = 0

    # Se ainda restou valor (pode ser porque o usuário pagou mais que as parcelas movidas),
    # abate do valor numérico da fatura (caso haja outros componentes como juros)
    if restante > 0:
        # restante aqui é negativo (já deduzimos), mas como usamos 'restante' subtraímos do current_bill:
        # na prática, se cc_data['current_bill'] > 0, reduzimos, senão ignora (saldo já foi deduzido)
        reduction = min(valor_a_pagar, cc_data.get('current_bill', 0.0))
        cc_data['current_bill'] = round(max(0.0, cc_data.get('current_bill', 0.0) - reduction), 2)

    registrar_transacao(username, "Pagamento Fatura Cartão", valor_a_pagar)
    salvar_usuarios(usuarios)
    print(f"\nPagamento de {formatar_moeda(valor_a_pagar)} realizado e descontado do saldo.")
    print(f"Fatura restante: {formatar_moeda(cc_data.get('current_bill', 0.0))}")
    return True

def quitar_divida_total(username, user_data, cc_data):
    """
    Calcula a dívida total (todas as parcelas não pagas, inclusive futuras),
    aplica desconto e tenta quitar tudo de uma vez.
    """
    # Soma total das parcelas não pagas (considerando paid_amount)
    total_devido = 0.0
    for p in cc_data.get('installments', []):
        if not p.get('paid', False):
            paid_amount = p.get('paid_amount', 0.0)
            total_devido += max(0.0, p['amount'] - paid_amount)

    # Não duplicar current_bill: installments já incluem o que foi movido_to_bill,
    # mas caso haja juros que foram adicionados à current_bill que não pertencem a parcelas, consideramos também:
    # Para simplicidade, também adicionamos current_bill extras não cobertos por parcelas:
    soma_parcelas_moved = sum(p['amount'] - p.get('paid_amount',0.0) for p in cc_data.get('installments', []) if p.get('moved_to_bill', False) and not p.get('paid', False))
    # Caso haja diferença entre current_bill e soma_parcelas_moved (ex: juros),
    # consideramos o que restar:
    diferenca_juros = max(0.0, cc_data.get('current_bill', 0.0) - soma_parcelas_moved)
    total_devido += diferenca_juros

    if total_devido <= 0:
        print("Não há dívida pendente para quitar.")
        return False

    desconto = round(total_devido * QUIT_DISCOUNT, 2)
    total_com_desconto = round(total_devido - desconto, 2)

    print(f"\nDívida total: {formatar_moeda(total_devido)}")
    print(f"Desconto por quitação ({int(QUIT_DISCOUNT*100)}%): {formatar_moeda(desconto)}")
    print(f"Total a pagar para quitar tudo: {formatar_moeda(total_com_desconto)}")

    confirmar = input("Deseja quitar toda a dívida com desconto? (s/n): ").strip().lower()
    if confirmar != 's':
        print("Quitar dívida cancelado.")
        return False

    if user_data['saldo'] < total_com_desconto:
        print("\nSaldo insuficiente para quitar toda a dívida.")
        return False

    # Deduz do saldo
    user_data['saldo'] -= total_com_desconto

    # Marca todas as parcelas como pagas (ajustando paid_amount)
    for p in cc_data.get('installments', []):
        if not p.get('paid', False):
            p['paid_amount'] = p.get('paid_amount', 0.0)
            faltante = p['amount'] - p['paid_amount']
            if faltante > 0:
                p['paid_amount'] = p['amount']
            p['paid'] = True
            p['moved_to_bill'] = True

    # Zera a fatura atual (já paga)
    cc_data['current_bill'] = 0.0

    registrar_transacao(username, f"Quitar dívida total (desconto {int(QUIT_DISCOUNT*100)}%)", total_com_desconto)
    salvar_usuarios(usuarios)
    print(f"\nDívida quitada com sucesso por {formatar_moeda(total_com_desconto)}. Desconto aplicado: {formatar_moeda(desconto)}")
    return True

def gerenciar_cartao_credito(username, usuarios):
    """
    Interface completa para gerenciamento do cartão de crédito
    Inclui visualização, pagamentos, compras e sistema de parcelas
    """
    user_data = usuarios[username]
    cc_data = user_data['credit_card']

    # Processa ciclo mensal do cartão - move parcelas vencidas para a fatura
    roll_over_installments(cc_data)
    salvar_usuarios(usuarios)

    # Sistema de aumento automático de limite baseado em atividade
    old_limit = cc_data.get('limit', 0.0)
    activity_increase = 0.0

    # Verifica atividade de depósitos (a cada R$100 = +R$10 de limite)
    deposit_activity = user_data.get('last_activity_deposit', 0)
    transfer_activity = user_data.get('last_activity_transfer', 0)

    if deposit_activity >= 100:
        increase_amount = (deposit_activity // 100) * 10
        activity_increase += increase_amount
        user_data['last_activity_deposit'] %= 100  # Mantém o resto

    # Verifica atividade de transferências (a cada R$100 = +R$10 de limite)
    if transfer_activity >= 100:
        increase_amount = (transfer_activity // 100) * 10
        activity_increase += increase_amount
        user_data['last_activity_transfer'] %= 100  # Mantém o resto

    # Aplica aumento de limite se houver
    if activity_increase > 0:
        cc_data['limit'] += activity_increase
        print(f"\n🎉 Seu limite de crédito foi aumentado de {formatar_moeda(old_limit)} para {formatar_moeda(cc_data['limit'])} devido à sua movimentação na conta!")
        salvar_usuarios(usuarios)

    # Menu principal do cartão de crédito
    while True:
        # Antes de mostrar, garante que parcelas vencidas sejam lançadas
        roll_over_installments(cc_data)
        salvar_usuarios(usuarios)

        limite_disponivel = calcular_limite_disponivel(cc_data)
        is_negativado = verificar_negativacao(cc_data)

        print("\n==================== CARTÃO DE CRÉDITO ====================")
        print("1 - Ver detalhes do cartão")
        print("2 - Ver e pagar fatura")
        print("3 - Fazer compra com cartão")
        print("4 - Quitar dívida total com desconto")
        print("5 - Voltar ao menu principal")
        print("===========================================================")
        opcao_cc = input("Escolha uma opção: ")

        if opcao_cc == '1':
            # Exibe informações detalhadas do cartão
            print("\n===== DETALHES DO CARTÃO =====")
            print(f"  Número: {cc_data['number']}")
            print(f"  CVV: {cc_data['cvv']}")
            print(f"  Vencimento: {cc_data['expiry_date']}")
            print(f"  Limite Total: {formatar_moeda(cc_data['limit'])}")
            print(f"  Fatura Atual: {formatar_moeda(cc_data['current_bill'])}")
            print(f"  Limite Disponível: {formatar_moeda(limite_disponivel)}")

            if is_negativado:
                print(f"  ⚠️ STATUS: CARTÃO NEGATIVADO!")
                print(f"  ⚠️ Juros de atraso serão MAJORADOS!")
            else:
                print(f"  ✅ STATUS: NORMAL")

            # Lista parcelas (com status)
            if cc_data.get('installments'):
                print("\n--- Parcelas (todas) ---")
                for p in cc_data['installments']:
                    status = "Pago" if p.get('paid', False) else ("Na fatura" if p.get('moved_to_bill', False) else "Futura")
                    paid_amt = p.get('paid_amount', 0.0)
                    print(f"  {p['installment_number']}/{p['total_installments']} - {formatar_moeda(p['amount'])} - Venc: {p['due_date']} - {status} (Pago: {formatar_moeda(paid_amt)})")
            else:
                print("  Nenhuma parcela registrada.")

            print("================================")

        elif opcao_cc == '2':
            # Interface de visualização e pagamento de fatura
            print("\n===== FATURA DO CARTÃO =====")
            print(f"  Fatura Atual: {formatar_moeda(cc_data.get('current_bill', 0.0))}")

            if is_negativado:
                print(f"  ⚠️ CARTÃO NEGATIVADO - Juros de atraso majorados!")

            # Mostra parcelas futuras e as que já estão na fatura
            if cc_data.get('installments'):
                print("\n--- Parcelas ---")
                for i, p in enumerate(cc_data['installments']):
                    status = "Pago" if p.get('paid', False) else ("Na fatura" if p.get('moved_to_bill', False) else "Futura")
                    paid_amt = p.get('paid_amount', 0.0)
                    print(f"  {p['installment_number']}/{p['total_installments']}: {formatar_moeda(p['amount'])} - {status} - Venc: {p['due_date']} - Pago: {formatar_moeda(paid_amt)}")
                print("-----------------------")
            else:
                print("  Nenhuma parcela registrada.")

            # Opções de pagamento se há fatura pendente
            if cc_data.get('current_bill', 0.0) > 0:
                print("\n--- Opções de Pagamento ---")
                print("1 - Pagar fatura total")
                print("2 - Pagar um valor específico")
                print("---------------------------")
                opcao_pagamento = input("Escolha uma opção de pagamento: ").strip()

                valor_a_pagar = 0.0

                if opcao_pagamento == '1':
                    # Pagamento total da fatura (apenas o que está na fatura atual)
                    valor_a_pagar = round(cc_data.get('current_bill', 0.0), 2)
                elif opcao_pagamento == '2':
                    # Pagamento parcial
                    try:
                        valor_a_pagar = float(input(f"Quanto deseja pagar? (Fatura atual: {formatar_moeda(cc_data.get('current_bill',0.0))}): "))
                        if valor_a_pagar <= 0:
                            print("Valor de pagamento inválido.")
                            continue
                        if valor_a_pagar > cc_data.get('current_bill', 0.0):
                            print("Você não pode pagar mais do que o valor da fatura atual.")
                            continue
                    except ValueError:
                        print("Entrada inválida. Digite um número.")
                        continue
                else:
                    print("Opção de pagamento inválida.")
                    continue

                # Processa o pagamento usando função que aloca o valor entre parcelas na fatura
                pagar_fatura_e_alocar_a_parcelas(username, user_data, cc_data, valor_a_pagar)

                # Se quitou completamente, atualiza data da última fatura
                if cc_data.get('current_bill', 0.0) <= 0:
                    cc_data['current_bill'] = 0.0
                    cc_data['last_bill_date'] = datetime.now().strftime("%Y-%m-%d")
                    print("Fatura atual quitada!")

                salvar_usuarios(usuarios)
            else:
                print("Não há fatura pendente.")
            print("==============================")

        elif opcao_cc == '3':
            # Interface para fazer compras com o cartão
            try:
                # Recalcula limite disponível atual
                limite_disponivel_atual = calcular_limite_disponivel(cc_data)

                print(f"\nLimite total: {formatar_moeda(cc_data['limit'])}")
                print(f"Fatura atual: {formatar_moeda(cc_data.get('current_bill',0.0))}")
                print(f"Limite disponível: {formatar_moeda(limite_disponivel_atual)}")

                if is_negativado:
                    print("⚠️ ATENÇÃO: Cartão está negativado!")

                valor_compra = float(input(f"\nQual o valor da compra? "))

                # Validações da compra
                if valor_compra <= 0:
                    print("Valor de compra inválido.")
                    continue

                # Verifica se a compra pode ser aprovada (baseado no valor original, sem juros)
                if valor_compra > limite_disponivel_atual:
                    print("❌ Compra negada! Valor da compra excede o limite disponível.")
                    print(f"Limite disponível: {formatar_moeda(limite_disponivel_atual)}")
                    continue

                # Escolha do número de parcelas
                parcelas = int(input("Em quantas parcelas deseja pagar? (1 para à vista): "))
                if parcelas <= 0:
                    print("Número de parcelas inválido.")
                    continue

                # Calcula juros e valor das parcelas
                juros_compra = calcular_juros_parcela(valor_compra, parcelas)
                valor_total_com_juros = round(valor_compra + juros_compra, 2)
                valor_parcela = round(valor_total_com_juros / parcelas, 2)

                # IMPORTANTE: Verifica se após os juros, a primeira parcela pode ser adicionada
                # Aqui consideramos que a primeira parcela será lançada imediatamente na fatura (due_date = hoje)
                if (cc_data.get('current_bill', 0.0) + valor_parcela) > cc_data['limit']:
                    print(f"⚠️ ATENÇÃO: A primeira parcela ({formatar_moeda(valor_parcela)}) fará com que você ultrapasse o limite total.")
                    print(f"Isso resultará em NEGATIVAÇÃO do cartão com juros majorados!")
                    confirmar = input("Deseja continuar mesmo assim? (s/n): ").strip().lower()
                    if confirmar != 's':
                        print("Compra cancelada.")
                        continue

                # Cria as parcelas com due_date mensal
                parcelas_criadas = []
                hoje = datetime.now().date()
                for i in range(parcelas):
                    # Definimos due_date: i==0 -> hoje (aparece na fatura imediatamente), i==1 -> hoje+30 dias, etc.
                    due_date = (hoje + timedelta(days=30 * i)).strftime("%Y-%m-%d")
                    parcela_obj = {
                        'amount': float(valor_parcela),
                        'due_date': due_date,
                        'paid_amount': 0.0,
                        'paid': False,
                        'moved_to_bill': False,  # será True quando due_date <= hoje e for movida para fatura
                        'installment_number': i + 1,
                        'total_installments': parcelas,
                        'original_amount': round(valor_compra,2)
                    }
                    # Se i == 0, movemos imediatamente para a fatura
                    if i == 0:
                        parcela_obj['moved_to_bill'] = True
                        cc_data['current_bill'] = round(cc_data.get('current_bill', 0.0) + parcela_obj['amount'], 2)
                    parcelas_criadas.append(parcela_obj)

                # Adiciona parcelas ao cartão
                cc_data.setdefault('installments', [])
                cc_data['installments'].extend(parcelas_criadas)

                # Verifica se ficou negativado após a compra
                if verificar_negativacao(cc_data):
                    print(f"\n⚠️ CARTÃO NEGATIVADO APÓS A COMPRA!")
                    print(f"⚠️ Juros de atraso serão MAJORADOS em futuras faturas!")

                # Confirma a compra
                print(f"\n✅ Compra de {formatar_moeda(valor_compra)} aprovada em {parcelas}x.")
                if juros_compra > 0:
                    print(f"Juros aplicados: {formatar_moeda(juros_compra)}. Valor total da compra: {formatar_moeda(valor_total_com_juros)}")
                print(f"Valor da parcela: {formatar_moeda(valor_parcela)}")
                print(f"Fatura atualizada: {formatar_moeda(cc_data.get('current_bill',0.0))}")
                print(f"Novo limite disponível: {formatar_moeda(calcular_limite_disponivel(cc_data))}")

                # Registra a transação
                registrar_transacao(username, f"Compra Cartão ({parcelas}x)", valor_compra)
                salvar_usuarios(usuarios)

            except ValueError:
                print("Entrada inválida. Digite um número para o valor ou parcelas.")

        elif opcao_cc == '4':
            # Quitar dívida total com desconto
            quitar_divida_total(username, user_data, cc_data)

        elif opcao_cc == '5':
            # Volta ao menu principal
            print("\nVoltando ao menu principal.")
            break

        else:
            print("\nOpção inválida. Tente novamente.")

# --- FLUXO PRINCIPAL DO PROGRAMA ---

# Cabeçalho do sistema
print("=============================================== SEU BANCO ===============================================")

# Carrega dados dos usuários existentes
usuarios = carregar_usuarios()

# Loop principal de autenticação
while True:
    initial_choice = input("\nVocê já tem conta? (s/n) ou 'admin' para login administrativo: ").strip().lower()

    if initial_choice == 'admin':
        # Login administrativo
        admin_user = input("Usuário Admin: ").strip()
        admin_pass = input("Senha Admin: ").strip()

        if admin_user == ADMIN_USERNAME and admin_pass == ADMIN_PASSWORD:
            print("\nLogin de administrador bem-sucedido!")
            # Entra no painel administrativo
            if admin_panel(usuarios):
                # Se o banco foi resetado, recarrega e encerra
                usuarios = carregar_usuarios()
                print("Banco de dados resetado. O programa será encerrado.")
                exit()
        else:
            print("\nCredenciais de administrador inválidas.")

    elif initial_choice in ['s', 'n']:
        # Opção válida de usuário comum
        tem_conta = initial_choice
        break
    else:
        print("Opção inválida. Tente novamente.")

# Fluxo para usuários existentes
if tem_conta == 's':
    # Login de usuário existente
    username = input("Nome de usuário: ").strip()

    if username not in usuarios:
        print("\nUsuário não encontrado.")
        exit()

    senha = input("Senha: ").strip()

    if usuarios[username]['senha'] == senha:
        # Login bem-sucedido
        print(f"\nBem-vindo de volta, {username}!")
        total = usuarios[username].get('saldo', 0.0)
    else:
        # Senha incorreta - opção de recuperação
        recuperar = input("\nSenha incorreta. Deseja tentar recuperar sua senha? (s/n): ").strip().lower()

        if recuperar == 's':
            # Processo de recuperação de senha
            pergunta = usuarios[username].get('pergunta')
            resposta_correta = usuarios[username].get('resposta')

            if pergunta and resposta_correta:
                resposta_usuario = input(f"{pergunta} ").strip().lower()

                if resposta_usuario == resposta_correta.lower():
                    # Resposta correta - permite redefinir senha
                    nova_senha = input("Digite a nova senha: ").strip()
                    usuarios[username]['senha'] = nova_senha
                    salvar_usuarios(usuarios)
                    print("\nSenha redefinida com sucesso!")
                    total = usuarios[username].get('saldo', 0.0)
                else:
                    print("\nResposta incorreta. Encerrando o programa.")
                    exit()
            else:
                print("\nConta não tem pergunta secreta cadastrada ou resposta. Encerrando.")
                exit()
        else:
            print("\nEncerrando o programa.")
            exit()

else:
    # Criação de nova conta
    username = input("Crie seu nome de usuário: ").strip()

    if username in usuarios:
        print("\nEsse usuário já existe. Tente outro.")
        exit()

    senha = input("Crie sua senha: ").strip()

    # Sistema de pergunta secreta
    pergunta_secreta_gerada = gerar_pergunta_secreta_aleatoria()
    print(f"\nSua pergunta secreta gerada aleatoriamente é: '{pergunta_secreta_gerada}'")
    trocar_pergunta = input("Deseja trocar a pergunta secreta? (s/n): ").strip().lower()

    if trocar_pergunta == 's':
        # Permite escolher pergunta da lista
        print("\nEscolha uma nova pergunta secreta da lista:")
        for i, q in enumerate(SECRET_QUESTIONS):
            print(f"{i+1} - {q}")

        while True:
            try:
                escolha = int(input("Digite o número da pergunta desejada: "))
                if 1 <= escolha <= len(SECRET_QUESTIONS):
                    pergunta = SECRET_QUESTIONS[escolha - 1]
                    break
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
    else:
        # Usa a pergunta gerada aleatoriamente
        pergunta = pergunta_secreta_gerada

    # Coleta resposta para a pergunta secreta
    resposta = input(f"Resposta para a pergunta '{pergunta}': ").strip()

    # Gera dados do cartão de crédito
    cc_number = gerar_numero_cartao()
    cc_cvv = gerar_cvv()
    cc_expiry = gerar_data_vencimento()
    cc_limit = gerar_limite_inicial()

    # Cria registro do novo usuário
    usuarios[username] = {
        "senha": senha,
        "saldo": 0.0,
        "pergunta": pergunta,
        "resposta": resposta,
        "credit_card": {
            "number": cc_number,
            "cvv": cc_cvv,
            "expiry_date": cc_expiry,
            "limit": cc_limit,
            "current_bill": 0.0,
            "last_bill_date": datetime.now().strftime("%Y-%m-%d"),
            "installments": []
        },
        "last_activity_deposit": 0.0,
        "last_activity_transfer": 0.0,
        "historico": []
    }

    # Salva novo usuário
    salvar_usuarios(usuarios)
    print("\nConta criada com sucesso!")
    total = 0.0

    # Oferece depósito inicial
    deseja_depositar = input("Deseja realizar um depósito inicial? (s/n): ").strip().lower()

    if deseja_depositar == 's':
        print("\nVamos realizar o depósito com notas:")
        try:
            # Coleta quantidade de cada nota
            N_200 = int(input("Notas de R$200,00: "))
            N_100 = int(input("Notas de R$100,00: "))
            N_50 = int(input("Notas de R$50,00: "))
            N_20 = int(input("Notas de R$20,00: "))
            N_10 = int(input("Notas de R$10,00: "))
            N_5 = int(input("Notas de R$5,00: "))
            N_2 = int(input("Notas de R$2,00: "))

            # Calcula valor total do depósito
            deposito_inicial = (N_200 * 200 + N_100 * 100 + N_50 * 50 +
                                N_20 * 20 + N_10 * 10 + N_5 * 5 + N_2 * 2)

            if deposito_inicial > 0:
                # Processa depósito inicial
                total += deposito_inicial
                usuarios[username]['saldo'] = total
                usuarios[username]['last_activity_deposit'] += deposito_inicial
                salvar_usuarios(usuarios)
                registrar_transacao(username, "Depósito inicial", deposito_inicial)
                print(f"\nDepósito realizado. Saldo atual: {formatar_moeda(total)}")
            else:
                print("Valor de depósito inicial inválido.")
        except ValueError:
            print("Entrada inválida para notas. Depósito inicial cancelado.")

# --- MENU PRINCIPAL DO SISTEMA ---

while True:
    print("\n==================== MENU PRINCIPAL ====================")
    print("1 - Consultar saldo")
    print("2 - Saques")
    print("3 - Transferências")
    print("4 - Depósitos")
    print("5 - Ver histórico de transações")
    print("6 - Cartão de Crédito")
    print("7 - Exportar Histórico")
    print("8 - Sair")
    print("========================================================")
    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        # Consulta de saldo
        print(f"\nSaldo atual: {formatar_moeda(total)}")

    elif opcao == '2':
        # Operação de saque
        try:
            valor_saque = float(input(f"\nQual valor deseja sacar? Saldo: {formatar_moeda(total)}: "))

            if valor_saque <= 0:
                print("Valor de saque inválido.")
            elif valor_saque <= total:
                # Processa saque
                total -= valor_saque
                usuarios[username]['saldo'] = total  # Mantém saldo do usuário sincronizado imediatamente
                print(f"\nSaque realizado no valor de {formatar_moeda(valor_saque)}! Novo saldo: {formatar_moeda(total)}")
                registrar_transacao(username, "Saque", valor_saque)
                salvar_usuarios(usuarios)
            else:
                print("\nSaldo insuficiente para saque.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    elif opcao == '3':
        # Operação de transferência
        destinatario = input("\nDigite o nome do usuário para quem deseja transferir: ").strip()

        if destinatario == username:
            print("\nVocê não pode transferir para si mesmo.")
        elif destinatario not in usuarios:
            print("\nUsuário destinatário não encontrado.")
        else:
            try:
                valor = float(input("Digite o valor a ser transferido: "))

                if valor <= 0:
                    print("\nValor inválido.")
                elif valor > total:
                    print("\nSaldo insuficiente para a transferência.")
                else:
                    # Processa transferência
                    total -= valor
                    usuarios[username]['saldo'] = total  # Sincroniza de imediato
                    usuarios[destinatario]['saldo'] += valor
                    usuarios[destinatario]['last_activity_transfer'] += valor

                    print(f"\nTransferência de {formatar_moeda(valor)} realizada para {destinatario}.")
                    print(f"Seu novo saldo: {formatar_moeda(total)}")

                    # Registra transação para ambos os usuários
                    registrar_transacao(username, f"Transferência para {destinatario}", valor)
                    registrar_transacao(destinatario, f"Recebido de {username}", valor)
                    salvar_usuarios(usuarios)
            except ValueError:
                print("Entrada inválida. Digite um número.")

    elif opcao == '4':
        # Operação de depósito
        print("\nDepósito com notas:")
        try:
            # Coleta quantidade de cada nota
            N_200 = int(input("Notas de R$200,00: "))
            N_100 = int(input("Notas de R$100,00: "))
            N_50 = int(input("Notas de R$50,00: "))
            N_20 = int(input("Notas de R$20,00: "))
            N_10 = int(input("Notas de R$10,00: "))
            N_5 = int(input("Notas de R$5,00: "))
            N_2 = int(input("Notas de R$2,00: "))

            # Calcula valor total do depósito
            deposito = (N_200 * 200 + N_100 * 100 + N_50 * 50 +
                        N_20 * 20 + N_10 * 10 + N_5 * 5 + N_2 * 2)

            if deposito <= 0:
                print("Valor de depósito inválido.")
            else:
                # Processa depósito
                total += deposito
                usuarios[username]['saldo'] = total  # Sincroniza de imediato
                usuarios[username]['last_activity_deposit'] += deposito
                print(f"\nDepósito de {formatar_moeda(deposito)} realizado. Novo saldo: {formatar_moeda(total)}")
                registrar_transacao(username, "Depósito", deposito)
                salvar_usuarios(usuarios)
        except ValueError:
            print("Entrada inválida para notas. Depósito cancelado.")

    elif opcao == '5':
        # Visualização do histórico de transações
        historico_path = f"{username}_historico.txt"

        if os.path.exists(historico_path):
            print("\n===== HISTÓRICO DE TRANSAÇÕES =====")
            with open(historico_path, "r") as f:
                print(f.read())
            print("====================================")
        else:
            print("\nNenhuma transação registrada ainda.")

    elif opcao == '6':
        # Acesso ao cartão de crédito
        if 'credit_card' not in usuarios[username]:
            # Gera cartão se não existir (para contas antigas)
            print("\nSeu cartão de crédito está sendo gerado. Por favor, tente novamente em breve.")
            usuarios[username]['credit_card'] = {
                'number': gerar_numero_cartao(),
                'cvv': gerar_cvv(),
                'expiry_date': gerar_data_vencimento(),
                'limit': gerar_limite_inicial(),
                'current_bill': 0.0,
                'last_bill_date': datetime.now().strftime("%Y-%m-%d"),
                'installments': []
            }
            salvar_usuarios(usuarios)

        # Acessa interface do cartão de crédito
        gerenciar_cartao_credito(username, usuarios)

    elif opcao == '7':
        # Exportação de histórico para CSV
        print("\n===== EXPORTAR HISTÓRICO =====")
        print("1 - Último 1 mês")
        print("2 - Últimos 5 meses")
        print("3 - Desde uma data específica")
        print("4 - Todas as informações")
        print("================================")

        periodo_exportacao = input("Escolha o período para exportar: ").strip()

        if periodo_exportacao in ['1', '2', '3', '4']:
            exportar_historico_csv(username, periodo_exportacao)
        else:
            print("Opção de período inválida.")

    elif opcao == '8':
        # Encerramento do programa
        print(f"\nSaindo... Obrigado por utilizar nossos serviços, {username}!")
        break

    else:
        print("\nOpção inválida. Tente novamente.")

    # >>> SINCRONIZAÇÃO DE SALDO NO FINAL DO LOOP <<<
    if username in usuarios:
        total = usuarios[username]['saldo']
        salvar_usuarios(usuarios)
