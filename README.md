Este é um sistema bancário completo e robusto desenvolvido em Python, com funcionalidades de conta corrente, operações de depósito e saque, transferências entre usuários, e um sistema de cartão de crédito integrado com parcelamento e cálculo de juros.

O projeto utiliza um arquivo JSON (usuarios.json) como um banco de dados simples para armazenar informações de usuários e transações, e arquivos de texto (.txt e .csv) para registrar e exportar históricos.

Funcionalidades
O sistema oferece uma ampla gama de recursos para o gerenciamento de contas bancárias e de cartão de crédito:

Funcionalidades de Conta Corrente
Login e Cadastro: Os usuários podem criar uma nova conta ou fazer login em uma conta existente.

Segurança: O sistema inclui um recurso de recuperação de senha via pergunta secreta.

Consulta de Saldo: Permite ao usuário verificar o saldo atual da sua conta a qualquer momento.

Depósito: Funcionalidade de depósito com base em notas de dinheiro (R$2, R$5, R$10, R$20, R$50, R$100, R$200).

Saque: Permite realizar saques da conta, com validação de saldo suficiente.

Transferência: Usuários podem transferir fundos para outras contas no sistema.

Histórico de Transações: Visualização e exportação do histórico de todas as transações da conta.

Funcionalidades de Cartão de Crédito
Geração Automática: Um cartão de crédito virtual é gerado automaticamente para cada novo usuário, com número, CVV e data de vencimento únicos.

Limite de Crédito: O limite inicial do cartão é gerado aleatoriamente e pode ser aumentado automaticamente com base na movimentação da conta (depósitos e transferências).

Compras e Parcelamento: Possibilidade de realizar compras com o cartão e parcelar em até 12 vezes (ou mais, com juros).

Cálculo de Juros:

Juros de parcelamento baseados no número de parcelas.

Juros diários para faturas em atraso.

Juros majorados (3x o normal) em caso de negativação.

Negativação: O sistema marca o cartão como "negativado" se a fatura atual exceder o limite de crédito disponível, aplicando juros mais altos.

Pagamento de Fatura: Permite o pagamento total ou parcial da fatura do cartão.

Quitação de Dívida: Oferece a opção de quitar a dívida total (incluindo parcelas futuras) com um desconto de 10%.

Funcionalidades de Administração
Painel Administrativo: Acesso exclusivo para o administrador com senha (admin_password).

Visualização de Dados: O administrador pode ver todos os dados de todos os clientes, incluindo saldo, informações do cartão de crédito, status de negativação e histórico de parcelas.

Reset do Banco de Dados: Funcionalidade para apagar completamente todos os dados de usuários e transações do sistema.

Estrutura do Código
main.py: O arquivo principal que contém toda a lógica do sistema.

usuarios.json: Arquivo JSON que atua como o banco de dados principal, armazenando os dados de cada usuário.

[nome_do_usuario]_historico.txt: Um arquivo de texto para cada usuário, registrando o histórico de transações de forma legível.

[nome_do_usuario]_historico_[periodo].csv: Arquivo CSV gerado ao exportar o histórico de transações, facilitando a análise externa.
