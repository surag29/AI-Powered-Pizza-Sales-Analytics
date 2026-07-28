"""
app.py
Connects to MySQL, runs every query defined in queries.py,
and saves the results to results.json for the AI insights
script and the Streamlit dashboard to use.

To add a new query: edit queries.py, not this file.
"""

import json
import os
from datetime import datetime

import mysql.connector
from dotenv import load_dotenv

from queries import QUERIES

# ---------- 1. CONNECT TO MYSQL ----------
load_dotenv()  # reads .env in the same folder

DB_PASSWORD = os.getenv("DB_PASSWORD")
if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD not found. Check your .env file.")

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=DB_PASSWORD,
    database=os.getenv("DB_NAME", "pizzahut")
)

cursor = connection.cursor()


# ---------- 2. HELPER FUNCTION ----------
def run_query(sql):
    """Executes a query and returns rows + column names in a clean shape."""
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    # Single value (1 row, 1 column)
    if len(rows) == 1 and len(columns) == 1:
        return rows[0][0]

    # Single row, multiple columns -> dict
    if len(rows) == 1:
        return dict(zip(columns, rows[0]))

    # Multiple rows -> list of dicts
    return [dict(zip(columns, row)) for row in rows]


# ---------- 3. RUN EVERY QUERY FROM queries.py ----------
results = {}

for name, sql in QUERIES.items():
    try:
        results[name] = run_query(sql)
        print(f"✅ {name}: {results[name]}")
    except Exception as e:
        print(f"❌ Failed on '{name}': {e}")
        results[name] = None


# ---------- 4. SAVE RESULTS TO A FILE ----------
output = {
    "generated_at": datetime.now().isoformat(),
    "results": results
}

with open("results.json", "w") as f:
    json.dump(output, f, indent=4, default=str)

print(f"\n📁 All {len(QUERIES)} query results saved to results.json")


# ---------- 5. CLEAN UP ----------
cursor.close()
connection.close()