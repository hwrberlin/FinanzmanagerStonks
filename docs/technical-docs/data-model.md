---
title: Data Model
parent: Technical Docs
nav_order: 3
---



# [Data model]
# Data Model

## 

## User Table

| Attribute  | Type          | Properties                                        |
|-----------|---------------|---------------------------------------------------|
| id        | INTEGER       | PRIMARY KEY, AUTOINCREMENT                        |
| username  | TEXT          | NOT NULL, UNIQUE                                  |
| password  | TEXT          | NOT NULL                                          |
| role      | TEXT          | NOT NULL, DEFAULT 'user', CHECK IN ('admin', 'user') |

## Transactions Table

| Attribute       | Type     | Properties                                                                 |
|-----------------|----------|----------------------------------------------------------------------------|
| id              | INTEGER  | PRIMARY KEY, AUTOINCREMENT                                                 |
| user_id         | INTEGER  | FOREIGN KEY, NOT NULL                                                      |
| amount          | REAL     | NOT NULL                                                                   |
| description     | TEXT     |                                                                            |
| timestamp       | DATETIME | DEFAULT CURRENT_TIMESTAMP                                                  |
| transaction_type| TEXT     | NOT NULL, DEFAULT 'expense', CHECK IN ('income', 'expense')                |
| category        | TEXT     | NOT NULL, DEFAULT 'miscellaneous'                                          |
| account_balance | FLOAT    | NOT NULL, DEFAULT 0                                                        |

## Budget Table

| Attribute | Type           | Properties                            |
|-----------|----------------|---------------------------------------|
| id        | INTEGER        | PRIMARY KEY, AUTOINCREMENT            |
| user_id   | INTEGER        | FOREIGN KEY                           |
| amount    | DECIMAL(10,2)  |                                       |
| end_date  | DATE           |                                       |
| name      | TEXT           |                                       |

