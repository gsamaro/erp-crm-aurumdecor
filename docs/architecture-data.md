# Arquitetura de Software — Dados e Persistência

## Modelo de Dados (Resumo)
Tabelas principais:
- users
- clients
- products
- product_amortization
- inventory
- events
- event_products
- budgets
- budget_products
- accounts_payable
- accounts_receivable
- cash_flow
- conversations
- messages
- logs

## Decisões de Persistência
- Banco relacional PostgreSQL no Supabase
- Chaves primárias UUID
- Migrations controladas com Alembic
- Acesso ao banco somente via API (Streamlit não conecta direto)
- Auditoria via logs
- Dados sensíveis persistidos como hash (ex.: senha, tokens)
- Consultas com ORM/queries parametrizadas (sem SQL concatenado)

## Regras de Consistência
- Evento consome produtos e registra amortização
- Orçamento aprovado gera evento
- Contas a pagar/receber impactam fluxo de caixa
