BEGIN TRANSACTION;
DELETE from sqlite_sequence;
INSERT INTO user (username, password, role) VALUES ('stonksadmin', 'pbkdf2:sha256:260000$sAgA2UxTvLkSfoeR$6c9d1e5d67984f6b585a5bf7d708eef4b8b4ebbd74f1a9c85c91980f6d46e3be', 'admin');
INSERT INTO user (username, password, role) VALUES ('stonksuser', 'pbkdf2:sha256:260000$4RjWgSwiySHDMoXj$326177632461fe6245dbe03ff8171c5a930cd4b04bf9870490c829b7f8c16a0e', 'user');
COMMIT;