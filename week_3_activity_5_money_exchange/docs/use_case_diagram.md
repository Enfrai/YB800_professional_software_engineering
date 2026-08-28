# Use Case Diagram — Money Exchange System

**Week 4 — Activity 1.2 (update of Activity 1.1)**

This is the revised version of the use case diagram from Activity 1.1 for
the Money Exchange System (originally modeled in Week 3 — Activity 5; see
the main [README](../README.md) for the database this maps onto).

## What changed since Activity 1.1

Activity 1.1 only showed **associations** (actor ↔ use case). This update
adds the other three standard use-case relationship types so the diagram
communicates *how* the use cases relate to each other, not just *who* uses
them:

| Relationship | Notation | Added in this version |
|---|---|---|
| Association | solid line | *(carried over from 1.1)* |
| **Generalization** | solid line, hollow triangle arrowhead | **New** — `Teller` and `Manager` generalize from an abstract `Staff` actor |
| **`<<include>>`** | dashed line, open arrowhead, arrow points to the *included* use case | **New** — `Perform Currency Exchange` includes `Apply Exchange Rate` |
| **`<<extend>>`** | dashed line, open arrowhead, arrow points to the *base* use case | **New** — `Update Customer Info` extends `Register Customer` |

![Use case diagram](use_case_diagram.svg)

*(If the image doesn't render in your viewer, open
[`use_case_diagram.svg`](use_case_diagram.svg) directly.)*

## Actors

| Actor | Type | Description |
|---|---|---|
| **Customer** | Concrete | The person bringing money in to exchange. Checks rates, requests an exchange, and reviews their own past transactions. |
| **Staff** | Abstract (generalization parent) | Not a real user by itself — represents behaviour common to every employee of the business: logging into the system. `Teller` and `Manager` both generalize from `Staff`, so both inherit the `Login` use case without it being drawn twice. |
| **Teller** | Concrete, generalizes `Staff` | Front-counter employee. Registers new customers and processes exchange transactions. |
| **Manager** | Concrete, generalizes `Staff` | Back-office employee. Keeps rates and currencies current and pulls reports. |

**Why generalization matters here:** without it, `Login` would need a
separate association line from both `Teller` and `Manager`, which
duplicates the same fact twice and hides the fact that they're both
"staff" in the business sense. Modeling `Staff` as an abstract actor and
having `Teller`/`Manager` generalize from it lets `Login` — and any future
staff-only use case — be defined once and inherited by both.

## Use cases

| Use case | Actor(s) | Description |
|---|---|---|
| **Login** | Staff *(inherited by Teller, Manager)* | Authenticate before accessing any staff-facing function. Customers don't need an account, so this use case has no direct association with `Customer`. |
| **View exchange rates** | Customer, Teller | Look up the current rate between two currencies before committing to an exchange. |
| **Register customer** | Teller | Create a new `customers` record (name, email, phone, ID document) the first time someone visits. |
| **Update customer info** *(extends Register Customer)* | Teller | Correct or update a customer's contact details. Modeled as `<<extend>>` rather than part of the main flow because it only happens *conditionally* — when a returning customer's details have changed — not on every registration. |
| **Perform currency exchange** | Customer, Teller | The core use case: convert an amount from one currency to another, creating a row in `transactions`. |
| **Apply exchange rate** *(included by Perform Currency Exchange)* | — *(sub-behaviour)* | Look up the latest rate from `exchange_rates` and calculate the converted amount. Modeled as `<<include>>` because this step is **mandatory** and identical every single time an exchange happens — it's not optional, so it belongs in the base flow rather than as an extension. |
| **View transaction history** | Customer, Teller, Manager | Customers see their own past exchanges; staff can look up any customer's history for service or audit purposes. |
| **Update exchange rate** | Manager | Add a new, timestamped rate entry for a currency pair when the market moves. |
| **Manage currencies** | Manager | Add a currency the business now supports, or retire one it no longer trades. |
| **Generate reports** | Manager | Produce summaries (e.g. daily volume, most-traded pairs) from `transactions` for business oversight. |

## `<<include>>` vs `<<extend>>` — why each one was chosen here

- **`<<include>>` (Perform Currency Exchange → Apply Exchange Rate):**
  used when the included behaviour is *always* required and the base use
  case would be incomplete without it. You cannot perform an exchange
  without applying a rate — there's no valid path around it.
- **`<<extend>>` (Update Customer Info → Register Customer):**
  used when the behaviour is *optional* and only triggers under a
  condition. Registering a customer doesn't always require updating their
  info afterward — it's an extra step that applies only in some cases
  (e.g. the teller notices outdated contact details).

This same reasoning generalizes to other use cases not drawn explicitly to
keep the diagram readable: for example, `Register Customer`,
`Update Exchange Rate`, `Manage Currencies`, and `Generate Reports` all
implicitly require `Login` first (inherited from the `Staff`
generalization), and `View Transaction History` could similarly be
extended by an optional `Filter by Date Range` use case.

## How this maps to the Week 3 database and code

- *View exchange rates* / *Update exchange rate* → `exchange_rates` table
- *Register customer* / *Update customer info* → `customers` table
- *Perform currency exchange* / *Apply exchange rate* → `transactions`
  (write) + `exchange_rates` (read) + `customers` (read)
- *View transaction history* / *Generate reports* → `transactions` table
- *Manage currencies* → `currencies` table

`ExchangeService.perform_exchange()` in
[`src/services.py`](../src/services.py) is the concrete implementation of
the "Perform currency exchange" use case together with its included
"Apply exchange rate" step — the code's structure (a service method that
always calls into a rate lookup) mirrors the `<<include>>` relationship in
the diagram directly.
