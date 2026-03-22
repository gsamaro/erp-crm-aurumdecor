# Modelo Relacional (PostgreSQL)

## Padroes
- UUID como chave primaria (uuid_generate_v4()).
- created_at/updated_at como timestamptz.
- monetary values como numeric(12,2).

## Tabelas e Tipos SQL (resumo)

### users
- id uuid PK
- name varchar(120) NOT NULL
- email varchar(160) UNIQUE NOT NULL
- password_hash varchar(255) NOT NULL
- role varchar(40) NOT NULL
- active boolean NOT NULL DEFAULT true
- created_at timestamptz NOT NULL
- updated_at timestamptz NOT NULL

### clients
- id uuid PK
- name varchar(160) NOT NULL
- phone varchar(30)
- email varchar(160)
- status varchar(30) NOT NULL
- notes text
- created_at timestamptz NOT NULL
- updated_at timestamptz NOT NULL

### products
- id uuid PK
- name varchar(160) NOT NULL
- purchase_cost numeric(12,2) NOT NULL
- quantity integer NOT NULL
- unit_cost numeric(12,2) NOT NULL
- life_events integer
- life_months integer
- amortize_value numeric(12,2) NOT NULL
- amortized_value numeric(12,2) NOT NULL DEFAULT 0
- remaining_value numeric(12,2) NOT NULL
- cost_per_event numeric(12,2)
- stock_current integer NOT NULL
- purchase_date date
- active boolean NOT NULL DEFAULT true
- created_at timestamptz NOT NULL
- updated_at timestamptz NOT NULL

### product_amortization
- id uuid PK
- product_id uuid FK -> products.id
- reference_type varchar(30) NOT NULL -- event/month
- reference_id uuid
- amortized_value numeric(12,2) NOT NULL
- created_at timestamptz NOT NULL

### inventory
- id uuid PK
- product_id uuid FK -> products.id
- movement_type varchar(20) NOT NULL -- in/out/adjust
- quantity integer NOT NULL
- reason text
- created_at timestamptz NOT NULL

### events
- id uuid PK
- client_id uuid FK -> clients.id
- event_date date NOT NULL
- revenue numeric(12,2) NOT NULL DEFAULT 0
- total_cost numeric(12,2) NOT NULL DEFAULT 0
- profit numeric(12,2) NOT NULL DEFAULT 0
- status varchar(30) NOT NULL
- created_at timestamptz NOT NULL
- updated_at timestamptz NOT NULL

### event_products
- id uuid PK
- event_id uuid FK -> events.id
- product_id uuid FK -> products.id
- quantity integer NOT NULL
- amortized_value numeric(12,2) NOT NULL
- created_at timestamptz NOT NULL

### budgets
- id uuid PK
- client_id uuid FK -> clients.id
- status varchar(30) NOT NULL
- total_cost numeric(12,2) NOT NULL DEFAULT 0
- sale_price numeric(12,2) NOT NULL DEFAULT 0
- profit numeric(12,2) NOT NULL DEFAULT 0
- margin numeric(5,2)
- created_at timestamptz NOT NULL
- updated_at timestamptz NOT NULL

### budget_products
- id uuid PK
- budget_id uuid FK -> budgets.id
- product_id uuid FK -> products.id
- quantity integer NOT NULL
- unit_cost numeric(12,2) NOT NULL
- unit_price numeric(12,2) NOT NULL
- created_at timestamptz NOT NULL

### accounts_payable
- id uuid PK
- description varchar(200) NOT NULL
- amount numeric(12,2) NOT NULL
- due_date date NOT NULL
- status varchar(30) NOT NULL
- paid_at date
- related_event_id uuid FK -> events.id
- created_at timestamptz NOT NULL

### accounts_receivable
- id uuid PK
- description varchar(200) NOT NULL
- amount numeric(12,2) NOT NULL
- due_date date NOT NULL
- status varchar(30) NOT NULL
- received_at date
- related_event_id uuid FK -> events.id
- created_at timestamptz NOT NULL

### cash_flow
- id uuid PK
- entry_type varchar(20) NOT NULL -- in/out
- amount numeric(12,2) NOT NULL
- reference_type varchar(30)
- reference_id uuid
- entry_date date NOT NULL
- created_at timestamptz NOT NULL

### conversations
- id uuid PK
- client_id uuid FK -> clients.id
- channel varchar(30) NOT NULL
- created_at timestamptz NOT NULL

### messages
- id uuid PK
- conversation_id uuid FK -> conversations.id
- direction varchar(20) NOT NULL -- inbound/outbound
- content text NOT NULL
- sent_at timestamptz NOT NULL
- created_at timestamptz NOT NULL

### logs
- id uuid PK
- level varchar(20) NOT NULL
- source varchar(80) NOT NULL
- message text NOT NULL
- context jsonb
- created_at timestamptz NOT NULL
