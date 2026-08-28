# Entity-Relationship Diagram

This diagram is written in [Mermaid](https://mermaid.js.org/) syntax and
renders automatically when viewed on GitHub.

```mermaid
erDiagram
    CUSTOMERS ||--o{ TRANSACTIONS : "makes"
    CURRENCIES ||--o{ EXCHANGE_RATES : "is source of (from)"
    CURRENCIES ||--o{ EXCHANGE_RATES : "is target of (to)"
    CURRENCIES ||--o{ TRANSACTIONS : "is source of (from)"
    CURRENCIES ||--o{ TRANSACTIONS : "is target of (to)"

    CUSTOMERS {
        int customer_id PK
        string full_name
        string email
        string phone
        string id_document_number
        timestamp created_at
    }

    CURRENCIES {
        int currency_id PK
        string code
        string name
        string symbol
    }

    EXCHANGE_RATES {
        int rate_id PK
        int from_currency_id FK
        int to_currency_id FK
        float rate
        timestamp effective_date
    }

    TRANSACTIONS {
        int transaction_id PK
        int customer_id FK
        int from_currency_id FK
        int to_currency_id FK
        float amount_from
        float amount_to
        float rate_applied
        timestamp transaction_date
        string status
    }
```

## Relationships summary

| Relationship | Cardinality | Meaning |
|---|---|---|
| Customer → Transaction | 1 : N | One customer can make many exchange transactions |
| Currency → ExchangeRate (from) | 1 : N | A currency can appear as the "from" side of many rates |
| Currency → ExchangeRate (to) | 1 : N | A currency can appear as the "to" side of many rates |
| Currency → Transaction (from/to) | 1 : N | A currency can appear as the "from" or "to" side of many transactions |
