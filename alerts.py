import datetime
import subprocess
import sys

# Auto-verify internet transaction sending tools are installed
try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

try:
    import psycopg2
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
    import psycopg2

# PASTE YOUR COPIED DISCORD OR SLACK WEBHOOK LINK BETWEEN THESE QUOTES:
WEBHOOK_URL = "https://hooks.slack.com/services/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"

def check_and_send_alerts():
    print("Executing Phase 9: Automated Notification System Rules Engine...")
    
    if WEBHOOK_URL == "YOUR_WEBHOOK_URL_HERE" or not WEBHOOK_URL.startswith("http"):
        print("Alert skipped: Please paste a valid Discord/Slack Webhook URL into the script code!")
        return

    today = datetime.date.today()

    try:
        connection = psycopg2.connect(
            "postgresql://neondb_owner:npg_AYovDKM7VL8s@ep-mute-tooth-adtz6q0f.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
        )
        cursor = connection.cursor()

        # Query today's highest-ranking stock scores from your data warehouse
        cursor.execute("""
            SELECT ticker, final_score, confidence, reasons 
            FROM scores 
            WHERE date = %s;
        """, (today,))
        
        todays_scores = cursor.fetchall()
        alerts_triggered = 0

        for ticker, score, confidence, reasons in todays_scores:
            # --- PHASE 9 ALERTER SYSTEM TRIGGER CRITERIA ---
            # Criteria A: Master score crosses the elite 85-point threshold
            # Criteria B: A major political cluster is specifically flagged in research notes
            is_elite_score = score >= 85
            is_congressional_cluster = "verified Congressional buys" in reasons

            if is_elite_score or is_congressional_cluster:
                print(f"Alert condition met for {ticker}! Compiling communication brief...")
                
                # Format a highly polished, clean text notification summary broadcast
                message_body = (
                    f"**QUANT SYSTEM ALERT: TARGET DETECTED**\n"
                    f"**Asset Ticker:** ${ticker}\n"
                    f"**Master Quant Score:** {score} / 100 points\n"
                    f"**Data Confidence Level:** {confidence}%\n"
                    f"**System Research Notes:** {reasons}\n"
                    f"*Action Recommended: Open Core Terminal Dashboard immediately.*"
                )

                # Slack expects "text"; Discord expects "content"
                if "hooks.slack.com" in WEBHOOK_URL:
                    alert_payload = {"text": message_body}
                else:
                    alert_payload = {"content": message_body}
                
                # Fire the text alert out across the web to your device app
                response = requests.post(WEBHOOK_URL, json=alert_payload, timeout=10)
                
                if response.status_code in (200, 204):
                    print(f"Notification message for {ticker} broadcasted successfully!")
                    alerts_triggered += 1
                else:
                    print(f"Failed to send payload link response code: {response.status_code}")

        if alerts_triggered == 0:
            print("No companies breached alert parameters today. Communications silent.")
            
        connection.commit()
        cursor.close()
        connection.close()

    except Exception as error:
        print(f"Alert Engine malfunction: {error}")

if __name__ == "__main__":
    check_and_send_alerts()
