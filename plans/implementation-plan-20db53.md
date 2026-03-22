# Plano de Implementação — ERP + CRM + WhatsApp

Plano incremental de implementação do sistema ERP + CRM + WhatsApp com PostgreSQL (Supabase), FastAPI (Render), Streamlit e Alembic, seguindo Clean Architecture e testes desde o início.

---

## Fase 0: Setup Inicial do Projeto
**Objetivo:** Estrutura base, ambiente e ferramentas.

### 0.1 Estrutura de Pastas
- Criar estrutura conforme SAD:
  ```
  /app
    /api
    /services
    /repositories
    /domain
    /schemas
    /integrations
    /config
    /tests
      /unit
      /integration
  /streamlit
    /pages
    /components
  /migrations
  ```
- Criar arquivos de configuração: `.env.example`, `requirements.txt`, `Dockerfile`, `.gitignore`, `README.md`.

### 0.2 Dependências Iniciais
- FastAPI, Uvicorn, Pydantic
- SQLAlchemy, Alembic, psycopg2-binary
- Pytest, pytest-asyncio
- python-dotenv
- Streamlit
- httpx (para client HTTP no Streamlit)

### 0.3 Configuração de Banco (Supabase)
- Criar projeto no Supabase.
- Obter connection string PostgreSQL.
- Configurar variáveis de ambiente.

### 0.4 Setup Alembic
- Inicializar Alembic.
- Configurar `alembic.ini` e `env.py` para PostgreSQL (Supabase).
- Criar primeira migration (tabelas base).

### 0.5 Setup CI/CD Básico
- Configurar lint (ruff/flake8) e type checking (mypy).
- Configurar pytest para rodar testes unitários e integrados.
- Criar workflow básico (GitHub Actions ou similar).

**Entregável:** Projeto estruturado, banco conectado, Alembic configurado, CI básico rodando.

---

## Fase 1: Autenticação e Usuários
**Objetivo:** Sistema de autenticação Admin e base de usuários.

### 1.1 Modelo de Dados
- Migration: tabela `users` (id, name, email, password_hash, role, active, created_at, updated_at).

### 1.2 Domain Layer
- Entidade `User` com validações básicas.

### 1.3 Repository Layer
- `UserRepository`: CRUD básico (create, get_by_id, get_by_email, list, update).

### 1.4 Service Layer
- `AuthService`: registro, login, hash de senha (bcrypt/argon2), geração de token (JWT).
- `UserService`: gerenciamento de usuários.

### 1.5 API Layer
- Endpoints: `POST /auth/register`, `POST /auth/login`, `GET /users/me`.
- Middleware de autenticação JWT.

### 1.6 Testes
- Unitários: `AuthService`, `UserRepository`.
- Integração: fluxo completo de registro e login.

### 1.7 Streamlit (Admin)
- Página de login.
- Página de gerenciamento de usuários (listar, criar).

**Entregável:** Autenticação funcional, usuários gerenciáveis, testes passando.

---

## Fase 2: CRM — Clientes
**Objetivo:** Cadastro e gestão de clientes.

### 2.1 Modelo de Dados
- Migration: tabela `clients` (id, name, phone, email, status, notes, created_at, updated_at).

### 2.2 Domain Layer
- Entidade `Client` com validações.

### 2.3 Repository Layer
- `ClientRepository`: CRUD completo.

### 2.4 Service Layer
- `ClientService`: criar, atualizar, listar, buscar por ID.

### 2.5 API Layer
- Endpoints: `POST /clients`, `GET /clients`, `GET /clients/{id}`, `PUT /clients/{id}`.

### 2.6 Testes
- Unitários: `ClientService`, `ClientRepository`.
- Integração: fluxo completo de CRUD de clientes.

### 2.7 Streamlit
- Página de clientes: listar, criar, editar.

**Entregável:** CRM básico funcional com clientes, testes passando.

---

## Fase 3: Produtos e Amortização
**Objetivo:** Cadastro de produtos com cálculo de amortização.

### 3.1 Modelo de Dados
- Migration: tabelas `products`, `product_amortization`, `inventory`.

### 3.2 Domain Layer
- Entidade `Product` com lógica de amortização.
- Entidade `ProductAmortization`.
- Entidade `Inventory`.

### 3.3 Repository Layer
- `ProductRepository`, `ProductAmortizationRepository`, `InventoryRepository`.

### 3.4 Service Layer
- `ProductService`: CRUD, cálculo de amortização por evento/tempo.
- `InventoryService`: movimentação de estoque.

### 3.5 API Layer
- Endpoints: `POST /products`, `GET /products`, `GET /products/{id}`, `PUT /products/{id}`.
- Endpoints: `POST /inventory/movement`.

### 3.6 Testes
- Unitários: lógica de amortização, serviços.
- Integração: criação de produto e movimentação de estoque.

### 3.7 Streamlit
- Página de produtos: listar, criar, editar.
- Página de estoque: visualizar movimentações.

**Entregável:** Produtos com amortização funcional, estoque rastreável, testes passando.

---

## Fase 4: Eventos
**Objetivo:** Registro de eventos com cálculo automático de custos e amortização.

### 4.1 Modelo de Dados
- Migration: tabelas `events`, `event_products`.

### 4.2 Domain Layer
- Entidade `Event`, `EventProduct`.

### 4.3 Repository Layer
- `EventRepository`, `EventProductRepository`.

### 4.4 Service Layer
- `EventService`: criar evento, calcular amortização de produtos, calcular custo total e lucro.

### 4.5 API Layer
- Endpoints: `POST /events`, `GET /events`, `GET /events/{id}`.

### 4.6 Testes
- Unitários: cálculo de amortização e lucro.
- Integração: criação de evento com produtos e validação de custos.

### 4.7 Streamlit
- Página de eventos: listar, criar (selecionar cliente e produtos).
- Exibir custos, lucro e resumo.

**Entregável:** Eventos funcionais com cálculo automático, testes passando.

---

## Fase 5: Orçamentos
**Objetivo:** Criação de orçamentos e conversão em eventos.

### 5.1 Modelo de Dados
- Migration: tabelas `budgets`, `budget_products`.

### 5.2 Domain Layer
- Entidade `Budget`, `BudgetProduct`.

### 5.3 Repository Layer
- `BudgetRepository`, `BudgetProductRepository`.

### 5.4 Service Layer
- `BudgetService`: criar, calcular custos/margem, aprovar, converter em evento.

### 5.5 API Layer
- Endpoints: `POST /budgets`, `GET /budgets`, `GET /budgets/{id}`, `PUT /budgets/{id}/approve`, `POST /budgets/{id}/convert`.

### 5.6 Testes
- Unitários: cálculo de margem, conversão.
- Integração: fluxo completo de orçamento → evento.

### 5.7 Streamlit
- Página de orçamentos: listar, criar, aprovar, converter.

**Entregável:** Orçamentos funcionais com conversão em eventos, testes passando.

---

## Fase 6: Financeiro
**Objetivo:** Contas a pagar/receber e fluxo de caixa.

### 6.1 Modelo de Dados
- Migration: tabelas `accounts_payable`, `accounts_receivable`, `cash_flow`.

### 6.2 Domain Layer
- Entidades `AccountPayable`, `AccountReceivable`, `CashFlow`.

### 6.3 Repository Layer
- `AccountPayableRepository`, `AccountReceivableRepository`, `CashFlowRepository`.

### 6.4 Service Layer
- `FinancialService`: registrar contas, calcular fluxo de caixa, amortização mensal.

### 6.5 API Layer
- Endpoints: `POST /accounts/payable`, `GET /accounts/payable`, `POST /accounts/receivable`, `GET /accounts/receivable`, `GET /cash-flow`.

### 6.6 Testes
- Unitários: cálculo de fluxo de caixa.
- Integração: evento → contas a receber → fluxo de caixa.

### 6.7 Streamlit
- Página financeira: contas a pagar, contas a receber, fluxo de caixa.

**Entregável:** Módulo financeiro funcional, testes passando.

---

## Fase 7: Integração WhatsApp
**Objetivo:** Receber e enviar mensagens via WhatsApp API.

### 7.1 Modelo de Dados
- Migration: tabelas `conversations`, `messages`.

### 7.2 Domain Layer
- Entidades `Conversation`, `Message`.

### 7.3 Repository Layer
- `ConversationRepository`, `MessageRepository`.

### 7.4 Integration Layer
- `WhatsAppWebhook`: receber mensagens, validar assinatura.
- `WhatsAppClient`: enviar mensagens.

### 7.5 Service Layer
- `WhatsAppService`: processar mensagens, vincular a clientes, enviar mensagens/orçamentos.

### 7.6 API Layer
- Endpoints: `POST /webhook/whatsapp`, `POST /whatsapp/send`.

### 7.7 Testes
- Unitários: validação de webhook, envio de mensagens.
- Integração: mensagem recebida → cliente vinculado → gravado.

### 7.8 Streamlit
- Página de conversas: histórico de mensagens por cliente.

**Entregável:** Integração WhatsApp funcional, testes passando.

---

## Fase 8: Relatórios
**Objetivo:** Relatórios financeiros e operacionais.

### 8.1 Service Layer
- `ReportService`: fluxo de caixa, lucro por evento, amortização por período, estoque.

### 8.2 API Layer
- Endpoints: `GET /reports/cash-flow`, `GET /reports/profit-by-event`, `GET /reports/amortization`, `GET /reports/inventory`.

### 8.3 Testes
- Unitários: cálculo de relatórios.
- Integração: dados completos → relatórios corretos.

### 8.4 Streamlit
- Página de relatórios: visualizações e filtros.

**Entregável:** Relatórios funcionais, testes passando.

---

## Fase 9: Logs e Observabilidade
**Objetivo:** Sistema de logs centralizado.

### 9.1 Modelo de Dados
- Migration: tabela `logs`.

### 9.2 Service Layer
- `LogService`: registrar logs por nível e contexto.

### 9.3 API Layer
- Middleware de logging para todas as requisições.

### 9.4 Testes
- Unitários: registro de logs.

### 9.5 Streamlit
- Página de logs: visualizar logs por nível/módulo.

**Entregável:** Sistema de logs funcional.

---

## Fase 10: Deploy e CI/CD
**Objetivo:** Deploy em produção e automação completa.

### 10.1 Containerização
- Dockerfile para API.
- Dockerfile para Streamlit.
- docker-compose para ambiente local.

### 10.2 Deploy
- API no Render.
- Streamlit no Streamlit Cloud.
- Banco no Supabase (já configurado).

### 10.3 CI/CD Completo
- Testes automatizados em PR.
- Deploy automático em merge para main.
- Monitoramento básico.

### 10.4 Documentação Final
- README atualizado com instruções de setup e deploy.
- Documentação de API (Swagger/OpenAPI).

**Entregável:** Sistema em produção, CI/CD completo, documentação atualizada.

---

## Ordem de Implementação (Resumo)
1. **Fase 0:** Setup inicial
2. **Fase 1:** Autenticação e usuários
3. **Fase 2:** CRM — Clientes
4. **Fase 3:** Produtos e amortização
5. **Fase 4:** Eventos
6. **Fase 5:** Orçamentos
7. **Fase 6:** Financeiro
8. **Fase 7:** Integração WhatsApp
9. **Fase 8:** Relatórios
10. **Fase 9:** Logs e observabilidade
11. **Fase 10:** Deploy e CI/CD

---

## Princípios de Implementação
- Testes unitários e integrados em cada fase.
- Commits incrementais por funcionalidade.
- Code review antes de merge.
- Documentação inline (docstrings).
- Migrations versionadas e reversíveis.
- Variáveis de ambiente para secrets.
- Clean Architecture e SOLID em todas as camadas.
