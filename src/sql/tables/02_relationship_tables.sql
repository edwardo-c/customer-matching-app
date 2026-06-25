CREATE SEQUENCE accepted_erp_account_to_parent_account_seq START 1;
CREATE TABLE accepted_erp_account_to_parent_account_map (
    relationship_id INTEGER DEFAULT nextval('accepted_erp_account_to_parent_account_seq'),
    erp_account_id INTEGER PRIMARY KEY REFERENCES erp_accounts(erp_account_id),
    parent_account_id INTEGER NOT NULL REFERENCES parent_accounts(parent_account_id)
);

CREATE SEQUENCE rejected_erp_account_to_parent_account_seq START 1;
CREATE TABLE rejected_erp_account_to_parent_account_map (
  relationship_id INTEGER DEFAULT nextval('rejected_erp_account_to_parent_account_seq'),
  erp_account_id INTEGER NOT NULL REFERENCES erp_accounts(erp_account_id),
  parent_account_id INTEGER NOT NULL REFERENCES parent_accounts(parent_account_id),
  PRIMARY KEY (erp_account_id, parent_account_id)
);

CREATE SEQUENCE accepted_vendor_customer_to_parent_account_seq START 1;
CREATE TABLE accepted_vendor_customer_to_parent_account_map (
    relationship_id INTEGER DEFAULT nextval('accepted_vendor_customer_to_parent_account_seq'),
    vendor_customer_id INTEGER PRIMARY KEY REFERENCES vendor_customers(vendor_customer_id),
    parent_account_id INTEGER REFERENCES parent_accounts(parent_account_id)
);

CREATE SEQUENCE rejected_vendor_customer_to_parent_account_seq START 1;
CREATE TABLE rejected_vendor_customer_to_parent_account_map (
    relationship_id INTEGER DEFAULT nextval('rejected_vendor_customer_to_parent_account_seq'),
    vendor_customer_id INTEGER REFERENCES vendor_customers(vendor_customer_id),
    parent_account_id INTEGER REFERENCES parent_accounts(parent_account_id),
    PRIMARY KEY (vendor_customer_id, parent_account_id)
);

CREATE SEQUENCE accepted_vendor_customer_to_erp_account_seq START 1;
CREATE TABLE accepted_vendor_customer_to_erp_account_map (
    relationship_id INTEGER DEFAULT nextval('accepted_vendor_customer_to_erp_account_seq'),
    vendor_customer_id INTEGER PRIMARY KEY REFERENCES vendor_customers(vendor_customer_id),
    erp_account_id INTEGER REFERENCES erp_accounts(erp_account_id)
);

CREATE SEQUENCE rejected_vendor_customer_to_erp_account_seq START 1;
CREATE TABLE rejected_vendor_customer_to_erp_account_map (
    relationship_id INTEGER DEFAULT nextval('rejected_vendor_customer_to_erp_account_seq'),
    vendor_customer_id INTEGER REFERENCES vendor_customers(vendor_customer_id),
    erp_account_id INTEGER REFERENCES erp_accounts(erp_account_id),
    PRIMARY KEY (vendor_customer_id, erp_account_id)
);

CREATE SEQUENCE accepted_vendor_customer_sibling_seq START 1;
CREATE TABLE accepted_vendor_siblings_map (
  relationship_id INTEGER DEFAULT nextval('accepted_vendor_customer_sibling_seq'),
  left_vendor_customer_id INTEGER REFERENCES vendor_customers(vendor_customer_id),
  right_vendor_customer_id INTEGER REFERENCES vendor_customers(vendor_customer_id),
  PRIMARY KEY (left_vendor_customer_id, right_vendor_customer_id)
);

CREATE SEQUENCE rejected_vendor_customer_sibling_seq START 1;
CREATE TABLE rejected_vendor_customer_sibling_map (
  relationship_id INTEGER DEFAULT nextval('rejected_vendor_customer_sibling_seq'),
  left_vendor_customer_id INTEGER REFERENCES vendor_customers(vendor_customer_id),
  right_vendor_customer_id INTEGER REFERENCES vendor_customers(vendor_customer_id),
  PRIMARY KEY (left_vendor_customer_id, right_vendor_customer_id)
);

