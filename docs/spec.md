# Documentação de Especificação – ERP + CRM + WhatsApp (Versão Simplificada)

## Sistema de Gestão de Eventos, Produtos, Custos, Orçamentos e Financeiro

---

# 1. Visão Geral do Sistema

O sistema será um **ERP + CRM integrado ao WhatsApp**, com interface administrativa em Streamlit e backend em Python.

O sistema deverá gerenciar:

* Clientes (CRM)
* Conversas WhatsApp
* Produtos
* Custos e amortização
* Estoque
* Eventos
* Orçamentos
* Financeiro
* Relatórios

**O módulo de Dashboard não será implementado neste momento**, mas a arquitetura deve permitir inclusão futura.

---

# 2. Arquitetura do Sistema

## Arquitetura geral

```
WhatsApp API
     ↓
Webhook (Backend)
     ↓
Backend (Regras de negócio)
     ↓
Banco de Dados
     ↓
Streamlit (ERP / CRM Interface)
```

## Camadas do sistema

```
Presentation Layer (Streamlit)
API Layer (FastAPI)
Service Layer (Regras de negócio)
Repository Layer (Banco de dados)
Domain Layer (Entidades)
Integration Layer (WhatsApp API)
```

Arquitetura deve seguir:

* SOLID
* Clean Architecture
* Repository Pattern
* Service Layer
* Dependency Injection
* Testes automatizados
* Código desacoplado e extensível

---

# 3. Módulos do Sistema

## Módulos principais

1. CRM / Clientes
2. WhatsApp / Conversas
3. Produtos
4. Custos e Amortização
5. Estoque
6. Eventos
7. Orçamentos
8. Financeiro
9. Relatórios
10. Usuários (apenas admin inicialmente)
11. Logs
12. Configurações

---

# 4. Gestão de Produtos e Custos

## Objetivo

Controlar custo de produtos ao longo do tempo utilizando **amortização por eventos ou por tempo**.

## Funcionalidades

* Cadastro de produtos
* Custo de compra
* Quantidade comprada
* Vida útil (em meses ou eventos)
* Valor total a amortizar
* Valor amortizado
* Valor restante a amortizar
* Custo por evento
* Controle de estoque
* Histórico de utilização do produto em eventos

**Não será implementado agora:**

* Baixa automática de estoque
* Relatório de custo por produto

## Campos da entidade Produto

| Campo             | Descrição                   |
| ----------------- | --------------------------- |
| id                | Identificador               |
| nome              | Nome do produto             |
| custo_compra      | Valor total pago            |
| quantidade        | Quantidade comprada         |
| custo_unitario    | Custo unitário              |
| vida_util_eventos | Vida útil em eventos        |
| vida_util_meses   | Vida útil em meses          |
| valor_amortizar   | Valor total a amortizar     |
| valor_amortizado  | Valor já amortizado         |
| valor_restante    | Valor restante              |
| custo_por_evento  | Custo amortizado por evento |
| estoque_atual     | Quantidade em estoque       |
| data_compra       | Data                        |
| ativo             | Boolean                     |

## Exemplo

Produto: Caixa térmica
Custo: R$ 1.000
Vida útil: 20 eventos
Amortização por evento: R$ 50

---

# 5. Gestão de Eventos

## Objetivo

Registrar eventos e calcular automaticamente o custo dos produtos utilizados.

## Funcionalidades

* Cadastro de evento
* Data
* Cliente
* Produtos utilizados
* Quantidade de cada produto
* Cálculo automático da amortização
* Custo total do evento
* Receita do evento
* Lucro do evento

---

# 6. Orçamentos

## Objetivo

Criar orçamentos para clientes com cálculo automático de custos e margens.

## Funcionalidades

* Criar orçamento
* Selecionar cliente
* Adicionar produtos ao orçamento
* Definir quantidade
* Sistema calcula automaticamente:

  * Custo
  * Preço de venda
  * Lucro
  * Margem
* Status do orçamento:

  * Em elaboração
  * Enviado
  * Aprovado
  * Recusado
  * Cancelado
* Histórico de orçamentos por cliente
* Conversão de orçamento em evento
* Envio de orçamento via WhatsApp

---

# 7. Módulo Financeiro

## Funcionalidades que serão implementadas agora

* Contas a pagar
* Contas a receber
* Fluxo de caixa
* Lucro por evento
* Amortização mensal

**O sistema deve ser projetado para permitir futuramente:**

* DRE
* Centro de custo
* Conciliação bancária
* Categorias financeiras
* Custos fixos
* Custos variáveis
* Indicadores financeiros

## Regras financeiras

* Contas a pagar impactam fluxo de caixa
* Contas a receber impactam fluxo de caixa
* Eventos geram contas a receber
* Compras geram contas a pagar
* Amortização mensal reduz valor contábil dos produtos
* Lucro por evento = Receita - Custos (incluindo amortização do evento)

---

# 8. CRM (Clientes)

## Funcionalidades

* Cadastro de clientes
* Histórico de eventos
* Histórico de orçamentos
* Conversas WhatsApp
* Observações
* Status do cliente (Lead / Cliente)
* Follow-ups
* Histórico de interações

---

# 9. Banco de Dados – Tabelas

## Tabelas principais

```
users
clients
products
product_amortization
inventory
events
event_products
budgets
budget_products
accounts_payable
accounts_receivable
cash_flow
conversations
messages
logs
```

---

# 10. Integração com WhatsApp

## Funcionalidades

* Receber mensagens
* Enviar mensagens
* Enviar orçamento
* Enviar lembrete de pagamento
* Conversas vinculadas ao cliente
* Histórico de mensagens
* Automação futura

---

# 11. Regras de Negócio Importantes

## Amortização

* Produto deve amortizar por evento ou por tempo
* Cada uso reduz o valor restante
* Quando valor restante = 0 → produto totalmente amortizado
* Amortização entra como custo do evento
* Amortização mensal deve ser registrada
* Amortização **não entra em DRE** (módulo não implementado)

## Financeiro

* Contas a pagar impactam fluxo de caixa
* Contas a receber impactam fluxo de caixa
* Eventos geram receita
* Compras geram despesas
* Fluxo de caixa deve considerar:

  * Pagamentos
  * Recebimentos
  * Saldo
  * Projeções

---

# 12. Relatórios Necessários

## Relatórios que serão implementados

* Fluxo de caixa
* Lucro por evento
* Lucro por produto
* Amortização por período
* Estoque
* Contas a pagar
* Contas a receber
* Receita mensal
* Custo mensal

Arquitetura deve permitir inclusão futura de novos relatórios.

---

# 13. Perfis de Usuário

Inicialmente o sistema terá apenas:

| Perfil | Permissões              |
| ------ | ----------------------- |
| Admin  | Acesso total ao sistema |

A arquitetura deve permitir futuramente:

* Financeiro
* Comercial
* Operacional
* Atendimento

---

# 14. Roadmap de Desenvolvimento

Os testes unitários e de integração devem ser implementados junto com cada fase da implementação, garantindo que o que foi entregue funcione como esperado.

## Fase 1

* Estrutura do projeto
* Banco de dados
* Produtos
* Amortização
* Estoque

## Fase 2

* Clientes (CRM)
* Eventos
* Cálculo de custos
* Lucro por evento

## Fase 3

* Orçamentos
* Conversão orçamento → evento

## Fase 4

* Financeiro
* Contas a pagar
* Contas a receber
* Fluxo de caixa
* Amortização mensal

## Fase 5

* Integração WhatsApp
* Conversas
* Envio de orçamento
* Lembretes financeiros

## Fase 6

* Relatórios
* Logs
* Permissões futuras
* Deploy
* CI/CD
* Testes completos

---

# 15. Boas Práticas Obrigatórias

O projeto deve conter:

* Arquitetura em camadas
* SOLID
* Clean Code
* Repository Pattern
* Service Layer
* Dependency Injection
* DTO / Schemas
* Testes unitários (implementados junto com as funcionalidades)
* Testes de integração (implementados junto com as funcionalidades)
* Docstrings
* Documentação
* Lint
* Type checking
* Logging
* Docker
* CI/CD
* Variáveis de ambiente
* Migrations de banco
* Versionamento de API

---

# 16. Resultado Final Esperado

O sistema será um:

## ERP + CRM + WhatsApp para gestão de eventos e produtos amortizados

Capaz de:

* Gerenciar clientes
* Conversar via WhatsApp
* Controlar produtos e estoque
* Calcular amortização
* Registrar eventos
* Criar orçamentos
* Controlar financeiro
* Fluxo de caixa
* Relatórios
* Arquitetura escalável
* Código testado
* Código documentado
* Deploy em nuvem
* Estrutura profissional de software
