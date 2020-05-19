DROP TABLE if exists accounts;
CREATE TABLE if not exists accounts (
	account_id serial PRIMARY KEY,
	username VARCHAR (32) UNIQUE NOT NULL,
    display_name TEXT,
	auth_verifier BYTEA UNIQUE NOT NULL,
    auth_salt BYTEA NOT NULL,
    muk_salt BYTEA NOT NULL
);
