import subprocess
import sys

# Verify all enterprise data-visualizer packages are checked out
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

# 🏛️ INSTITUTIONAL QUIVER STYLING ENGINE OVERRIDES
st.markdown("""
    <style>
    .stApp { background-color: #0a0d14; }
    .main { background-color: #0a0d14; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    
    h1 { color: #f4f4f0; font-family: 'Inter', system-ui, sans-serif; font-weight: 700; font-size: 2rem; letter-spacing: -0.04rem; margin-top: 5px; }
    h2, h3 { color: #e2e8f0; font-family: 'Inter', system-ui, sans-serif; font-weight: 600; letter-spacing: -0.02rem; }
    p, span, label { color: #8a99ad !important; font-family: 'Inter', sans-serif; }
    [data-testid="stMetricValue"] { color: #f4f4f0 !important; font-family: 'Inter', sans-serif; font-weight: 700; font-size: 1.6rem !important; }
    
    .quiver-container { background-color: #0e121a; border: 1px solid #1a1f2c; border-radius: 8px; padding: 15px; margin-bottom: 15px; }
    .bio-card { background-color: #0e121a; border-left: 4px solid #f4f4f0; border-top: 1px solid #1a1f2c; border-right: 1px solid #1a1f2c; border-bottom: 1px solid #1a1f2c; border-radius: 0 8px 8px 0; padding: 20px; margin-top: 15px; }
    .news-box { border-bottom: 1px solid #1a1f2c; padding: 12px 0; }
    .stDataFrame { border: 1px solid #1a1f2c; border-radius: 8px; overflow: hidden; background-color: #0e121a; }
    
    /* Responsive Top-Row Application Navigation Segment Controls */
    div.stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: space-around;
        background-color: #0e121a;
        border: 1px solid #1a1f2c;
        border-radius: 10px;
        padding: 4px;
        margin-bottom: 20px;
    }
    div.stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #8a99ad !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 8px 12px;
        border-radius: 6px;
        border: none !important;
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

# 🖥️ NATIVE NAVIGATION PANEL WITH THE NEW INTERACTIVE HELP MODULE ACCENT
tab_explore, tab_signals, tab_whales, tab_news, tab_help = st.tabs([
    "🔍 EXPLORE",
    "📈 SIGNALS",
    "🐋 WHALES",
    "📰 READ",
    "❓ HELP"  # 🆕 NEW NATIVE USER PORT FOR AI ASSISTANT CHANNELS
])

# ----------------- CHANNELS DISPLAY -----------------

with tab_explore:
    st.markdown('<div class="quiver-container"><h1>🔍 Market Discovery Explorer</h1><p style="color: #8a99ad; margin:0;">Search global financial registries powered by clean Yahoo Finance metrics</p></div>', unsafe_allow_html=True)
    user_search_ticker = st.text_input("TYPE IN ANY TICKER SYMBOL:", value="TSLA", key="explore_search_box").upper().strip()
    if user_search_ticker:
        try:
            ticker_obj = yf.Ticker(user_search_ticker)
            ticker_history = ticker_obj.history(period="1mo", interval="1d")
            ticker_info = ticker_obj.info
            if not ticker_history.empty:
                comp_name = ticker_info.get("longName", f"{user_search_ticker} Equity Profile")
                price_now = ticker_history["Close"].iloc[-1]
                price_start = ticker_history["Close"].iloc[0]
                net_change_pct = ((price_now - price_start) / price_start) * 100
                chart_color = "#10b981" if price_now >= price_start else "#ef4444"
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.metric("Asset Name", comp_name)
                with col_m2:
                    st.metric("Price Trend (1-Month)", f"${price_now:.2f}", f"{net_change_pct:+.2f}%")
                st.line_chart(pd.DataFrame({"Price ($)": ticker_history["Close"]}), color=chart_color)
        except Exception:
            st.error("Market search engine currently offline.")

with tab_signals:
    st.markdown('<div class="quiver-container"><h1>⚡ Quantitative Signals Matrix</h1><p style="color: #8a99ad; margin:0;">Aggregated real-time public asset tracking scores</p></div>', unsafe_allow_html=True)
    query = "SELECT s.ticker AS \"Asset Ticker\", c.name AS \"Company Identity\", s.final_score AS \"Master Quant Score\", s.reasons AS \"System Research Notes\" FROM scores s JOIN companies c ON s.ticker = c.ticker ORDER BY s.final_score DESC;"
    df = pd.read_sql_query(query, connection)
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)

with tab_whales:
    st.markdown('<div class="quiver-container"><h1>🐋 Whale Performance Registry</h1><p style="color: #8a99ad; margin:0;">Dossier profiles tracking 50 elite global investors and high-profile targets</p></div>', unsafe_allow_html=True)
    query_roster = 'SELECT name AS "Trader Profile", category AS "Classification", annual_return AS "3-Yr Return (%)", trading_style AS "Execution Focus" FROM trader_registry ORDER BY annual_return DESC;'
    df_roster = pd.read_sql_query(query_roster, connection)
    st.dataframe(df_roster, use_container_width=True, hide_index=True)

    if df_roster.empty:
        st.warning("No trader profiles found. Run python fetch_super_investors.py first.")
    else:
        selected_target = st.selectbox("🔍 SELECT PROFILE TO AUDIT:", df_roster["Trader Profile"].tolist(), key="whale_select_box")
        if selected_target:
            cursor = connection.cursor()
            cursor.execute("SELECT category, annual_return, trading_style, biography FROM trader_registry WHERE name = %s;", (selected_target,))
            cat, ret, style, bio = cursor.fetchone()
            cursor.close()
            st.markdown(
                f'<div class="bio-card"><h3>🐋 Dossier Record: {selected_target}</h3><p style="font-size:0.75rem; color:#8a99ad;">Type: {cat} | Returns: {ret}%</p><p style="color:#e2e8f0; font-size:0.95rem;">{bio}</p></div>',
                unsafe_allow_html=True,
            )

with tab_news:
    st.markdown('<div class="quiver-container"><h1>📰 Live Market News Terminal</h1><p style="color: #8a99ad; margin:0;">Comprehensive multi-source financial media streaming feed</p></div>', unsafe_allow_html=True)
    feed = feedparser.parse("https://marketwatch.com")
    if not feed.entries:
        st.info("Live feed temporarily unavailable. Showing backup headlines.")
        backup_headlines = [
            {"title": "Global Semiconductor Fabrication Plants Adjust Capacity Forecasts Over Logistics Constraints", "link": "https://reuters.com"},
            {"title": "Consumer Moat Operations Record Stable Margin Profiles in Quarterly Financial Audits", "link": "https://marketwatch.com"},
            {"title": "Enterprise Cloud Computing Demands Drive Hardware Expansion Architecture Pipelines", "link": "https://bloomberg.com"},
            {"title": "Federal Subsidy Adjustments Spark Options Volume Inflow Across Defense Assets", "link": "https://reuters.com"},
            {"title": "Macro Inflation Pricing Indexes Level Off Matching Central Bank Strategy Goals", "link": "https://bloomberg.com"},
        ]
        for item in backup_headlines:
            st.markdown(
                f'<div class="news-box"><h4><a href="{item["link"]}" target="_blank" style="color:#f4f4f0; text-decoration:none;">{item["title"]}</a></h4><p style="font-size:0.8rem; color:#8a99ad; margin-top:4px;">Channel Source: Backup Market Terminal</p></div>',
                unsafe_allow_html=True,
            )
    else:
        for entry in feed.entries[:20]:
            st.markdown(
                f'<div class="news-box"><h4><a href="{entry.get("link","#")}" target="_blank" style="color:#f4f4f0; text-decoration:none;">{entry.get("title","")}</a></h4><p style="font-size:0.8rem; color:#8a99ad; margin-top:4px;">Channel Source: MarketWatch Media Terminal</p></div>',
                unsafe_allow_html=True,
            )

# 🆕 BRAND NEW USER INTERFACE SCREEN: INTEL RESEARCH CO-PILOT ASSISTANT (HELP PAGE)
with tab_help:
    st.markdown('<div class="quiver-container"><h1>❓ AlphaQuant Research Co-Pilot</h1><p style="color: #8a99ad; margin:0;">Ask questions about stock terms, market calculations, or trader movements instantly</p></div>', unsafe_allow_html=True)

    st.markdown("### 🤖 Ask Your Financial Analyst")
    user_query = st.text_input(
        "ENTER YOUR INVESTING OR CONTRARIAN TRADING CONTEXT QUESTION BELOW:",
        placeholder="e.g., What does a Price-to-Earnings (P/E) ratio mean, or why did TSLA drop?",
    )

    if user_query:
        with st.spinner("Analyzing parameters and drafting response layout..."):
            try:
                # Direct backend handshake call utilizing free open source model pipeline routing
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional, elite institutional quant financial analyst at a top hedge fund. Give precise, clear, direct, and concise investing answers. Do not use generic filler words, pleasantries, or heavy dialogue text blocks. Format using clear markdown.",
                        },
                        {"role": "user", "content": user_query},
                    ],
                )

                # Render the AI's response inside a polished custom card block layout
                st.markdown("#### ⚙️ Co-Pilot Intelligence Output Analysis Summary")
                st.markdown(
                    f'<div class="bio-card" style="border-left-color: #10b981;"><p style="color: #f4f4f0; font-size:0.95rem; line-height:1.5;">{response}</p></div>',
                    unsafe_allow_html=True,
                )

            except Exception as ai_err:
                st.markdown("#### ⚙️ Co-Pilot Intelligence Output Analysis Summary")
                st.markdown(
                    """
                <div class="bio-card" style="border-left-color: #ef4444;">
                    <p style="color: #f4f4f0; font-size:0.95rem;">
                    <strong>Market definition placeholder trace:</strong><br>
                    • P/E Ratio: Represents the trailing price divided by current earnings per share. High numbers imply strong future expansion demands.<br>
                    • Market Action: Asset movements fluctuate over macro liquidity supply shifts, technical resistance bands, and policy changes tracking.<br>
                    <em>Note: AI stream routing throttled. Re-execute question input to clear channel lines.</em>
                    </p>
                </div>
                    """,
                    unsafe_allow_html=True,
                )

connection.close()
