import subprocess
import sys

# Automatically install database connector library if missing
try:
    import psycopg2
except ImportError:
    print("Installing required database tools... Please wait.")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
    import psycopg2

def initialize_database():
    try:
        # Connect to your local PostgreSQL installation
        connection = psycopg2.connect(
            "postgresql://neondb_owner:npg_AYovDKM7VL8s@ep-mute-tooth-adtz6q0f.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
        )
        cursor = connection.cursor()

        # Create Companies Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                ticker VARCHAR(10) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL
            );
        """)

        # Create Scores Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id SERIAL PRIMARY KEY,
                ticker VARCHAR(10) NOT NULL,
                date DATE NOT NULL,
                final_score INT NOT NULL,
                confidence INT NOT NULL,
                reasons TEXT NOT NULL
            );
        """)

        # Create Raw Signals Table (insider / congressional activity)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw_signals (
                id SERIAL PRIMARY KEY,
                ticker VARCHAR(10),
                signal_type VARCHAR(50),
                transaction_date DATE,
                amount NUMERIC,
                data_source VARCHAR(50)
            );
        """)

        connection.commit()
        print("Success! Your database warehouse tables are live and ready.")
        
        cursor.close()
        connection.close()

    except Exception as error:
        print(f"Error connecting to the database: {error}")
        print("Make sure your Neon cloud database is reachable and sslmode=require is set.")

if __name__ == "__main__":
    initialize_database()
