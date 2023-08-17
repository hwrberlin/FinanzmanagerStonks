---
title: API Reference
parent: Technical Docs
nav_order: 4
---



# [API reference]
---

### `login()`

**Route:** `/`

**Methods:** `GET, POST`

**Purpose:** to sign or log in.

**Sample output:**

![get_lists() sample]()

---

### `homepage()`

**Route:** `/homepage`

**Methods:** `GET`

**Purpose:** to show all accessable funkctions and have an overview of the finances

**Sample output:**

![get_list_todos() sample](../assets/images/fswd-intro_02.png)

---

### `addTransaction()`

**Route:** `/addTransaction`

**Methods:** `GET, POST`

**Purpose:** insert a Transaction by user input 

**Sample output:**

Browser shows: `Database flushed and populated with some sample data.`


---

### `transactionOverview()`

**Route:** `/transactionOverview`

**Methods:** `GET`

**Purpose:** show all Transactions from the user

**Sample output:**

Browser shows: `Transactions from the user with delete buttons`


---

### `delete_transaction(id)`

**Route:** `delete_transaction/<int:id>`

**Methods:** `,POST`

**Purpose:** delete a selected transaction from the database (and changes Kontostand)

**Sample output:**

Browser shows: `Transaktion erfolgreich gelöscht!`

---

### `Steuerung()`

**Route:** `/Steuerung`

**Methods:** `GET`

**Purpose:** available as admin user, shows all users with delete buttons  

**Sample output:**

Browser shows: `Shows all users `

---

### `deleteUser()`

**Route:** `//deleteUser/<int:user_id>`

**Methods:** ` POST`

**Purpose:** delete selected User 

**Sample output:**

Browser shows: `Benutzer erfolgreich gelöscht.`

---


### `edit_profile()`

**Route:** `/edit_profile`

**Methods:** `GET, POST`

**Purpose:** lets the user change his username or delete his account, with insertion of his password 

**Sample output:**

Browser shows: `Benutzername erfolgreich aktualisiert!, Benutzerkonto erfolgreich gelöscht.`

---

### `insert/sample()`

**Route:** `/insert/sample`

**Methods:** `GET`

**Purpose:** insert a sample user and sample admin

**Sample output:**

Browser shows: `Database flushed and populated with some sample data.`

---

### `budget()`

**Route:** `/budget`

**Methods:** `GET, POST`

**Purpose:** user can create a budget

**Sample output:**

Browser shows: `f'Budget "{name}" erfolgreich erstellt.`


