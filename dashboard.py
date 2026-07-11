import subprocess
import sys

try:
    import streamlit as st
    import pandas as pd
    import feedparser
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit pandas feedparser"])
    import streamlit as st
    import pandas as pd
    import feedparser

try:
    import psycopg2
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
    import psycopg2

st.set_page_config(page_title="AlphaQuant Core Terminal", layout="wide", initial_sidebar_state="expanded")

# 🏛️ QUIVER QUANTITATIVE UI STYLING ENGINE OVERRIDES
st.markdown("""
    <style>
    .stApp { background-color: #0a0d14; }
    .main { background-color: #0a0d14; }
    [data-testid="stSidebar"] { background-color: #0e121a; border-right: 1px solid #1a1f2c; }
    h1 { color: #f4f4f0; font-family: 'Inter', system-ui, sans-serif; font-weight: 700; font-size: 2.2rem; letter-spacing: -0.04rem; }
    h2, h3 { color: #e2e8f0; font-family: 'Inter', system-ui, sans-serif; font-weight: 600; letter-spacing: -0.02rem; }
    p, span, label { color: #8a99ad !important; font-family: 'Inter', sans-serif; }
    [data-testid="stMetricValue"] { color: #f4f4f0 !important; font-family: 'Inter', sans-serif; font-weight: 700; font-size: 2rem !important; }
    .quiver-container { background-color: #0e121a; border: 1px solid #1a1f2c; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
    .news-box { border-bottom: 1px solid #1a1f2c; padding: 15px 0; }
    .stDataFrame { border: 1px solid #1a1f2c; border-radius: 8px; overflow: hidden; background-color: #0e121a; }
    
    /* Bio & Dossier Display Card Custom Overrides */
    .bio-card {
        background-color: #0e121a;
        border-left: 4px solid #f4f4f0;
        border-top: 1px solid #1a1f2c;
        border-right: 1px solid #1a1f2c;
        border-bottom: 1px solid #1a1f2c;
        border-radius: 0 8px 8px 0;
        padding: 20px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Secure cloud connection configuration fallback logic
if "postgres" in st.secrets:
    db_secrets = st.secrets["postgres"]
    host = db_secrets["host"]
    password = db_secrets["password"]
else:
    host = "ep-mute-tooth-adtz6q0f.c-2.us-east-1.aws.neon.tech"
    password = "npg_AYovDKM7VL8s"

connection = psycopg2.connect(host=host, port="5432", user="neondb_owner", password=password, database="neondb", sslmode="require")

# 🖥️ SIDEBAR NAVIGATION (QUIVER SPEC MODULE)
with st.sidebar:
    st.markdown("### ⚡ ALTERNATIVE DATA CORRIDOR")
    st.caption("Quiver Data Architecture Framework")
    st.markdown("---")
    
    selected_view = st.radio("DATA FEEDS", [
        "📈 Core Scorer Signals", 
        "🐋 Whale Performance Registry", # NEW INDEPENDENT DEDICATED PAGE
        "📰 Live Market Terminal", 
        "🔌 System Status"
    ])
    st.markdown("---")
    st.caption("AlphaQuant v2.8.0 Secure Cloud Mode Active")

# ----------------- PAGE ROUTING -----------------

if selected_view == "📈 Core Scorer Signals":
    st.markdown('<div class="quiver-container"><h1>⚡ Quantitative Alternative Signals Core</h1><p style="color: #8a99ad; margin-top:-5px;">Aggregated real-time public transaction intelligence matrix tracking</p></div>', unsafe_allow_html=True)
    query = """
        SELECT s.ticker AS "Asset Ticker", c.name AS "Company Identity", s.final_score AS "Master Quant Score", 
               s.confidence AS "Data Confidence", s.reasons AS "System Research Notes"
        FROM scores s JOIN companies c ON s.ticker = c.ticker ORDER BY s.final_score DESC;
    """
    df = pd.read_sql_query(query, connection)
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)

# 🆕 BRAND NEW PAGE: THE WHALE PERFORMANCE REGISTRY & DOSSIER ENGINE
elif selected_view == "🐋 Whale Performance Registry":
    st.markdown('<div class="quiver-container"><h1>🐋 Whale Performance Registry</h1><p style="color: #8a99ad; margin-top:-5px;">Tracking and auditing high-profile managers sorted by annualized market returns</p></div>', unsafe_allow_html=True)
    
    # Load profile data table from cloud
    query_roster = """
        SELECT name AS "Trader Profile", category AS "Sector Classification", 
               annual_return AS "3-Yr Annualized Return (%)", trading_style AS "Execution Focus"
        FROM trader_registry
        ORDER BY annual_return DESC;
    """
    df_roster = pd.read_sql_query(query_roster, connection)
    
    st.markdown("### 📊 Performance Leaderboard")
    st.caption("Click any column header to sort on demand. Select a trader below to view their complete dossier file.")
    
    # Display the high-end leaderboard grid
    st.dataframe(
        df_roster,
        use_container_width=True,
        hide_index=True,
        column_config={
            "3-Yr Annualized Return (%)": st.column_config.NumberColumn(format="%.1f%%")
        }
    )
    
    st.markdown("---")
    
    if df_roster.empty:
        st.warning("No trader profiles found. Run python fetch_super_investors.py first.")
    else:
        # 🗚 THE USER CLICK SELECTOR INTERACTIVE DROP DOWN FIELD
        selected_target = st.selectbox(
            "🔍 SELECT TARGET PROFILE TO OPEN COMPREHENSIVE DOSSIER:",
            df_roster["Trader Profile"].tolist()
        )
        
        if selected_target:
            # Query specific biography elements for the selected individual
            cursor = connection.cursor()
            cursor.execute("SELECT category, annual_return, trading_style, biography FROM trader_registry WHERE name = %s;", (selected_target,))
            cat, ret, style, bio = cursor.fetchone()
            cursor.close()
            
            # 🎨 RENDER THE SLATE / EGGSHELL BIO PROFILE CARD WINDOW
            st.markdown(f"""
                <div class="bio-card">
                    <h2 style="margin:0; color:#f4f4f0;">🐋 Dossier Record: {selected_target}</h2>
                    <p style="margin:5px 0 15px 0; color:#8a99ad; font-weight:600; text-transform:uppercase; font-size:0.8rem; letter-spacing:0.05rem;">
                        Classification: {cat} | Audited Track Record: {ret}% Annualized
                    </p>
                    <h4 style="margin:0 0 5px 0; color:#e2e8f0;">⚡ System Execution Blueprint:</h4>
                    <p style="color:#e2e8f0; margin-bottom:15px; font-size:0.95rem;">{style}</p>
                    <h4 style="margin:0 0 5px 0; color:#e2e8f0;">📖 Background Profile context:</h4>
                    <p style="color:#8a99ad; font-size:0.95rem; line-height:1.5;">{bio}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Pull transactional audit logging tracking tables for this specific individual
            st.markdown(f"### 📋 Public Position Audit Log: {selected_target}")
            query_history = """
                SELECT ticker AS "Asset Symbol", transaction_type AS "Action",
                       transaction_date AS "Filing Date", dollar_value AS "Est Dollar Value ($)", research_insight AS "Context / Evidence"
                FROM super_investor_history
                WHERE investor_name = %s
                ORDER BY transaction_date DESC;
            """
            df_target_history = pd.read_sql_query(query_history, connection, params=(selected_target,))
            
            if df_target_history.empty:
                st.info("No corporate filings or alternative transactions recorded for this quarter period cycle.")
            else:
                df_target_history["Action"] = df_target_history["Action"].apply(lambda x: f"🟢 {x}" if "Buy" in x or "Purchase" in x else f"🔴 {x}")
                st.dataframe(
                    df_target_history,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Est Dollar Value ($)": st.column_config.NumberColumn(format="$%d")
                    }
                )

elif selected_view == "📰 Live Market Terminal":
    st.markdown('<div class="quiver-container"><h1>📰 Live Market News Terminal</h1><p style="color: #8a99ad; margin-top:-5px;">Real-time global news aggregation</p></div>', unsafe_allow_html=True)
    # Reuses your verified live RSS reader module code logic...
    feed = feedparser.parse("https://marketwatch.com")
    for entry in feed.entries[:5]:
        st.markdown(f'<div class="news-box"><h4 style="margin:0;"><a href="{entry.get("link","#")}" target="_blank" style="color:#f4f4f0; text-decoration:none;">{entry.get("title","")}</a></h4></div>', unsafe_allow_html=True)

elif selected_view == "🔌 System Status":
    st.markdown('<div class="quiver-container"><h1>🔌 Infrastructure Hub</h1><p style="color: #8a99ad; margin-top:-5px;">Alternative tracker connectivity logs</p></div>', unsafe_allow_html=True)
    st.success("🟢 Connected Table: trader_registry (Relational Dossier Framework Mapping Live)")

connection.close()
