# Padrão UI/UX — ERP Aurum Decor

## Objetivo
Definir o padrão visual e de experiência para o ERP em Streamlit, garantindo uma interface moderna, limpa e elegante para uma empresa de decoração de festas e eventos.

## Direção visual
- **Clean, moderno e minimalista**
- **Muito espaço em branco** e respiro entre blocos
- **Interface leve e agradável**
- **Referências**: Notion, Canva, Monday, Stripe Dashboard
- **Evitar aparência de sistemas contábeis antigos**

## Paleta de cores (oficial)
| Papel | Cor | Hex |
| --- | --- | --- |
| Principal | Verde oliva | `#6B8E23` |
| Secundária | Bege | `#E8E3D9` |
| Destaque | Rosé | `#D4A5A5` |
| Background | Off-white | `#FAFAF9` |
| Cards | Branco | `#FFFFFF` |
| Bordas | Cinza claro | `#E5E7EB` |
| Texto principal | Cinza escuro | `#2F2F2F` |
| Texto secundário | Cinza médio | `#6B7280` |
| Sucesso | Verde | `#22C55E` |
| Alerta | Amarelo | `#F59E0B` |
| Erro | Vermelho | `#EF4444` |

## Tipografia
- Fonte principal: **sans-serif moderna e simples** (ex.: "Inter" ou "Manrope")
- Tamanhos sugeridos:
  - Título de página: 26–30px
  - Subtítulos: 18–20px
  - Texto comum: 14–16px
  - Labels e metadados: 12–13px

## Layout padrão das páginas (Streamlit)
1. **Sidebar** para navegação global
2. **Header com título** e descrição curta da página
3. **Cards de KPIs** no topo (3–5 cards)
4. **Área de filtros** (busca, datas, status)
5. **Tabela principal** com ações por linha
6. **Botões de ação** no canto superior direito (Novo, Editar, Excluir)
7. **Formulários em seções**, com campos agrupados
8. **Uso de colunas** para organizar conteúdo

> Regra: todo conteúdo deve estar em blocos claros, com espaçamento generoso, evitando páginas muito longas.

## Padrão de componentes
### Cards de métricas (KPIs)
- Fundo branco, borda clara, raio 12px
- Número em destaque + label + variação (seta ou tag)
- Ícone discreto à esquerda

### Tabelas
- Cabeçalho leve, sem contraste agressivo
- Linhas com espaçamento vertical
- Borda sutil ou sombra leve
- Coluna de ações sempre à direita
- **Padrão**: tabela custom (HTML/CSS) para maior controle visual

### Formulários
- Agrupados por seções (ex.: Dados do Cliente, Endereço, Observações)
- Labels acima dos campos
- Inputs com fundo branco e borda suave

### Botões
- **Primário**: verde oliva, texto branco
- **Secundário**: fundo bege, texto cinza escuro
- **Tertiário**: texto com borda leve, usado para ações menores

### Tags de status
- **Aprovado**: verde (`#22C55E`)
- **Pendente**: amarelo (`#F59E0B`)
- **Cancelado**: vermelho (`#EF4444`)
- **Enviado**: rosé (`#D4A5A5`)

### KPI e indicadores
- Sempre em cards horizontais
- Uso de ícone + número + variação

### Timeline de interações
- Linha vertical à esquerda
- Cada item com data, descrição e ícone
- **Implementação**: pode usar componentes externos (ex.: `streamlit-elements`) quando necessário

### Kanban (Orçamentos / CRM)
- Colunas com fundo bege claro
- Cards em branco com borda sutil
- Mover status com drag & drop (quando possível)
- **Implementação**: preferencialmente com `streamlit-elements` para layout mais fluido

## Regras de UX
- **Métricas importantes sempre no topo**
- **Busca e filtros visíveis** em todas as páginas de listagem
- **Evitar telas longas** (use tabs, seções ou colunas)
- **Agrupar informações relacionadas**
- **Minimizar cliques** (ação principal sempre visível)
- **Botões principais no canto superior direito**
- **Cores apenas para ações e status**
- **Consistência total** entre módulos

## Padrão visual
- Bordas arredondadas (10–12px)
- Cards com sombra leve
- Muito espaço em branco
- Ícones simples e lineares
- Layout em blocos
- Evitar excesso de linhas e divisórias
- Tipografia limpa e moderna

## Exemplo de layout de página

```
[SIDEBAR]
ERP Aurum Decor
- Clientes
- Produtos
- Eventos
- Orçamentos
- Financeiro
- WhatsApp

[HEADER]
Título: Clientes
Descrição: Gestão de clientes e histórico de interações

[KPIs]
| Total de clientes | Novos no mês | Orçamentos ativos | Taxa de conversão |

[FILTROS]
- Busca por nome
- Status (Lead / Cliente)
- Último contato

[AÇÕES]                               [Novo Cliente] [Exportar]

[TABELA]
| Nome | Status | Último evento | Telefone | Ações |

[FORMULÁRIO]
Seção 1: Dados do Cliente
Seção 2: Endereço
Seção 3: Observações
```

## Exemplo visual em Streamlit (estrutura)
```python
import streamlit as st
from components.ui import configure_page, render_sidebar, page_header

configure_page("Clientes", "🧑‍💼")
render_sidebar(__file__)
page_header("Clientes", "Gestão de clientes e histórico de interações", "CRM")

col_kpi = st.columns(4)
col_kpi[0].metric("Total", "328")
col_kpi[1].metric("Novos no mês", "24", "+8%")
col_kpi[2].metric("Orçamentos ativos", "12")
col_kpi[3].metric("Conversão", "38%", "+4%")

st.markdown("### Filtros")
filters = st.columns([2, 1, 1, 1])
filters[0].text_input("Buscar cliente")
filters[1].selectbox("Status", ["Todos", "Lead", "Cliente"])
filters[2].date_input("Último contato")
filters[3].button("Aplicar")

actions = st.columns([1, 1, 6])
actions[0].button("Novo cliente")
actions[1].button("Exportar")

st.markdown("### Lista de clientes")
st.dataframe([])

st.markdown("### Cadastro")
form = st.form("cliente")
with form:
    st.text_input("Nome")
    st.text_input("Telefone")
    st.text_input("Email")
    st.text_area("Observações")
    st.form_submit_button("Salvar")
```
