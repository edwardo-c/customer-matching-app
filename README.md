# Customer Resolution Application

## What Is It
Python & SQL based system to aid in customer relationship heirarchy management
 

## Why It Exists
We recieve sell-thru data monthly from multiple vendors. The customers in those reports
purchase through multiple vendors but each vendor has the customer with different names.
We also have an ERP system with customer and account numbers.
Vendor customers may be ERP customers, ERP customers may have multiple branches,
therefore we need a resolution system to manage Parent Accounts for the analytical layer.

example: 
ABCOM purchases through Vendor A under "Abcom Inc" and "Ab Communications Inc" from Vendor B,
then purchases directly in ERP under "Absolute Communications Inc." 
All of these aliases are under the ABCOM parent account. To have a complete understanding of 
their purchasing, these must all be assigned up to the ABCOM parent account.

This system provides outputs for a human to confirm or deny potential matches to
ERP accounts, Parent accounts, or both.


