from typing import Protocol

class RelationshipMapTable(Protocol):
    TABLE: str
    SOURCE: str
    TARGET: str

class VendorCustomerToParentMap:
    TABLE = "vendor_customer_to_parent_account_map"

    VENDOR_CUSTOMER_ID = "vendor_customer_id"
    PARENT_ACCOUNT_ID = "parent_account_id"

    TARGET = "parent_account_id"
    SOURCE = "vendor_customer_id"

class RejectedVendorCustomerToParentMap:
    TABLE = "mismatch_vendor_customer_to_parent_account_map"

    VENDOR_CUSTOMER_ID = "vendor_customer_id"
    PARENT_ACCOUNT_ID = "parent_account_id"

    TARGET = "parent_account_id"
    SOURCE = "vendor_customer_id"
