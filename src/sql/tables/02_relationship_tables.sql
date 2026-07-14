CREATE SEQUENCE vendor_customer_to_resolved_customer_seq START 1;
CREATE TABLE vendor_customer_to_resolved_customer_map (
    relationship_id INTEGER DEFAULT nextval('vendor_customer_to_resolved_customer_seq'),
    vendor_customer_id INTEGER PRIMARY KEY REFERENCES vendor_customers(vendor_customer_id),
    resolved_customer_id INTEGER REFERENCES resolved_customers(resolved_customer_id)
);

CREATE SEQUENCE rejected_vendor_customer_to_resolved_customer_seq START 1;
CREATE TABLE rejected_vendor_customer_to_resolved_customer_map (
    relationship_id INTEGER DEFAULT nextval('rejected_vendor_customer_to_resolved_customer_seq'),
    vendor_customer_id INTEGER REFERENCES vendor_customers(vendor_customer_id),
    resolved_customer_id INTEGER REFERENCES resolved_customers(resolved_customer_id),
    PRIMARY KEY (vendor_customer_id, resolved_customer_id)
);

CREATE SEQUENCE vendor_customer_sibling_seq START 1;
CREATE TABLE vendor_customer_sibling_map (
  relationship_id INTEGER DEFAULT nextval('vendor_customer_sibling_seq'),
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

