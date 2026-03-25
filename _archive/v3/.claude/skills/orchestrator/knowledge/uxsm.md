---
doc_meta:
  id: uxs
  display_name: UX Sitemap
  pillar: Design
  owner_role: UX Lead
  summary: Outlines page inventory, navigation structure, and routing hierarchy.
  order: 19
  gate: design
  requires:
  - prd
  - jour
  optional: []
  feeds:
  - wire
  - des
  - fe
uuid: <UUID>
version: 0.2.0
status: Draft
owners:
- <owner>
product: <product>
namespace: <namespace>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>
tags:
- UXSM
- Navigation
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# UX Sitemap — ${product}

> **Propósito:** inventário de **rotas** e **views** (páginas/modais/drawers/layouts), seus **estados obrigatórios**, e o **grafo de navegação**.  
> **Escopo:** sem tokens (Style Guide), sem schemas de endpoint (Backend), sem Given/When/Then (User Stories).  
> **Traçabilidade:** IDs aqui são usados por **Wireframes**, **Frontend Requirements**, **User Stories**, **Backend Requirements** e **Data Dictionary**.

---

## 0) Convenções de Nome (substitui GV/UV)

- **Rota (route_id)**: `r:/caminho/completo`
  - _Exs._ `r:/`, `r:/auth/login`, `r:/billing/invoices/:invoiceId`
- **View (view_id)**: `view.<domínio>.<página>[.<sub>]` (kebab-case; 2–3 níveis)
  - _Exs._ `view.auth.login`, `view.billing.invoices-list`, `view.billing.invoice-detail`, `view.billing.invoice-send` (type: modal)
- **Estado de UI**: `<view_id>#<state>`
  - _States padrão:_ `#default`, `#loading`, `#empty`, `#error`, `#success`
- **Componente (component_id)**: `cmp.<grupo>.<nome>`
  - _Exs._ `cmp.form.input-email`, `cmp.table.data-grid`
- **Fluxo (opcional)**: `flow.<área>.<objetivo>`
  - _Ex._ `flow.auth.onboarding`

**Lint (regex):**

- `route_id`: `^r:\/[a-z0-9\-\/:]*$`
- `view_id`: `^view\.[a-z0-9\-]+(\.[a-z0-9\-]+){1,2}$`
- `state`: `^#[a-z0-9\-]+$` (sempre após `view_id#`)
- `component_id`: `^cmp\.[a-z0-9\-]+\.[a-z0-9\-]+$`

> **Notas:**  
> • Parâmetros de rota em **camelCase**: `:invoiceId` (documentar tipo na coluna `params`).  
> • Queries: `?tab=overdue&sort=-date` (chaves em kebab-case).  
> • Guardas: `auth_guard = public | user | admin | role:<nome>`.  
> • Telemetria de página: event **`ev.page.view`** + `route_id` e UTM/referrer (payload no Data Dictionary).

---

## 1) Route Inventory

| route_id                       | name             | parent              | auth_guard | feature_flag | params            | redirect_from |
| ------------------------------ | ---------------- | ------------------- | ---------- | ------------ | ----------------- | ------------- |
| r:/                            | Home             | –                   | public     | –            | –                 | –             |
| r:/auth/login                  | Login            | r:/                 | public     | –            | –                 | –             |
| r:/dashboard                   | Dashboard        | r:/                 | user       | –            | –                 | –             |
| r:/billing/invoices            | Invoices         | r:/billing          | user       | billing_v2   | –                 | –             |
| r:/billing/invoices/:invoiceId | Invoice Detail   | r:/billing/invoices | user       | billing_v2   | :invoiceId (uuid) | –             |
| r:/settings/profile            | Profile Settings | r:/settings         | user       | –            | –                 | –             |

> **Boas práticas:** `parent` facilita breadcrumbs/menus; `redirect_from` mapeia URLs legadas se houver.

---

## 2) View Inventory

> **type:** `page | modal | drawer | layout | partial`  
> **stories:** IDs **US-#** (aceitação vive no _user-stories.md_)  
> **apis:** endpoints do BE (esta doc **não** redefine schemas)  
> **events:** **ev.\*** definidos no _data-dictionary.md_  
> **components:** **cmp.\*** (catálogo do FE)

| view_id                     | type  | route_id                       | priority | stories    | apis                           | events                     | components                                                    |
| --------------------------- | ----- | ------------------------------ | -------- | ---------- | ------------------------------ | -------------------------- | ------------------------------------------------------------- |
| view.auth.login             | page  | r:/auth/login                  | P0       | us-2       | POST /api/v1/auth/login        | ev.auth.login              | cmp.form.input-email, cmp.form.input-pass, cmp.button.primary |
| view.dashboard.home         | page  | r:/dashboard                   | P0       | us-5, us-6 | GET /api/v1/insights           | ev.dashboard.view          | cmp.card.kpi, cmp.chart.timeseries                            |
| view.billing.invoices-list  | page  | r:/billing/invoices            | P0       | us-7, us-9 | GET /api/v1/invoices           | ev.invoice.list            | cmp.table.data-grid, cmp.search.bar                           |
| view.billing.invoice-detail | page  | r:/billing/invoices/:invoiceId | P0       | us-10      | GET /api/v1/invoices/:id       | ev.invoice.view            | cmp.description.list, cmp.button.primary                      |
| view.billing.invoice-send   | modal | r:/billing/invoices/:invoiceId | P1       | us-11      | POST /api/v1/invoices/:id/send | ev.invoice.send            | cmp.form.textarea, cmp.button.primary                         |
| view.settings.profile       | page  | r:/settings/profile            | P1       | us-12      | GET/PUT /api/v1/users/me       | ev.settings.profile.update | cmp.form.input-text, cmp.avatar.uploader                      |

---

## 3) Required UI States por View

| view_id                     | required_states                    |
| --------------------------- | ---------------------------------- |
| view.auth.login             | #default, #loading, #error         |
| view.dashboard.home         | #default, #loading, #error         |
| view.billing.invoices-list  | #default, #loading, #empty, #error |
| view.billing.invoice-detail | #default, #loading, #error         |
| view.billing.invoice-send   | #default, #loading, #error         |
| view.settings.profile       | #default, #loading, #error         |

---

## 4) Navigation Graph (alto nível)

- `r:/auth/login` —(success)→ `r:/dashboard`
- `r:/dashboard` —(billing link)→ `r:/billing/invoices`
- `r:/billing/invoices` —(row click)→ `r:/billing/invoices/:invoiceId`
- `r:/billing/invoices/:invoiceId` ↔ _(open/close)_ `view.billing.invoice-send`
- `r:/dashboard` —(profile click)→ `r:/settings/profile`

> Dicas: descreva **gatilhos** entre parênteses (ex.: success/row click). Isso orienta Wireframes e FE.

---

## 5) Traceability (resumo)

| journey_step | route_id                       | view_id                           | stories    | primary_api                    |
| ------------ | ------------------------------ | --------------------------------- | ---------- | ------------------------------ |
| J1: Login    | r:/auth/login                  | view.auth.login                   | us-2       | POST /api/v1/auth/login        |
| J2: Acesso   | r:/dashboard                   | view.dashboard.home               | us-5, us-6 | GET /api/v1/insights           |
| J3: Billing  | r:/billing/invoices            | view.billing.invoices-list        | us-7, us-9 | GET /api/v1/invoices           |
| J4: Detalhe  | r:/billing/invoices/:invoiceId | view.billing.invoice-detail       | us-10      | GET /api/v1/invoices/:id       |
| J5: Envio    | r:/billing/invoices/:invoiceId | view.billing.invoice-send (modal) | us-11      | POST /api/v1/invoices/:id/send |

---

## 6) Regras & Lint

- **Proibido** GV.xxx.xx / UV.xxx.xx.
- **Obrigatório** usar os regex acima para `route_id`, `view_id`, `component_id`, `state`.
- **Sem tokens** ou CSS aqui (ver _style-guide.md_).
- **Sem schemas** de payload aqui (ver _backend-requirements.md_).
- **Sem Given/When/Then** aqui (ver _user-stories.md_).

---

## 7) Referências cruzadas

- **Frontend Requirements**: rotas/guards, componentes/props, states (aceitação do FE).
- **Wireframes**: “Screen = `view.*`”, ilustra **required_states**.
- **User Stories**: acceptance criteria (Gherkin) e métricas por **US‑#**.
- **Backend Requirements**: endpoints usados por `view.*` e telemetria `ev.*`.
- **Data Dictionary**: evento `ev.page.view` + payload de pageview e UTM.

---

## 8) AI Extraction Markers (machine‑readable)

```yaml
ROUTES:
  - id: r:/
    name: Home
    parent: null
    auth_guard: public
  - id: r:/auth/login
    name: Login
    parent: r:/
    auth_guard: public
  - id: r:/dashboard
    name: Dashboard
    parent: r:/
    auth_guard: user
  - id: r:/billing/invoices
    name: Invoices
    parent: r:/billing
    auth_guard: user
  - id: r:/billing/invoices/:invoiceId
    name: Invoice Detail
    parent: r:/billing/invoices
    auth_guard: user
  - id: r:/settings/profile
    name: Profile Settings
    parent: r:/settings
    auth_guard: user

VIEWS:
  - id: view.auth.login
    type: page
    route: r:/auth/login
    priority: P0
    stories: [us-2]
    apis: ["POST /api/v1/auth/login"]
    events: ["ev.auth.login"]
  - id: view.dashboard.home
    type: page
    route: r:/dashboard
    priority: P0
    stories: [us-5, us-6]
    apis: ["GET /api/v1/insights"]
    events: ["ev.dashboard.view"]

STATES:
  - view: view.billing.invoices-list
    required: ["#default", "#loading", "#empty", "#error"]

NAV_EDGES:
  - from: r:/auth/login
    to: r:/dashboard
    trigger: success
  - from: r:/billing/invoices
    to: r:/billing/invoices/:invoiceId
    trigger: row_click
  - from: r:/billing/invoices/:invoiceId
    to: view.billing.invoice-send
    trigger: open_modal
```

## 9) Gate Checklist (Design / Navigation)

Todas as rotas têm auth_guard correto.

Todas as views mapeadas a rotas e stories (US‑#).

Estados obrigatórios listados para cada view_id.

Transições críticas do grafo descritas.

Sem tokens/CSS, sem payloads, sem Gherkin
