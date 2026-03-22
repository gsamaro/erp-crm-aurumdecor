# Arquitetura de Software — Integrações

## WhatsApp API
- Webhook para receber mensagens
- Endpoint dedicado para validação e assinatura
- Processamento assíncrono (fila futura)
- API hospedada no Render

## Fluxo básico
1. Mensagem recebida via webhook
2. API (Render) processa e valida
3. Registro no PostgreSQL (Supabase)
4. Vinculação ao cliente
5. Resposta ou ação no CRM

## Observabilidade
- Logs por conversa
- Alertas em caso de falha na integração
