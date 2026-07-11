import subprocess
import sys

try:
    import streamlit as st
    import pandas as pd
    import feedparser
    import yfinance as yf
    import requests
    import g4f
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit pandas feedparser yfinance requests g4f"])
    import streamlit as st
    import pandas as pd
    import feedparser
    import yfinance as yf
    import requests
    import g4f

try:
    import psycopg2
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
    import psycopg2

st.set_page_config(page_title="AlphaQuant Core Terminal", layout="wide", initial_sidebar_state="collapsed")

# 🏛️ INSTITUTIONAL SLATE DESIGN ENGINE OVERRIDES
st.markdown("""
    <style>
    .stApp { background-color: #0a0d14; }
    .main { background-color: #0a0d14; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    
    h1 { color: #f4f4f0; font-family: 'Inter', system-ui, sans-serif; font-weight: 700; font-size: 1.8rem; letter-spacing: -0.04rem; margin-top: 5px; }
    h2, h3 { color: #e2e8f0; font-family: 'Inter', system-ui, sans-serif; font-weight: 600; letter-spacing: -0.02rem; }
    p, span, label { color: #8a99ad !important; font-family: 'Inter', sans-serif; }
    [data-testid="stMetricValue"] { color: #f4f4f0 !important; font-family: 'Inter', sans-serif; font-weight: 700; font-size: 1.5rem !important; }
    
    .quiver-container { background-color: #0e121a; border: 1px solid #1a1f2c; border-radius: 8px; padding: 15px; margin-bottom: 15px; }
    .bio-card { background-color: #0e121a; border-left: 4px solid #f4f4f0; border-top: 1px solid #1a1f2c; border-right: 1px solid #1a1f2c; border-bottom: 1px solid #1a1f2c; border-radius: 0 8px 8px 0; padding: 15px; margin-top: 10px; }
    .news-box { border-bottom: 1px solid #1a1f2c; padding: 12px 0; }
    .stDataFrame { border: 1px solid #1a1f2c; border-radius: 8px; overflow: hidden; background-color: #0e121a; }
    
    /* Premium Responsive Top Segment Navigation Tabs */
    div.stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: space-around;
        background-color: #0e121a;
        border: 1px solid #1a1f2c;
        border-radius: 10px;
        padding: 4px;
        margin-bottom: 15px;
    }
    div.stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #8a99ad !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 8px 10px;
        border-radius: 6px;
    }
    div.stTabs [aria-selected="true"] { background-color: #1a1f2c !important; color: #f4f4f0 !important; }
    div.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# Secure cloud gateway cluster configurations
if "postgres" in st.secrets:
    db_secrets = st.secrets["postgres"]
    host = db_secrets["host"]
    password = db_secrets["password"]
else:
    host = "ep-mute-tooth-adtz6q0f.c-2.us-east-1.aws.neon.tech"
    password = "npg_AYovDKM7VL8s"

connection = psycopg2.connect(host=host, port="5432", user="neondb_owner", password=password, database="neondb", sslmode="require")

# Dictionary mapping common business company names directly onto core stock ticker tickers
company_ticker_map = {
    "TESLA": "TSLA", "ELON MUSK": "TSLA", "NVIDIA": "NVDA", "JENSEN HUANG": "NVDA",
    "APPLE": "AAPL", "IPHONE": "AAPL", "AMAZON": "AMZN", "JEFF BEZOS": "AMZN",
    "MICROSOFT": "MSFT", "BILL GATES": "MSFT", "META": "META", "FACEBOOK": "META",
    "MARK ZUCKERBERG": "META", "COSTCO": "COST", "AMD": "AMD", "NETFLIX": "NFLX",
    "GOOGLE": "GOOGL", "ALPHABET": "GOOGL"
}

# Fetch unique whale tracking lists
cursor = connection.cursor()
try:
    cursor.execute("SELECT name FROM trader_registry ORDER BY annual_return DESC;")
    whale_names_list = [row[0] for row in cursor.fetchall()]
except Exception:
    whale_names_list = ["Nancy Pelosi", "Warren Buffett", "Michael Burry", "Bill Ackman", "Stanley Druckenmiller"]
cursor.close()

# 📱 FIVE SECTOR RESPONSIVE SEGMENT TOUCH NAVIGATION TABS INTERFACE
tab_explore, tab_signals, tab_whales, tab_news, tab_help = st.tabs([
    "🔍 EXPLORE",
    "📈 SIGNALS",
    "🐋 INVESTORS",  # Dedicated selection page
    "📰 READ",
    "❓ HELP"
])

# ----------------- CHANNELS DISPLAY -----------------

with tab_explore:
    st.markdown('<div class="quiver-container"><h1>🔍 Market Discovery Explorer</h1><p style="color: #8a99ad; margin:0;">Search global financial registries by typing either Ticker Symbols or Company Names</p></div>', unsafe_allow_html=True)

    # ADVANCED SEARCH CONSOLE INPUT
    search_input = st.text_input("ENTER TICKER OR COMPANY IDENTITY (e.g., TSLA, Apple, Nvidia, Costco, Google):", value="TSLA", key="univ_search_input").upper().strip()

    # Intelligence mapper routing translation logic
    target_ticker = search_input
    for key, value in company_ticker_map.items():
        if key in search_input:
            target_ticker = value
            break

    if target_ticker:
        try:
            ticker_obj = yf.Ticker(target_ticker)
            ticker_history = ticker_obj.history(period="1mo", interval="1d")
            ticker_info = ticker_obj.info

            if not ticker_history.empty:
                comp_name = ticker_info.get("longName", f"{target_ticker} Equity Profile")
                price_now = ticker_history["Close"].iloc[-1]
                price_start = ticker_history["Close"].iloc[0]
                net_change_pct = ((price_now - price_start) / price_start) * 100
                chart_color = "#10b981" if price_now >= price_start else "#ef4444"

                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.metric("Company Asset Verified", comp_name)
                with col_m2:
                    st.metric(f"Ticker: ${target_ticker} (30-Day Trend)", f"${price_now:.2f}", f"{net_change_pct:+.2f}%")

                st.line_chart(pd.DataFrame({"Price ($)": ticker_history["Close"]}), color=chart_color)
            else:
                st.warning("Unable to match record for input string. Verify capitalization syntax rules.")
        except Exception:
            st.error("Market data feeds down or processing throttle active.")

with tab_signals:
    st.markdown('<div class="quiver-container"><h1>⚡ Quantitative Signals Matrix</h1><p style="color: #8a99ad; margin:0;">Aggregated real-time public asset tracking scores</p></div>', unsafe_allow_html=True)
    query = "SELECT s.ticker AS \"Asset Ticker\", c.name AS \"Company Identity\", s.final_score AS \"Master Quant Score\", s.reasons AS \"System Research Notes\" FROM scores s JOIN companies c ON s.ticker = c.ticker ORDER BY s.final_score DESC;"
    df = pd.read_sql_query(query, connection)
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)

# 🐋 DEDICATED INDEPENDENT HIGH PROFILE TRADER HISTORY LEDGER PAGE
with tab_whales:
    st.markdown('<div class="quiver-container"><h1>🐋 Whale Ledger Auditor Portal</h1><p style="color: #8a99ad; margin:0;">One-click list selection interface displaying historical execution sheets</p></div>', unsafe_allow_html=True)

    # Structured clean selector row list
    selected_whale_profile = st.selectbox(
        "🗂️ SELECT ANY REGISTERED TRADER PROFILE TO GENERATE LIVE BALANCE LEDGER SHEET:",
        whale_names_list,
        key="dedicated_whale_tab_selector"
    )

    if selected_whale_profile:
        cursor = connection.cursor()
        cursor.execute("SELECT category, annual_return, trading_style, biography FROM trader_registry WHERE name = %s;", (selected_whale_profile,))
        whale_record = cursor.fetchone()
        cursor.close()

        if whale_record:
            cat, ret, style, bio = whale_record
            st.markdown(f"""
                <div class="bio-card">
                    <h3 style="margin:0; color:#f4f4f0;">👤 Profile Dossier: {selected_whale_profile}</h3>
                    <p style="margin:3px 0 10px 0; color:#8a99ad; font-weight:600; text-transform:uppercase; font-size:0.75rem;">Classification Group: {cat} | Performance Vector: {ret}% Annualized Returns</p>
                    <p style="color:#8a99ad; font-size:0.95rem; line-height:1.4; margin:0;">{bio}</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"### 📋 Clear Transaction Execution History: {selected_whale_profile}")
            query_history = """
                SELECT ticker AS "Asset Symbol", transaction_type AS "Action Type",
                       transaction_date AS "Execution Date", dollar_value AS "Est Allocation Value ($)",
                       research_insight AS "Hedge Context Notes"
                FROM super_investor_history
                WHERE investor_name = %s
                ORDER BY transaction_date DESC;
            """
            df_target_history = pd.read_sql_query(query_history, connection, params=(selected_whale_profile,))

            if not df_target_history.empty:
                # Append green and red visibility markers inside clean ledger text grids
                df_target_history["Action Type"] = df_target_history["Action Type"].apply(
                    lambda x: f"🟢 {x}" if "Buy" in x or "Purchase" in x else f"🔴 {x}"
                )
                st.dataframe(
                    df_target_history,
                    use_container_width=True,
                    hide_index=True,
                    column_config={"Est Allocation Value ($)": st.column_config.NumberColumn(format="$%d")}
                )
            else:
                st.info("No transactional filings reported by regulators for this specific target timeline block.")

with tab_news:
    st.markdown('<div class="quiver-container"><h1>📰 Live Market News Terminal</h1><p style="color: #8a99ad; margin:0;">Comprehensive multi-source financial media streaming feed</p></div>', unsafe_allow_html=True)
    feed = feedparser.parse("https://marketwatch.com")
    if not feed.entries:
        st.info("No live headlines available right now.")
    else:
        for entry in feed.entries[:20]:
            st.markdown(
                f'<div class="news-box"><h4 style="margin:0;"><a href="{entry.get("link","#")}" target="_blank" style="color:#f4f4f0; text-decoration:none;">{entry.get("title","")}</a></h4><p style="font-size:0.8rem; color:#8a99ad; margin-top:4px;">Channel Source: MarketWatch Media Terminal</p></div>',
                unsafe_allow_html=True,
            )

with tab_help:
    st.markdown('<div class="quiver-container"><h1>❓ AlphaQuant Research Co-Pilot</h1><p style="color: #8a99ad; margin:0;">Ask questions about stock terms, market calculations, or trader movements instantly</p></div>', unsafe_allow_html=True)
    user_query = st.text_input("ENTER INVESTING OR CONTRARIAN TRADING QUESTION BELOW:", key="help_ai_input_box")
    if user_query:
        with st.spinner("Analyzing parameters..."):
            try:
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4,
                    messages=[
                        {"role": "system", "content": "You are a professional hedge fund analyst. Give direct, precise financial answers without filler dialogue."},
                        {"role": "user", "content": user_query},
                    ],
                )
                st.markdown(
                    f'<div class="bio-card" style="border-left-color: #10b981;"><p style="color:#f4f4f0; font-size:0.95rem; line-height:1.5;">{response}</p></div>',
                    unsafe_allow_html=True,
                )
            except Exception:
                st.markdown(
                    '<div class="bio-card" style="border-left-color: #ef4444;"><p style="color:#f4f4f0;">Data channel busy. Re-submit question to cycle pipeline lines.</p></div>',
                    unsafe_allow_html=True,
                )

connection.close()
