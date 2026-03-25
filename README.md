# erp-crm-aurumdecor

## Setup local
1. Crie um ambiente virtual.
2. Instale dependências:
   ```bash
   pip install -e .
   pip install -e .[dev]
   ```
3. Crie o arquivo `.env` baseado em `.env.example`.

## Secrets
- Nunca commitar `.env` (já está no `.gitignore`).
- Local: use `.env` para variáveis como `DATABASE_URL`, `SECRET_KEY` e `ENCRYPTION_KEY`.
- Render/Streamlit Cloud: configure as variáveis de ambiente no painel do serviço.
- `ENCRYPTION_KEY` deve ser uma chave Fernet (base64 urlsafe, 32 bytes). Exemplo de geração:
  ```bash
  python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
  ```

## Qualidade e testes
```bash
ruff check .
mypy app
pytest
```
