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
    raw_billing_zip VARCHAR,
    normalized_billing_zip VARCHAR,
    billing_state VARCHAR,
    period_date DATE,
    first3_token VARCHAR NOT NULL 
);

CREATE SEQUENCE erp_account_id_seq START 1;
CREATE TABLE erp_accounts (
    erp_account_id INTEGER PRIMARY KEY DEFAULT nextval('erp_account_id_seq'),
    erp_account_number VARCHAR UNIQUE NOT NULL,
    erp_account_name VARCHAR NOT NULL,
    normalized_erp_account_name VARCHAR NOT NULL,
    raw_billing_zip VARCHAR,
    normalized_billing_zip VARCHAR,
    billing_state VARCHAR,
    billing_city VARCHAR,
    first3_token VARCHAR NOT NULL 
);