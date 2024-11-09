CREATE DATABASE IF NOT EXISTS sso_db;
CREATE USER IF NOT EXISTS 'sso_user'@'localhost' IDENTIFIED BY 'ijaodhsuajsdujdaslidjsda';
GRANT ALL PRIVILEGES ON sso_db.* TO 'sso_user'@'localhost';
FLUSH PRIVILEGES;