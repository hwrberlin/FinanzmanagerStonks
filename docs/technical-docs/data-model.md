---
title: Data Model
parent: Technical Docs
nav_order: 3
---



# [Data model]
# Data Model

## 
user Tabelle
Attributes:
- id: Integer (Primary Key, Auto-incremented)
- username: Text (Must be unique and non-null)
- password: Text (Non-null)
- role: Text (Non-null, default value = 'user'. Can only be 'admin' or 'user')
  
Transactions Table
Attributes:
- id: Integer (Primary Key, Auto-incremented)
- user_id: Integer (Foreign Key, Non-null)
- amount: Real Number (Non-null)
- description: Text
- timestamp: Datetime (Default = Current Timestamp)
- transaction_type: Text (Non-null, default value = 'expense'. Can only be 'income' or 'expense')
- category: Text (Non-null, default value = 'miscellaneous')
- account_balance: Float (Non-null, default value = 0)

Budget Table
- Attributes:
- id: Integer (Primary Key, Auto-incremented)
- user_id: Integer (Foreign Key)
- amount: Decimal (with 2 decimal places, can be up to 10 digits long)
- end_date: Date
- name: Text
