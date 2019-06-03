CREATE DATABASE test;
USE test;
CREATE TABLE some_table (
	id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	some_key VARCHAR(30) NOT NULL
);
INSERT INTO some_table (id, some_key) VALUES (1, 'anything');
