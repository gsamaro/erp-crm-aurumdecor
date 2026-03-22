# Arquitetura de Software — Visão Geral

## Objetivo
Definir a arquitetura de alto nível para o ERP + CRM + WhatsApp, garantindo escalabilidade, manutenibilidade e evolução modular.

## Princípios
- Clean Architecture e SOLID
- Separação de responsabilidades por camadas
- Baixo acoplamento e alta coesão
- Testes automatizados (unitários e integrados) desde o início
- Observabilidade (logs e rastreabilidade)

## Visão Geral dos Componentes
```
[Streamlit UI]
      |
      v
[FastAPI — API Layer (Render)]
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

## Camadas
1. Presentation Layer (Streamlit)
2. API Layer (FastAPI)
3. Service Layer (regras de negócio)
4. Repository Layer (persistência)
5. Domain Layer (entidades e modelos)
6. Integration Layer (WhatsApp API)

## Decisões Arquiteturais
- Backend em Python com FastAPI
- Interface administrativa em Streamlit
- Banco de dados relacional PostgreSQL no Supabase
- Backend hospedado no Render
- Streamlit não acessa o banco diretamente; todo acesso passa pela API
- Migrations controladas por ferramenta dedicada (Alembic)

## Restrições
- Dashboard avançado fica para fase futura
- Integração WhatsApp é assíncrona via webhook
