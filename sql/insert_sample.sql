BEGIN TRANSACTION;

DELETE from sqlite_sequence;
INSERT INTO user (username, password, role) VALUES ('stonksadmin', 'stonksadmin', 'admin');
INSERT INTO user (username, password, role) VALUES ('stonksuser', 'stonksuser', 'user');
COMMIT;