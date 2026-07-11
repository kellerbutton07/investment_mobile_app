import datetime
import subprocess
import sys

try:
    import psycopg2
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
    import psycopg2

def build_institutional_roster():
    print("Connecting to Neon Cloud Data Engine... Architecting Whale Registry...")
    
    try:
        connection = psycopg2.connect(
            host="ep-mute-tooth-adtz6q0f.c-2.us-east-1.aws.neon.tech",
            port="5432", user="neondb_owner", password="npg_AYovDKM7VL8s", database="neondb", sslmode="require"
        )
        cursor = connection.cursor()

        # Table 1: Master Trader Profiles (Returns & Bios)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trader_registry (
                trader_id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                category VARCHAR(50) NOT NULL,
                annual_return NUMERIC NOT NULL,
                trading_style VARCHAR(100) NOT NULL,
                biography TEXT NOT NULL
            );
        """)

        # Table 2: Transaction History Tables (Mapped back to Trader Names)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS super_investor_history (
                id SERIAL PRIMARY KEY,
                investor_name VARCHAR(100) NOT NULL,
                ticker VARCHAR(10) NOT NULL,
                transaction_type VARCHAR(20) NOT NULL,
                transaction_date DATE NOT NULL,
                dollar_value NUMERIC NOT NULL,
                research_insight TEXT NOT NULL
            );
        """)
        
        cursor.execute("TRUNCATE TABLE trader_registry RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE TABLE super_investor_history;")

        # --- SEEDING EXPANSIVE ROSTER PROFILES ---
        traders = [
            ("Nancy Pelosi (Capitol)", "Political Insider", 31.4, "Policy Momentum & Deep Tech Call Options", 
             "Representative Nancy Pelosi's family portfolio has historically drawn significant attention for perfectly timed corporate equity executions, particularly tracking semiconductor and enterprise compute frameworks right before large federal subsidy implementations."),
            
            ("Michael Burry (Scion)", "Activist Hedge Fund", 24.8, "Contrarian Deep Value & Structural Shorts", 
             "Famed for predicting the 2008 subprime mortgage collapse, Dr. Michael Burry runs highly concentrated, rapid-rotation portfolio plays targeting technically beaten-down equities experiencing extreme ad-revenue or cash-flow metric compression."),
            
            ("Warren Buffett (Berkshire)", "Macro Legend", 19.5, "Moat-Driven Long Term Value Accumulation", 
             "The Oracle of Omaha utilizes a foundational value architecture. He screens for businesses displaying bulletproof operational moats, highly predictable consumer pricing power, defensive margins, and generational shares-buyback programs."),
            
            ("Bill Ackman (Pershing Square)", "Activist Hedge Fund", 22.1, "Concentrated Operational Activism", 
             "Ackman runs a high-conviction, single-digit line portfolio strategy. He targets scale-heavy consumer franchises, using media presence and structural boardroom interventions to optimize operational cash generation loops."),
            
            ("Stanley Druckenmiller (Duquesne)", "Macro Legend", 28.3, "Cross-Asset Macro Liquidity Trends", 
             "George Soros' former chief strategist, Druckenmiller tracks global thematic macro shifts. He rotates multi-million dollar allocations rapidly into equities displaying severe underlying sector growth structural acceleration patterns."),
            
            ("Jensen Huang (NVIDIA CEO)", "Tech Corporate Insider", 42.6, "Executive Stock Compensation Liquidations", 
             "As the foundational pioneer of generative compute infrastructure, Huang's public transactional filings represent automated regulatory programmatic liquidity adjustments alongside strategic confidence matrix signals."),
            
            ("Mark Zuckerberg (Meta CEO)", "Tech Corporate Insider", 38.2, "Open Market Strategic Reinvestments", 
             "Zuckerberg's market execution strategies reflect direct internal forecasting insights regarding digital media spatial networks, ad-spend demand curves, and next-gen hardware infrastructure integration timelines.")
        ]

        for name, cat, ret, style, bio in traders:
            cursor.execute("""
                INSERT INTO trader_registry (name, category, annual_return, trading_style, biography)
                VALUES (%s, %s, %s, %s, %s);
            """, (name, cat, ret, style, bio))

        # --- SEEDING CORRESPONDING INSTITUTIONAL LEDGERS ---
        trades = [
            ("Nancy Pelosi (Capitol)", "NVDA", "Buy", "2026-03-22", 5000000, "Exercised deep tech call options."),
            ("Nancy Pelosi (Capitol)", "AAPL", "Buy", "2026-05-18", 2500000, "Accumulated core consumer tech blocks."),
            ("Michael Burry (Scion)", "META", "Buy", "2026-01-20", 8500000, "Deep value rotation play."),
            ("Michael Burry (Scion)", "MSFT", "Sell", "2026-04-14", 6200000, "Exited position over cap-ex expansion fatigue."),
            ("Warren Buffett (Berkshire)", "AAPL", "Buy", "2026-02-15", 12500000, "Increased structural anchor position."),
            ("Warren Buffett (Berkshire)", "COST", "Buy", "2026-05-10", 4200000, "Added defensive retail margin plays."),
            ("Bill Ackman (Pershing Square)", "COST", "Buy", "2026-03-11", 11000000, "High-conviction consumer moat play."),
            ("Stanley Druckenmiller (Duquesne)", "NVDA", "Buy", "2026-02-28", 14500000, "Rode cross-asset AI liquidity wave."),
            ("Stanley Druckenmiller (Duquesne)", "MSFT", "Buy", "2026-05-02", 9000000, "Positioned into cloud scaling infrastructure."),
            ("Jensen Huang (NVIDIA CEO)", "NVDA", "Sell", "2026-05-30", 14000000, "Programmatic Rule 10b5-1 executive distribution."),
            ("Mark Zuckerberg (Meta CEO)", "META", "Buy", "2026-06-15", 9200000, "Open market accumulation filing.")
        ]

        for investor, ticker, t_type, date_str, amt, notes in trades:
            c_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            cursor.execute("""
                INSERT INTO super_investor_history (investor_name, ticker, transaction_type, transaction_date, dollar_value, research_insight)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (investor, ticker, t_type, c_date, amt, notes))

        connection.commit()
        print("Roster & Ledgers synced flawlessly to the Neon Cloud Repository.")
        cursor.close()
        connection.close()

    except Exception as error:
        print(f"Database setup error: {error}")

if __name__ == "__main__":
    build_institutional_roster()
