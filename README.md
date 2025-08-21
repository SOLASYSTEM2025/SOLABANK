# 🏦 Sistema Bancário em Python

Este é um **sistema bancário completo e robusto** desenvolvido em **Python**, com funcionalidades de **conta corrente**, **operações financeiras** (depósito, saque, transferências), além de um **sistema de cartão de crédito integrado** com parcelamento e cálculo de juros.

O projeto utiliza:
- Um arquivo **JSON (`usuarios.json`)** como banco de dados simples para armazenar informações de usuários e transações.  
- Arquivos de texto **(.txt)** e **.csv** para registrar e exportar históricos de movimentações.

---

## ⚙️ Funcionalidades

### 📌 Conta Corrente
- **Login e Cadastro** de usuários.  
- **Recuperação de Senha** via pergunta secreta.  
- **Consulta de Saldo** em tempo real.  
- **Depósitos** com base em notas reais (R$2, R$5, R$10, R$20, R$50, R$100, R$200).  
- **Saques** com validação de saldo suficiente.  
- **Transferências** entre contas do sistema.  
- **Histórico de Transações** com opção de exportar para `.txt` ou `.csv`.

### 💳 Cartão de Crédito
- **Geração Automática** de cartão para novos usuários (número, CVV e validade únicos).  
- **Limite de Crédito** inicial aleatório, com possibilidade de aumento automático baseado em movimentação.  
- **Compras e Parcelamento** em até 12 vezes (ou mais, com juros).  
- **Cálculo de Juros**:  
  - Juros proporcionais ao número de parcelas.  
  - Juros diários para faturas em atraso.  
  - Juros majorados (3x) em caso de negativação.  
- **Negativação** automática caso o limite seja excedido.  
- **Pagamento de Fatura** (total ou parcial).  
- **Quitação de Dívida** com 10% de desconto (inclui parcelas futuras).

### 🛠️ Administração
- **Painel Administrativo** protegido por senha (`admin_password`).  
- **Visualização Completa** de dados de todos os usuários (saldo, cartão, status, histórico).  
- **Reset do Banco de Dados** (apagar todos os registros e recomeçar do zero).

---

## 📂 Estrutura do Projeto
- `main.py` → Arquivo principal com toda a lógica do sistema.  
- `usuarios.json` → Banco de dados com informações de usuários.  
- `[nome_do_usuario]_historico.txt` → Histórico de transações legível.  
- `[nome_do_usuario]_historico_[periodo].csv` → Histórico exportado em formato CSV.  

---

## 🚀 Tecnologias Utilizadas
- **Linguagem:** Python  
- **Banco de Dados:** JSON  
- **Exportação de dados:** TXT e CSV  

---

[Assista à demonstração no LinkedIn](https://www.linkedin.com/posts/marco-gizoni-811b61300_projeto-solabank-simula%C3%A7%C3%A3o-de-um-caixa-activity-7364128109719166976-06EH?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAAE0OtU0Bv2b9M4stuaQKF1SCE6XUmm9vL4M)

---

✍️ Autor: Marco Gizoni.
