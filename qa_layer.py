import datetime
import subprocess
import sys

try:
    import psycopg2
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
    import psycopg2

def run_quality_assurance():
    print("Executing Phase 5: Quality Assurance Layer Pipeline...")
    
    try:
        connection = psycopg2.connect(
            "postgresql://neondb_owner:npg_AYovDKM7VL8s@ep-mute-tooth-adtz6q0f.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
        )
        cursor = connection.cursor()

        # Step 1: Fetch all signals currently sitting in raw storage
        cursor.execute("SELECT id, ticker, signal_type, transaction_date, amount FROM raw_signals;")
        all_signals = cursor.fetchall()

        if not all_signals:
            print("QA Layer canceled: No raw signals found to verify.")
            return

        today = datetime.date.today()
        ninety_days_ago = today - datetime.timedelta(days=90)
        
        cleaned_signals = []
        duplicate_count = 0
        stale_count = 0
        
        # Track unique combinations to catch double-filings or duplicates
        seen_signals = set()

        for signal_id, ticker, signal_type, trans_date, amount in all_signals:
            # --- RULES ENGINE 1: FILTER OUT STALE DATA ---
            if trans_date < ninety_days_ago:
                stale_count += 1
                continue
            
            # --- RULES ENGINE 2: REMOVE DUPLICATE FILINGS ---
            # Create a unique fingerprint for this transaction
            signal_fingerprint = (ticker, signal_type, trans_date, amount)
            
            if signal_fingerprint in seen_signals:
                duplicate_count += 1
                continue
                
            seen_signals.add(signal_fingerprint)
            cleaned_signals.append({
                "ticker": ticker,
                "type": signal_type,
                "date": trans_date,
                "amount": amount
            })

        print(f"QA Processing complete: Removed {duplicate_count} duplicates and {stale_count} stale rows.")
        print(f"{len(cleaned_signals)} verified high-confidence signals are cleared for analytical routing.")
        
        cursor.close()
        connection.close()
        return cleaned_signals

    except Exception as error:
        print(f"QA Pipeline error: {error}")

if __name__ == "__main__":
    run_quality_assurance()
