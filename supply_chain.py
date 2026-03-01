import os
import pandas as pd
from sqlalchemy import create_engine

# --- CONFIG ---
DB_NAME = "supply_chain_db"
DB_USER = "postgres"
DB_PASS = "Sanika123"  # <--- Change this to your real pgAdmin password
DB_HOST = "localhost"
DB_PORT = "5432"

file_path = r'c:\Users\Sanika\SQL_project\DataCoSupplyChainDataset.csv'

# THE TRY BLOCK STARTS HERE
try:
    print("⏳ Step 1: Loading CSV into memory...")
    df = pd.read_csv(file_path, encoding='ISO-8859-1')
    
    # Clean column names for SQL compatibility
    df.columns = [c.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_') for c in df.columns]

    print("🔗 Step 2: Connecting to PostgreSQL...")
    conn_str = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(conn_str)

    print("🚀 Step 3: Performing Bulk Upload (Please wait ~60 seconds)...")
    # This creates the table and pushes the data
    df.to_sql('stg_supply_chain', engine, if_exists='replace', index=False, chunksize=5000)
    
    print("✅ Step 4: Verifying Data...")
    with engine.connect() as conn:
        from sqlalchemy import text
        result = conn.execute(text("SELECT COUNT(*) FROM stg_supply_chain")).fetchone()
        print(f"🌟 SUCCESS! {result[0]} rows are now LIVE in the database.")

# THE EXCEPT BLOCK FIXES YOUR SYNTAX ERROR
except Exception as e:
    print(f"❌ ERROR OCCURRED: {e}")

# THE FINALLY BLOCK (Optional but professional)
finally:
    print("🏁 Process finished.")