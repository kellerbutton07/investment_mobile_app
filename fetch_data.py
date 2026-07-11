import subprocess
import sys

# Automatically install network utility libraries if missing
try:
    import requests
except ImportError:
    print("Installing web tools... Please wait.")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

try:
    import psycopg2
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
    import psycopg2

def load_initial_companies():
    # A standard starting list of tech companies to build your system around
    sample_stocks = [
        {"ticker": "AAPL", "name": "Apple Inc."},
        {"ticker": "MSFT", "name": "Microsoft Corporation"},
        {"ticker": "NVDA", "name": "NVIDIA Corporation"},
        {"ticker": "META", "name": "Meta Platforms, Inc."},
        {"ticker": "COST", "name": "Costco Wholesale Corporation"}
    ]

    try:
        connection = psycopg2.connect(
            "postgresql://neondb_owner:npg_AYovDKM7VL8s@ep-mute-tooth-adtz6q0f.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
        )
        cursor = connection.cursor()

        for stock in sample_stocks:
            # Insert stocks only if they do not already exist to prevent duplication
            cursor.execute("""
                INSERT INTO companies (ticker, name) 
                VALUES (%s, %s) 
                ON CONFLICT (ticker) DO NOTHING;
            """, (stock["ticker"], stock["name"]))
        
        connection.commit()
        print("Core company profiles loaded into database warehouse.")
        
        cursor.close()
        connection.close()

    except Exception as error:
        print(f"Error loading data: {error}")

if __name__ == "__main__":
    load_initial_companies()
