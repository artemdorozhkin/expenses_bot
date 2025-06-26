import os
import sys


DB_FILE = "db/expenses.db"
try:
    admin_id = os.getenv("ADMIN")
    if not admin_id:
        raise ValueError()
    ADMIN_ID = int(admin_id)
except ValueError:
    ADMIN_ID = -1
    print("ERR: you need specify ADMIN env variable")
    sys.exit(1)
