CREATE SEQUENCE batch_seq START 1;
CREATE TABLE batches (
    batch_id INTEGER PRIMARY KEY DEFAULT nextval('batch_seq'),
    rows_added BIGINT NOT NULL,
    target_table VARCHAR NOT NULL,
    upload_datetime TIMESTAMP
);

-- ====================== ENTITIES =========================
CREATE SEQUENCE parent_account_seq START 1;
CREATE TABLE parent_accounts (
    parent_account_id INTEGER PRIMARY KEY DEFAULT nextval('parent_account_seq'),
    parent_account_name VARCHAR UNIQUE NOT NULL,
    normalized_parent_name VARCHAR UNIQUE NOT NULL,
    first3_token VARCHAR NOT NULL
);

CREATE SEQUENCE vendor_customer_id_seq START 1;
CREATE TABLE vendor_customers (
    vendor_customer_id INTEGER PRIMARY KEY DEFAULT nextval('vendor_customer_id_seq'),
    vendor_name VARCHAR,
    raw_vendor_customer_name VARCHAR,
    normalized_vendor_customer_name VARCHAR NOT NULL,
    billing_zip VARCHAR,
    billing_state VARCHAR,
    billing_city VARCHAR,
    first3_token VARCHAR NOT NULL 
);

CREATE SEQUENCE erp_account_id_seq START 1;
CREATE TABLE erp_accounts (
    erp_account_id INTEGER PRIMARY KEY DEFAULT nextval('erp_account_id_seq'),
    erp_account_number VARCHAR UNIQUE NOT NULL,
    erp_account_name VARCHAR NOT NULL,
    normalized_erp_account_name VARCHAR NOT NULL,
    billing_zip VARCHAR,
    billing_state VARCHAR,
    billing_city VARCHAR,
    first3_token VARCHAR NOT NULL 
);

-- ====================== RELATIONSHIPS =========================

CREATE SEQUENCE erp_to_parent_match_seq START 1;
CREATE TABLE erp_account_to_parent_account_map (
    relationship_id INTEGER DEFAULT nextval('erp_to_parent_match_seq'),
    erp_account_id INTEGER PRIMARY KEY REFERENCES erp_accounts(erp_account_id),
    parent_account_id INTEGER NOT NULL REFERENCES parent_accounts(parent_account_id)
);

CREATE SEQUENCE erp_to_parent_mismatch_seq START 1;
CREATE TABLE mismatch_erp_account_to_parent_account_map (
  relationship_id INTEGER DEFAULT nextval('erp_to_parent_mismatch_seq'),
  erp_account_id INTEGER NOT NULL REFERENCES erp_accounts(erp_account_id),
  parent_account_id INTEGER NOT NULL REFERENCES parent_accounts(parent_account_id),
  PRIMARY KEY (erp_account_id, parent_account_id)
);

CREATE SEQUENCE vendor_customer_to_parent_match_seq START 1;
CREATE TABLE vendor_customer_to_parent_account_map (
    relationship_id INTEGER DEFAULT nextval('vendor_customer_to_parent_match_seq'),
    vendor_customer_id INTEGER PRIMARY KEY REFERENCES vendor_customers(vendor_customer_id),
    parent_account_id INTEGER REFERENCES parent_accounts(parent_account_id)
);

CREATE SEQUENCE vendor_customer_to_parent_mismatch_seq START 1;
CREATE TABLE mismatch_vendor_customer_to_parent_account_map (
    relationship_id INTEGER DEFAULT nextval('vendor_customer_to_parent_mismatch_seq'),
    vendor_customer_id INTEGER REFERENCES vendor_customers(vendor_customer_id),
    parent_account_id INTEGER REFERENCES parent_accounts(parent_account_id),
    PRIMARY KEY (vendor_customer_id, parent_account_id)
);

CREATE SEQUENCE vendor_customer_to_erp_match_seq START 1;
CREATE TABLE vendor_customer_to_erp_account_map (
    relationship_id INTEGER DEFAULT nextval('vendor_customer_to_erp_match_seq'),
    vendor_customer_id INTEGER PRIMARY KEY REFERENCES vendor_customers(vendor_customer_id),
    erp_account_id INTEGER REFERENCES erp_accounts(erp_account_id)
);

CREATE SEQUENCE vendor_customer_to_erp_account_mismatch_seq START 1;
CREATE TABLE mismatch_vendor_customer_to_erp_account_map (
    relationship_id INTEGER DEFAULT nextval('vendor_customer_to_erp_account_mismatch_seq'),
    vendor_customer_id INTEGER REFERENCES vendor_customers(vendor_customer_id),
    erp_account_id INTEGER REFERENCES erp_accounts(erp_account_id),
    PRIMARY KEY (vendor_customer_id, erp_account_id)
);


