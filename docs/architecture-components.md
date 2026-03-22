# Arquitetura de Software — Componentes

## API Layer (FastAPI - Render)
- Autenticação e autorização (inicialmente Admin)
- Rotas por módulo: CRM, Produtos, Eventos, Orçamentos, Financeiro, Relatórios
- Validação via DTOs/Schemas
- Versionamento de API desde o início

## Service Layer
- Orquestra regras de negócio
- Calcula amortização, lucro e custos
- Converte orçamento em evento
- Gera contas a pagar/receber

## Repository Layer
- CRUD desacoplado por entidade
- Transações controladas por unidade de trabalho
- Consultas otimizadas por módulo
- Conexão com PostgreSQL no Supabase

## Domain Layer
- Entidades: Product, Event, Budget, Client, AccountsPayable, AccountsReceivable, Conversation, Message, etc.
- Regras de domínio isoladas e testáveis

## Presentation Layer (Streamlit)
- Interface administrativa por módulos
- Navegação simples e orientada a tarefas
- Acesso a dados somente via API (sem conexão direta ao banco)

## Integration Layer (WhatsApp API)
- Webhook para entrada de mensagens
- Serviço para envio de mensagens, orçamento e lembretes
- Logs de integração e reprocessamento
