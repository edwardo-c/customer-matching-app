CREATE SEQUENCE resolved_customer_seq START 1;
CREATE TABLE resolved_customers (
    resolved_customer_id INTEGER PRIMARY KEY DEFAULT nextval('resolved_customer_seq'),
    resolved_customer_name VARCHAR UNIQUE NOT NULL,
    normalized_resolved_customer_name VARCHAR UNIQUE NOT NULL,
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