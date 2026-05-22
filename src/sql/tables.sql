CREATE SEQUENCE batch_seq START 1;
CREATE TABLE batches (
    batch_id INTEGER PRIMARY KEY DEFAULT nextval('batch_seq'),
    rows_added BIGINT NOT NULL,
    target_table VARCHAR NOT NULL,
    upload_datetime TIMESTAMP
);

-- ENTITIES --
CREATE SEQUENCE vendor_customer_id_seq START 1;
CREATE TABLE vendor_customers (
    vendor_customer_id INTEGER PRIMARY KEY DEFAULT nextval('vendor_customer_id_seq'),
    vendor_name VARCHAR,
    raw_vendor_customer_name VARCHAR,
    normalized_vendor_customer_name VARCHAR NOT NULL,
    vendor_customer_billing_zip VARCHAR,
    vendor_customer_billing_state VARCHAR,
    vendor_customer_billing_city VARCHAR,
    vendor_customer_first3_token VARCHAR
);

CREATE SEQUENCE erp_account_id_seq START 1;
CREATE TABLE erp_accounts (
    erp_account_id INTEGER PRIMARY KEY DEFAULT nextval('erp_account_id_seq'),
    erp_account_number VARCHAR UNIQUE NOT NULL,
    erp_account_name VARCHAR NOT NULL,
    normalized_erp_account_name VARCHAR NOT NULL,
    erp_account_billing_zip VARCHAR,
    erp_account_billing_state VARCHAR,
    erp_account_billing_city VARCHAR,
    erp_name_first3_token VARCHAR
);

CREATE SEQUENCE parent_account_seq START 1;
CREATE TABLE parent_accounts (
    parent_account_id INTEGER PRIMARY KEY DEFAULT nextval('parent_account_seq'),
    parent_account_name VARCHAR UNIQUE NOT NULL,
    normalized_parent_name VARCHAR UNIQUE NOT NULL,
    parent_name_first3_token VARCHAR
);

-- ==================== RELATIONSHIPS ====================

CREATE TABLE vendor_customer_to_erp_account_map (
    vendor_customer_id INTEGER PRIMARY KEY REFERENCES vendor_customers(vendor_customer_id),
    erp_account_id INTEGER NOT NULL REFERENCES erp_accounts(erp_account_id)
);

CREATE SEQUENCE vendor_customer_to_erp_account_seq START 1;

CREATE TABLE vendor_customer_to_erp_account_candidate_map (    
    candidate_id INTEGER PRIMARY KEY DEFAULT nextval('vendor_customer_to_erp_account_seq'),
    vendor_customer_id INTEGER NOT NULL REFERENCES vendor_customers(vendor_customer_id),
    erp_account_id INTEGER NOT NULL REFERENCES erp_accounts(erp_account_id),
    score DECIMAL(5,2),
    status VARCHAR CHECK(status IN ('pending', 'accepted', 'rejected')),
    batch_id INTEGER NOT NULL REFERENCES batches(batch_id)
);

-- =======================================================


















-- ==================== CONFIRMED RELATIONSHIPS ====================
-- CREATE TABLE vendor_customer_to_parent_account_map (
--     vendor_customer_id INTEGER PRIMARY KEY REFERENCES vendor_customers(vendor_customer_id),
--     parent_account_id INTEGER REFERENCES parent_accounts(parent_account_id)
-- );



-- CREATE TABLE erp_account_to_parent_account_map (
--     erp_account_id INTEGER PRIMARY KEY REFERENCES erp_accounts(erp_account_id),
--     parent_account_id INTEGER NOT NULL REFERENCES parent_accounts(parent_account_id)
-- );