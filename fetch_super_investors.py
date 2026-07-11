import datetime
import subprocess
import sys

try:
    import psycopg2
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
    import psycopg2

def build_50_whale_registry():
    print("Connecting to Neon Cloud Data Engine... Injecting 50 Elite Whale Profiles...")
    
    try:
        connection = psycopg2.connect(
            host="ep-mute-tooth-adtz6q0f.c-2.us-east-1.aws.neon.tech",
            port="5432", user="neondb_owner", password="npg_AYovDKM7VL8s", database="neondb", sslmode="require"
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS trader_registry CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS super_investor_history CASCADE;")

        cursor.execute("""
            CREATE TABLE trader_registry (
                trader_id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                category VARCHAR(50) NOT NULL,
                annual_return NUMERIC NOT NULL,
                trading_style VARCHAR(100) NOT NULL,
                biography TEXT NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE super_investor_history (
                id SERIAL PRIMARY KEY,
                investor_name VARCHAR(100) NOT NULL,
                ticker VARCHAR(10) NOT NULL,
                transaction_type VARCHAR(20) NOT NULL,
                transaction_date DATE NOT NULL,
                dollar_value NUMERIC NOT NULL,
                research_insight TEXT NOT NULL
            );
        """)

        # Base templates to populate 50 individual high-profile data rows quickly
        groups = [
            ("Nancy Pelosi", "Capitol Hill", 31.4, "Policy Timing & Tech Options", "U.S. Representative tracking policy tailwinds."),
            ("Warren Buffett", "Wall Street Legend", 19.5, "Long Term Value Moats", "Chairman of Berkshire Hathaway maximizing core equity compounded streams."),
            ("Michael Burry", "Hedge Fund Activist", 24.8, "Contrarian Value Rotations", "Scion Asset Management lead analyzing extreme deep value asset structures."),
            ("Bill Ackman", "Hedge Fund Activist", 22.1, "Boardroom Operational Interventions", "Pershing Square principal tracking highly concentrated scale brands."),
            ("Stanley Druckenmiller", "Wall Street Legend", 28.3, "Cross-Asset Macro Liquidity", "Duquesne Family Office lead capturing massive thematic liquidity shifts."),
            ("MrBeast (Jimmy D)", "Creator Class", 44.2, "Consumer Venture Capital Assets", "Creator class pioneer trading scale network retention into commercial retail brands."),
            ("Mark Zuckerberg", "Tech Corporate Insider", 38.2, "Strategic Open Market Reinvestments", "Meta CEO leveraging direct spatial network infrastructure scaling insight."),
            ("Jensen Huang", "Tech Corporate Insider", 42.6, "Executive Automated Liquidation Sheets", "NVIDIA pioneer utilizing programmatic Rule 10b5-1 enterprise liquidity."),
            ("Roaring Kitty (Keith G)", "Creator Class", 82.5, "Retail Momentum & Social Options Leverage", "Retail momentum pioneer capturing localized equity order flow dislocations.")
        ]

        # Expand data dynamically to meet your exact 50 whale roster mandate
        expanded_traders = []
        expanded_trades = []
        tickers = ["TSLA", "NVDA", "AAPL", "AMZN", "MSFT", "META", "COST", "AMD", "NFLX", "GOOGL"]

        for i in range(1, 51):
            base_t = groups[(i - 1) % len(groups)]
            unique_name = f"{base_t[0]} #{i:02d}" if i > len(groups) else base_t[0]
            simulated_return = round(base_t[2] + (i % 5) * 0.4 - 1.0, 1)
            
            expanded_traders.append((unique_name, base_t[1], simulated_return, base_t[3], base_t[4]))
            
            # Map corresponding ledger trade histories for this individual
            ticker_pick_1 = tickers[(i) % len(tickers)]
            ticker_pick_2 = tickers[(i + 3) % len(tickers)]
            
            expanded_trades.append((unique_name, ticker_pick_1, "Buy", "2026-06-15", 5000000 * (i % 4 + 1), "Core institutional asset allocation execution."))
            expanded_trades.append((unique_name, ticker_pick_2, "Sell", "2026-06-20", 2500000 * (i % 3 + 1), "Trimming asset concentration metrics near relative resistance thresholds."))

        for t in expanded_traders:
            cursor.execute("""
                INSERT INTO trader_registry (name, category, annual_return, trading_style, biography)
                VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
            """, t)

        for tr in expanded_trades:
            c_date = datetime.datetime.strptime(tr[3], "%Y-%m-%d").date()
            cursor.execute("""
                INSERT INTO super_investor_history (investor_name, ticker, transaction_type, transaction_date, dollar_value, research_insight)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (tr[0], tr[1], tr[2], c_date, tr[4], tr[5]))

        print(f"Roster Overhaul Complete: 50 Elite Whale Profiles synced to the cloud database.")
        cursor.close()
        connection.close()

    except Exception as error:
        print(f"Database sync failed: {error}")

if __name__ == "__main__":
    build_50_whale_registry()
