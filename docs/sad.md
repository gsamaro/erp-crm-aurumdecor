# Documento de Arquitetura de Software (SAD)

## 1. Objetivo
Descrever como o sistema sera construido, incluindo estrutura tecnica, comunicacao entre componentes, padroes, decisoes arquiteturais e requisitos nao funcionais.

## 2. Visao Geral da Arquitetura
```
[Streamlit UI]
      |
      v
[FastAPI - API Layer (Render)]
      |
      v
[Service Layer]
      |
      v
[Repository Layer]
      |
      v
[PostgreSQL (Supabase)]

[Integration Layer] <-> WhatsApp API
```

## 3. Principios e Camadas
Principios:
- Clean Architecture e SOLID
- Separacao de responsabilidades por camadas
- Baixo acoplamento e alta coesao
- Testes automatizados (unitarios e integrados) desde o inicio
- Observabilidade (logs e rastreabilidade)

Camadas:
1. Presentation Layer (Streamlit)
2. API Layer (FastAPI)
3. Service Layer (regras de negocio)
4. Repository Layer (persistencia)
5. Domain Layer (entidades e modelos)
6. Integration Layer (WhatsApp API)

## 4. Componentes e Responsabilidades
- Presentation (Streamlit): interface administrativa por modulos.
- API (FastAPI): rotas por modulo, validacao, versionamento e autenticacao.
- Service Layer: orquestra regras de negocio, amortizacao, custos e lucro.
- Repository Layer: CRUD desacoplado, transacoes e consultas.
- Domain: entidades e regras isoladas e testaveis.
- Integration: webhook e envio de mensagens, orcamento e lembretes.
- Observabilidade: logs e reprocessamento de integracoes.

## 5. Comunicacao entre Componentes
- Streamlit consome a API via HTTP.
- API chama servicos de dominio e repositorios.
- Webhook do WhatsApp entra pela API e aciona servicos.

## 6. Padroes e Decisoes Arquiteturais
- Backend em Python com FastAPI.
- Interface administrativa em Streamlit.
- Banco de dados relacional PostgreSQL no Supabase.
- Backend hospedado no Render.
- Streamlit nao acessa o banco diretamente; todo acesso passa pela API.
- DTOs/Schemas para validacao.
- Repository Pattern e Service Layer.
- Dependency Injection.
- Migrations com ferramenta dedicada (Alembic).

## 7. Requisitos Nao Funcionais
- Manutenibilidade: codigo modular e testavel.
- Observabilidade: logs por modulo e integracao.
- Seguranca: autenticacao e controle de acesso.
- Performance: consultas otimizadas por modulo.

## 8. Seguranca
- Autenticacao inicial por usuario admin.
- Senhas com hash seguro (ex.: bcrypt/argon2).
- Secrets em variaveis de ambiente.
- Protecao de endpoints e rate limit para webhook.
- Registro de logs de acesso e erros.

## 9. Dados e Persistencia (resumo)
- Tabelas principais: users, clients, products, product_amortization, inventory, events,
  event_products, budgets, budget_products, accounts_payable, accounts_receivable,
  cash_flow, conversations, messages, logs.
- Chaves primarias UUID e migrations controladas com Alembic.
- Acesso ao banco somente via API (Streamlit nao conecta direto).
- Regras de consistencia:
  - Evento consome produtos e registra amortizacao.
  - Orcamento aprovado gera evento.
  - Contas a pagar/receber impactam fluxo de caixa.

## 10. Integracoes
WhatsApp API:
- Webhook para receber mensagens.
- Endpoint dedicado para validacao e assinatura.
- Processamento assincrono (fila futura).

Fluxo basico:
1. Mensagem recebida via webhook.
2. Registro no banco.
3. Vinculo ao cliente.
4. Resposta ou acao no CRM.

## 11. Estrategia de Deploy
### Ambientes
- Dev: ambiente local.
- Producao: ambiente principal.

### Containerizacao
- Docker para API e jobs auxiliares.
- Streamlit em container separado.

### Hospedagem (sugestao simples)
- API: Render.
- Streamlit: Streamlit Cloud.
- Banco: PostgreSQL no Supabase.

### CI/CD
- Lint + type checking.
- Testes unitarios e integrados.
- Build de imagem.
- Deploy por ambiente.

### Monitoramento e Logs
- Logs centralizados por ambiente.
- Alertas basicos para falhas de integracao.

## 12. Estrategia de Testes
- Testes unitarios por camada (servicos, dominio, repositorios).
- Testes de integracao cobrindo fluxos principais (evento -> amortizacao -> financeiro).
- Testes executados junto com cada entrega funcional.
- Padroes: Arrange-Act-Assert, fixtures reutilizaveis, seeds para banco em integracao.

## 13. Estrutura de Pastas (sugestao)
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

## 14. Fluxos do Sistema (alto nivel)
### Fluxo completo de dados (exemplo: criar cliente)
1. Usuario preenche dados do cliente no Streamlit.
2. Streamlit chama a API (Render) com os dados do formulario.
3. API valida o schema e autentica o usuario.
4. Service Layer aplica regras de negocio (ex.: status, campos obrigatorios).
5. Repository grava no PostgreSQL (Supabase).
6. Banco confirma a operacao e retorna o registro criado.
7. API responde com o cliente persistido.
8. Streamlit atualiza a tela e confirma a criacao.

### Fluxo de Evento
1. Usuario cria evento no Streamlit (cliente, data, produtos, quantidades).
2. Streamlit envia os dados para a API.
3. API valida e carrega dados de produtos e cliente.
4. Service Layer calcula amortizacao por produto e custo total do evento.
5. Repository registra evento e itens no PostgreSQL.
6. Service Layer gera contas a receber e lucro do evento.
7. API retorna evento consolidado.
8. Streamlit exibe custos, lucro e resumo do evento.

### Fluxo de Orcamento
1. Usuario cria orcamento e adiciona produtos no Streamlit.
2. Streamlit envia o orcamento para a API.
3. API valida dados e calcula custos, margem e preco sugerido.
4. Repository salva orcamento e itens no PostgreSQL.
5. API retorna orcamento com status inicial (em elaboracao/enviado).
6. Quando aprovado, Streamlit chama a API para conversao.
7. Service Layer converte orcamento em evento e gera contas a receber.
8. API retorna evento gerado e atualiza o status do orcamento.

### Fluxo de WhatsApp
1. Mensagem recebida via webhook do WhatsApp.
2. API (Render) valida assinatura e registra payload.
3. Service Layer identifica ou cria cliente pela origem.
4. Repository grava conversa e mensagem no PostgreSQL.
5. API dispara resposta automatica (se configurado).
6. Streamlit mostra o historico atualizado na interface do CRM.

## 15. Restricoes
- Dashboard avancado fica para fase futura.
- Integracao WhatsApp e assincrona via webhook.
