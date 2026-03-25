# Arquitetura de Software — Testes e CI/CD

## Estratégia de Testes
- Testes unitários por camada (serviços, domínio, repositórios)
- Testes de integração cobrindo fluxos principais (evento → amortização → financeiro)
- Testes executados junto com cada entrega funcional

## Padrões
- Arrange-Act-Assert
- Fixtures reutilizáveis
- Seeds para banco em testes de integração

## CI/CD (mínimo)
- Lint + type checking
- Execução de testes unitários e integrados
- Build de container
- Deploy controlado por ambiente
