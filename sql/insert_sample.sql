BEGIN TRANSACTION;
DELETE from sqlite_sequence;
INSERT INTO user (username, password, role) VALUES ('stonksadmin', 'pbkdf2:sha256:260000$sAgA2UxTvLkSfoeR$6c9d1e5d67984f6b585a5bf7d708eef4b8b4ebbd74f1a9c85c91980f6d46e3be', 'admin');
INSERT INTO user (username, password, role) VALUES ('stonksuser', 'pbkdf2:sha256:260000$4RjWgSwiySHDMoXj$326177632461fe6245dbe03ff8171c5a930cd4b04bf9870490c829b7f8c16a0e', 'user');

-- stonksadmin Transaktionen und Budgets
INSERT INTO transactions (user_id, amount, description, transaction_type, category, kontostand) VALUES (1, 1500.0, 'Monatliches Gehalt', 'einnahme', 'gehalt', 1500.0);
INSERT INTO transactions (user_id, amount, description, transaction_type, category, kontostand) VALUES (1, 850.0, 'Miete', 'ausgabe', 'wohnen', 650.0);
INSERT INTO transactions (user_id, amount, description, transaction_type, category, kontostand) VALUES (1, 50.0, 'Tanken', 'ausgabe', 'transport', 600.0);
INSERT INTO transactions (user_id, amount, description, transaction_type, category, kontostand) VALUES (1, 150.0, 'Lebensmittel', 'ausgabe', 'essen', 450.0);
INSERT INTO budget (user_id, category, amount, end_date) VALUES (1, 'wohnen', 900.0, '2023-09-30');
INSERT INTO budget (user_id, category, amount, end_date) VALUES (1, 'transport', 150.0, '2023-09-30');
INSERT INTO budget (user_id, category, amount, end_date) VALUES (1, 'essen', 250.0, '2023-09-30');

-- stonksuser Transaktionen und Budgets
INSERT INTO transactions (user_id, amount, description, transaction_type, category, kontostand) VALUES (2, 1200.0, 'Monatliches Gehalt', 'einnahme', 'gehalt', 1200.0);
INSERT INTO transactions (user_id, amount, description, transaction_type, category, kontostand) VALUES (2, 700.0, 'Miete', 'ausgabe', 'wohnen', 500.0);
INSERT INTO transactions (user_id, amount, description, transaction_type, category, kontostand) VALUES (2, 60.0, 'ÖPNV-Ticket', 'ausgabe', 'transport', 440.0);
INSERT INTO transactions (user_id, amount, description, transaction_type, category, kontostand) VALUES (2, 100.0, 'Lebensmittel', 'ausgabe', 'essen', 340.0);
INSERT INTO budget (user_id, category, amount, end_date) VALUES (2, 'wohnen', 800.0, '2023-09-30');
INSERT INTO budget (user_id, category, amount, end_date) VALUES (2, 'transport', 100.0, '2023-09-30');
INSERT INTO budget (user_id, category, amount, end_date) VALUES (2, 'essen', 200.0, '2023-09-30');

COMMIT;
