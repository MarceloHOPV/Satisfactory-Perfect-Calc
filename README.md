# Satisfactory Perfect Calc

> A factory-optimization calculator for the game **Satisfactory**. Plan production lines, calculate exact machine counts, and find the minimum all-integer layout using LCM scaling.

![Stack](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Stack](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Stack](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![Stack](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

---

## Table of Contents

1. [Requisitos Obrigatórios Atendidos](#requisitos-obrigatórios-atendidos)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Quick Start (Docker)](#quick-start-docker)
6. [Development Setup (without Docker)](#development-setup-without-docker)
7. [Running Tests](#running-tests)
8. [API Reference](#api-reference)
9. [Database Schema](#database-schema)
10. [How the Calculator Works](#how-the-calculator-works)

---

## Requisitos Obrigatórios Atendidos

> Mapeamento direto entre cada requisito da disciplina C116 e onde ele foi implementado.

---

### ✅ Tema livre
**Calculadora de linhas de produção para o jogo Satisfactory.**  
Dado um item alvo e uma taxa desejada (unidades/min), a ferramenta resolve recursivamente toda a cadeia de dependências, conta o número exato de máquinas necessárias em cada etapa e calcula os recursos brutos totais. Inclui escalonamento por MMC para obter linhas com número inteiro de máquinas.

---

### ✅ Pelo menos 3 páginas/telas no Frontend

| Página | Rota | Descrição |
|---|---|---|
| **Home** | `/` | Apresentação da ferramenta, produções salvas e acesso rápido à calculadora |
| **Calculator** | `/calculator` | Calculadora principal com busca de itens, árvore de produção e resumo de máquinas |
| **Settings** | `/settings` | Troca de idioma (EN / PT-BR) e tema (dark / light) |

Implementado em [`frontend/src/pages/`](frontend/src/pages/).

---

### ✅ 2 ou mais tabelas no banco de dados

O banco possui **6 tabelas**:

| Tabela | Descrição |
|---|---|
| `buildings` | Máquinas do jogo (Smelter, Constructor, Assembler…) |
| `items` | Todos os itens (minérios, componentes, equipamentos) |
| `recipes` | Receitas de produção |
| `recipe_ingredients` | Ingredientes de cada receita (tabela de junção N:M) |
| `recipe_products` | Produtos de cada receita (tabela de junção N:M) |
| `saved_productions` | Produções salvas pelo usuário |

Definidas em [`backend/app/models.py`](backend/app/models.py).

---

### ✅ Pelo menos 10 operações com ao menos 1 uso de cada método REST (GET, POST, PUT, DELETE)

O backend expõe **21 rotas** distribuídas em 5 recursos:

| Método | Rota | Operação |
|---|---|---|
| `GET` | `/api/v1/items/` | Listar itens |
| `GET` | `/api/v1/items/{id}` | Buscar item |
| `POST` | `/api/v1/items/` | Criar item |
| `PUT` | `/api/v1/items/{id}` | Atualizar item |
| `DELETE` | `/api/v1/items/{id}` | Deletar item |
| `GET` | `/api/v1/recipes/` | Listar receitas |
| `GET` | `/api/v1/recipes/{id}` | Buscar receita |
| `POST` | `/api/v1/recipes/` | Criar receita |
| `PUT` | `/api/v1/recipes/{id}` | Atualizar receita |
| `DELETE` | `/api/v1/recipes/{id}` | Deletar receita |
| `GET` | `/api/v1/buildings/` | Listar buildings |
| `GET` | `/api/v1/buildings/{id}` | Buscar building |
| `POST` | `/api/v1/buildings/` | Criar building |
| `PUT` | `/api/v1/buildings/{id}` | Atualizar building |
| `DELETE` | `/api/v1/buildings/{id}` | Deletar building |
| `POST` | `/api/v1/calculate/` | Executar cálculo de produção |
| `GET` | `/api/v1/saved-productions/` | Listar produções salvas |
| `GET` | `/api/v1/saved-productions/{id}` | Buscar produção salva |
| `POST` | `/api/v1/saved-productions/` | Salvar produção |
| `PUT` | `/api/v1/saved-productions/{id}` | Atualizar produção salva |
| `DELETE` | `/api/v1/saved-productions/{id}` | Deletar produção salva |

Todos os métodos REST estão cobertos. Documentação interativa disponível em `http://localhost:8000/docs`.  
Implementado em [`backend/app/routers/`](backend/app/routers/).

---

### ✅ Toda a aplicação deve rodar em containers via docker-compose

Três serviços orquestrados pelo [`docker-compose.yml`](docker-compose.yml):

| Serviço | Imagem | Porta | Descrição |
|---|---|---|---|
| `db` | `postgres:16-alpine` | 5432 | Banco de dados PostgreSQL |
| `backend` | build local | 8000 | API FastAPI + seed automático na inicialização |
| `frontend` | build local (nginx) | 3000 | React buildado servido pelo nginx com proxy reverso para `/api/*` |

Para subir tudo:
```bash
cp .env.example .env
docker compose up --build
```

---

### ✅ Ao menos uma relação N:M e outra N:1 no banco de dados

**Relação N:1 — `recipes → buildings`**
> Muitas receitas pertencem a uma mesma máquina.  
> `recipes.building_id` → FK para `buildings.id`

**Relação N:M — `items ↔ recipes` (via duas tabelas de junção)**
> Um item pode aparecer como ingrediente em várias receitas, e uma receita pode ter vários ingredientes.  
> Tabela de junção: `recipe_ingredients` (`recipe_id` + `item_id` + `amount_per_min`)

> Um item pode ser produto de várias receitas (ex: receitas alternativas), e uma receita pode produzir vários itens.  
> Tabela de junção: `recipe_products` (`recipe_id` + `item_id` + `amount_per_min`)

```
buildings  1 ──< recipes >──────────────── recipe_ingredients >── items
                                └──────── recipe_products    >── items
```

---

## Features

| Feature | Description |
|---|---|
| **Dependency tree** | Recursively resolves the full ingredient chain for any item |
| **Machine counter** | Calculates exact (possibly fractional) machine counts per recipe |
| **LCM scaling** | Scales the entire production line to the minimum all-integer layout |
| **Alternate recipes** | Switch between standard and alternate recipes per item |
| **Save productions** | Persist calculation results with a custom name |
| **Dark / Light mode** | Toggle via UI or Settings page |
| **i18n** | English and Brazilian Portuguese |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 · FastAPI · SQLAlchemy 2 · Pydantic v2 |
| Tests | Pytest · httpx · SQLite (in-memory) |
| Frontend | React 18 · TypeScript · Vite · Tailwind CSS |
| Database | PostgreSQL 16 |
| Orchestration | Docker · Docker Compose |
| Web server | nginx (serves React build + proxies `/api/*`) |

---

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app, CORS, startup
│   │   ├── database.py        # SQLAlchemy engine + session
│   │   ├── models.py          # ORM models (Building, Item, Recipe, …)
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── routers/           # One file per resource + calculator
│   │   └── services/
│   │       └── calculator.py  # Core production-tree algorithm
│   ├── tests/                 # pytest test suite
│   ├── seed.py                # Seeds DB with real Satisfactory data
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/             # Home · Calculator · Settings
│   │   ├── components/        # Navbar · ProductionTree · MachineCard
│   │   ├── contexts/          # ThemeContext · LanguageContext
│   │   ├── i18n/              # en.ts · pt.ts
│   │   └── api/               # axios client + TypeScript types
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## Quick Start (Docker)

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) ≥ 24
- Git

### 1. Clone the repository

```bash
git clone https://github.com/MarceloHOPV/Satisfactory-Perfect-Calc.git
cd Satisfactory-Perfect-Calc
```

### 2. Configure environment

```bash
cp .env.example .env
# Optionally change POSTGRES_PASSWORD in .env
```

### 3. Build and start all services

```bash
docker compose up --build
```

The first run takes ~2-3 minutes to build images. Once all services are healthy:

| Service | URL |
|---|---|
| **Frontend** | <http://localhost:3000> |
| **Backend API** | <http://localhost:8000/api/v1> |
| **Swagger docs** | <http://localhost:8000/docs> |

### 4. Stop

```bash
docker compose down        # keep database volume
docker compose down -v     # also delete database
```

### Viewing logs

```bash
docker compose logs -f            # all services
docker compose logs -f backend    # backend only
docker compose logs -f frontend   # nginx only
```

---

## Development Setup (without Docker)

### Backend

```bash
cd backend

# Create and activate venv
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt

# Point to a running PostgreSQL (or use SQLite for quick testing)
export DATABASE_URL="postgresql://postgres:changeme@localhost:5432/satisfactory_calc"

# Create tables and seed data
python seed.py

# Start dev server with hot-reload
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev          # starts Vite on http://localhost:5173
                     # proxies /api/* to http://localhost:8000
```

---

## Running Tests

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

Tests use an in-memory SQLite database — no running Postgres needed.

---

## API Reference

All endpoints are prefixed with `/api/v1`.  
Interactive docs: **<http://localhost:8000/docs>**

### Items

| Method | Path | Description |
|---|---|---|
| `GET` | `/items/` | List items (supports `?search=` and `?category=`) |
| `GET` | `/items/{id}` | Get single item |
| `POST` | `/items/` | Create item |
| `PUT` | `/items/{id}` | Update item |
| `DELETE` | `/items/{id}` | Delete item |

### Recipes

| Method | Path | Description |
|---|---|---|
| `GET` | `/recipes/` | List recipes (supports `?item_id=`, `?building_id=`, `?include_alternates=`) |
| `GET` | `/recipes/{id}` | Get single recipe (with ingredients + products) |
| `POST` | `/recipes/` | Create recipe |
| `PUT` | `/recipes/{id}` | Update recipe (replaces ingredients/products when provided) |
| `DELETE` | `/recipes/{id}` | Delete recipe |

### Buildings

| Method | Path | Description |
|---|---|---|
| `GET` | `/buildings/` | List buildings |
| `GET` | `/buildings/{id}` | Get building |
| `POST` | `/buildings/` | Create building |
| `PUT` | `/buildings/{id}` | Update building |
| `DELETE` | `/buildings/{id}` | Delete building |

### Calculator

| Method | Path | Description |
|---|---|---|
| `POST` | `/calculate/` | Run production calculation |

**Request body:**

```json
{
  "target_item_id": 5,
  "target_rate": 60.0,
  "recipe_overrides": {},
  "scale_to_integers": false
}
```

`recipe_overrides` is a map of `item_id → recipe_id` to override the default recipe selection per item.

### Saved Productions

| Method | Path | Description |
|---|---|---|
| `GET` | `/saved-productions/` | List saved productions |
| `GET` | `/saved-productions/{id}` | Get one |
| `POST` | `/saved-productions/` | Save a production |
| `PUT` | `/saved-productions/{id}` | Update name/description |
| `DELETE` | `/saved-productions/{id}` | Delete |

---

## Database Schema

```mermaid
erDiagram
    buildings {
        int     id          PK
        varchar name
        text    description
    }

    items {
        int     id          PK
        varchar name
        text    description
        varchar category
    }

    recipes {
        int     id          PK
        varchar name
        int     building_id FK
        boolean is_alternate
    }

    recipe_ingredients {
        int   recipe_id     FK
        int   item_id       FK
        float amount_per_min
    }

    recipe_products {
        int   recipe_id     FK
        int   item_id       FK
        float amount_per_min
    }

    saved_productions {
        int      id          PK
        varchar  name
        text     description
        json     config
        datetime created_at
        datetime updated_at
    }

    buildings       ||--o{ recipes             : "hosts (N:1)"
    recipes         ||--o{ recipe_ingredients  : "has inputs"
    recipes         ||--o{ recipe_products     : "has outputs"
    items           ||--o{ recipe_ingredients  : "used as ingredient (N:M)"
    items           ||--o{ recipe_products     : "produced as output (N:M)"
```

**Relações:**
- **N:1** — `recipes.building_id → buildings.id` (várias receitas por máquina)
- **N:M** — `items ↔ recipes` via `recipe_ingredients` (itens como entrada)
- **N:M** — `items ↔ recipes` via `recipe_products` (itens como saída)

---

## How the Calculator Works

### Algorithm

The calculator uses a **depth-first recursive traversal** of the recipe dependency DAG:

1. Given a target item and desired rate (e.g., 10 Reinforced Iron Plates/min):
2. Find the recipe that produces the item.
3. Calculate `machines_needed = target_rate / recipe_output_rate`.
4. For each ingredient in the recipe, compute its required rate and recurse.
5. Accumulate totals in flat dicts (`machine_demands`, `raw_demands`).
6. Return both the full tree (for display) and the aggregated summaries.

### LCM Scaling

When `scale_to_integers = true`:

1. Express each machine count as a `Fraction` (exact rational arithmetic).
2. Compute `LCM` of all denominators.
3. Multiply the entire production line by that factor.

**Example** — target 7 Reinforced Iron Plates/min:

| Recipe | Machines (raw) | Machines (×10 LCM) |
|---|---|---|
| RIP Assembler | 7/5 = 1.4 | **14** |
| Iron Plate Constructor | 21/10 = 2.1 | **21** |
| Screw Constructor | 21/10 = 2.1 | **21** |
| Iron Rod Constructor | 7/5 = 1.4 | **14** |
| Iron Ingot Smelter | 14/5 = 2.8 | **28** |

Scale factor = 10 → produces **70 RIP/min** with all-integer machines.

---

## Good Practices

- Never commit `.env` to version control — use `.env.example` as template.
- The seed script is idempotent — safe to run multiple times.
- Alternate recipes are stored with `is_alternate = true` and can be selected per item in the UI.
- Add new items/recipes via the API (`POST /api/v1/items/`, `POST /api/v1/recipes/`) or extend `seed.py`.

---

*INATEL — Disciplina C116 — Projeto Final — 2026*
