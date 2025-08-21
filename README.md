# 🏦 SOLABANK

Um sistema bancário avançado em **Python** que simula operações financeiras reais de forma interativa, incluindo:

- 👤 **Gerenciamento de Usuários**  
- 💳 **Cartões de Crédito (compras, faturas e PDF)**  
- 📈 **Investimentos (simulação de rendimentos e resgates)**  
- 💵 **Empréstimos (solicitação, juros e pagamentos)**  
- 🔧 **Painel Administrativo (estatísticas e relatórios em CSV/PDF)**  
- 📝 **Auditoria (logs de ações)**  

---

## 🚀 Funcionalidades

### 👥 Usuários
- Cadastro e login com senha e pergunta secreta 🔑  
- Depósitos, saques e transferências 💰  
- Histórico de transações com exportação 📄  

### 💳 Cartões de Crédito
- Solicitar até **5 cartões por usuário**  
- Compras à vista ou parceladas (até 24x com juros progressivos) 🛒  
- Sistema de **pontos de recompensa** ⭐ (troca por saldo)  
- Geração de **faturas em PDF** 🧾  

### 📈 Investimentos
- Opções: **Poupança, CDB, Tesouro Direto, Ações e Bitcoin**  
- Simulação de **rendimentos compostos** 📊  
- Resgates com depósito direto na conta 💸  

### 💵 Empréstimos
- Solicitação baseada no saldo do usuário (até 5x)  
- Juros de **2% ao mês** 📉  
- Pagamento de parcelas ou quitação total ✅  

### 🔧 Administração
- Login administrativo 🔐  
- Estatísticas gerais (saldo total, usuários, transações, etc.)  
- Relatórios exportáveis em **CSV e PDF** 📑  

### 📝 Auditoria
- Registro detalhado de todas as operações  
- Histórico limitado aos últimos **1000 registros**  

---

## 🛠️ Tecnologias Utilizadas
- 🐍 **Python 3.9+**  
- 📂 **JSON** para armazenamento de dados persistentes  
- 📄 **ReportLab** para geração de relatórios em PDF  
- 📊 **CSV** para exportação de planilhas  

---

## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/solabank.git
   cd solabank
Instale as dependências:

bash
Copiar
Editar
pip install reportlab
Execute o sistema:

bash
Copiar
Editar
python main.py

---

🎮 Como Usar
Ao iniciar o sistema, você pode escolher:

Login para acessar sua conta

Cadastrar para criar um novo usuário

Painel Administrativo para acessar estatísticas e relatórios

---

⚖️ Licença
Este projeto foi desenvolvido para fins de estudo e simulação.
Você pode modificá-lo e adaptá-lo conforme necessário.

---

✍️ Autor: Marco Gizoni.
