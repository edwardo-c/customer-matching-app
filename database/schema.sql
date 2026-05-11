CREATE TABLE batches (
    batch_id INTEGER PRIMARY KEY,
    source_system VARCHAR NOT NULL,
    source_file VARCHAR,
    target_table VARCHAR NOT NULL CHECK (
        target_table IN ('erp_accounts', 'vendor_customers', 'parent_accounts')
    ),
    
    new_rows_loaded BIGINT NOT NULL,
    rows_overwritten BIGINT NOT NULL,
    status VARCHAR NOT NULL CHECK (status IN ('Success', 'Failed', 'Partial')),
    loaded_at TIMESTAMP NOT NULL,
    loaded_by VARCHAR NOT NULL
);

-- ENTITY TABLES 

CREATE TABLE parent_accounts (
    parent_account_id INTEGER PRIMARY KEY,
    parent_account_name VARCHAR UNIQUE NOT NULL,
    normalized_parent_name VARCHAR UNIQUE NOT NULL,
    status VARCHAR NOT NULL CHECK (status IN ('Active', 'Inactive')),
    batch_id INTEGER REFERENCES batches(batch_id)
);

CREATE TABLE vendor_customers (
    vendor_customer_id INTEGER PRIMARY KEY,
    vendor_name VARCHAR NOT NULL,
    vendor_provided_customer_number VARCHAR,
    raw_customer_name VARCHAR NOT NULL,
    normalized_customer_name VARCHAR NOT NULL,
    billing_zip VARCHAR,
    billing_state VARCHAR,
    billing_city VARCHAR,
    batch_id INTEGER REFERENCES batches(batch_id)
);

CREATE TABLE erp_accounts (
    erp_account_id INTEGER PRIMARY KEY,
    erp_account_number VARCHAR UNIQUE NOT NULL,
    erp_account_name VARCHAR NOT NULL,
    normalized_erp_account_name VARCHAR NOT NULL,
    billing_zip VARCHAR,
    billing_state VARCHAR,
    billing_city VARCHAR,
    status VARCHAR NOT NULL CHECK (status IN ('Active', 'On Hold', 'Credit Hold', 'One-Time', 'Inactive')),
    batch_id INTEGER REFERENCES batches(batch_id)
);

-- ENTITY RELATIONSHIP TABLES 

CREATE TABLE erp_account_parent_map (
    erp_account_id INTEGER PRIMARY KEY REFERENCES erp_accounts(erp_account_id),
    parent_account_id INTEGER NOT NULL REFERENCES parent_accounts(parent_account_id),
    status VARCHAR NOT NULL CHECK (status IN ('Active', 'Inactive')),
    batch_id INTEGER REFERENCES batches(batch_id)
);

CREATE TABLE vendor_customer_erp_map (
    vendor_customer_id INTEGER PRIMARY KEY REFERENCES vendor_customers(vendor_customer_id),
    erp_account_id INTEGER REFERENCES erp_accounts(erp_account_id),
    status VARCHAR NOT NULL CHECK (status IN ('Active', 'Inactive')),
    batch_id INTEGER REFERENCES batches(batch_id)
);

CREATE TABLE vendor_customer_parent_map (
    vendor_customer_id INTEGER PRIMARY KEY REFERENCES vendor_customers(vendor_customer_id),
    parent_account_id INTEGER REFERENCES parent_accounts(parent_account_id),
    status VARCHAR NOT NULL CHECK (status IN ('Active', 'Inactive')),
    batch_id INTEGER REFERENCES batches(batch_id)
);

