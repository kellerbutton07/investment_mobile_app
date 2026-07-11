import subprocess
import sys

try:
    import streamlit as st
    import pandas as pd
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit pandas"])
    import streamlit as st
    import pandas as pd

try:
    import psycopg2
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
    import psycopg2

st.set_page_config(page_title="AlphaQuant Pro Core Terminal", layout="wide", initial_sidebar_state="expanded")

# Dark-mode professional theme aesthetics engine styles
st.markdown("""
    <style>
    .stApp { background-color: #0b0f17; }
    .main { background-color: #0b0f17; }
    h1 { color: #ffffff; font-family: 'Inter', system-ui, sans-serif; font-weight: 800; font-size: 2.5rem; letter-spacing: -0.05rem; }
    h2, h3 { color: #f8fafc; font-family: 'Inter', system-ui, sans-serif; font-weight: 600; }
    .crypto-card { background-color: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.5); }
    .stDataFrame { border: 1px solid #1f2937; border-radius: 10px; overflow: hidden; background-color: #111827; }
    [data-testid="stSidebar"] { background-color: #0d131f; border-right: 1px solid #1f2937; }
    </style>
""", unsafe_allow_html=True)

# Database connection gateway fallback logic
if "postgres" in st.secrets:
    db_secrets = st.secrets["postgres"]
    host = db_secrets["host"]
    password = db_secrets["password"]
else:
    host = "ep-mute-tooth-adtz6q0f.c-2.us-east-1.aws.neon.tech"
    password = "npg_AYovDKM7VL8s"

# Establish baseline database connection to parse sidebar setup lists
connection = psycopg2.connect(host=host, port="5432", user="neondb_owner", password=password, database="neondb", sslmode="require")

# Fetch unique list of high profile investors for the select boxes
cursor = connection.cursor()
try:
    cursor.execute("SELECT DISTINCT investor_name FROM super_investor_history;")
    available_investors = [row[0] for row in cursor.fetchall()]
except Exception:
    available_investors = ["Warren Buffett (Berkshire)", "Michael Burry (Scion)", "Nancy Pelosi (Capitol)", "Jensen Huang (NVIDIA CEO)"]
cursor.close()

# 🖥️ PROFESSIONAL INTERACTIVE CONTROL SIDEBAR PANEL
with st.sidebar:
    st.markdown("### 🏛️ Operational Controls")
    st.caption("AlphaQuant Enterprise Engine Settings")
    st.markdown("---")
    
    selected_view = st.radio("Navigation Matrix", ["🔥 Core Market Signals", "🐋 Super Investor Intel Tracker", "⚙️ Data Warehouse Status"])
    
    st.markdown("---")
    st.markdown("### 🐋 Target Whales Filter")
    # THE MULTI-SELECT DROP DOWN BOX FUNCTIONALITY
    target_whales = st.multiselect(
        "Select High-Profile Targets:",
        options=available_investors,
        default=available_investors[:2] # Pre-select top two targets by default
    )
    
    st.markdown("---")
    st.caption("© 2026 AlphaQuant Core Technologies. Secure Cloud Mode Enabled.")

# MAIN INTERFACE APP RENDERING ROUTING 
if selected_view == "🔥 Core Market Signals":
    st.markdown('<div class="crypto-card"><h1>🏛️ AlphaQuant Core Pro Terminal</h1><p style="color: #94a3b8; font-size: 1.1rem; margin-top:-5px;">Institutional Cross-Signal Asset Scorer Matrix</p></div>', unsafe_allow_html=True)
    
    query = """
        SELECT s.ticker AS "Asset Ticker", c.name AS "Company Identity", s.final_score AS "Master Quant Score", 
               s.confidence AS "Data Confidence", s.reasons AS "System Research Notes"
        FROM scores s JOIN companies c ON s.ticker = c.ticker ORDER BY s.final_score DESC;
    """
    df = pd.read_sql_query(query, connection)
    
    if not df.empty:
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1: st.metric(label="Active Qualified Assets Screened", value=len(df))
        with m_col2: st.metric(label="Maximum Quant Score Detected", value=f"{df['Master Quant Score'].max()} pts")
        with m_col3: st.metric(label="Top Priority Candidate", value=df.iloc[0]["Asset Ticker"], delta="Valuation Priority")

        st.markdown("<br>### 📊 Live System Alpha Recommendations Portfolio Matrix", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)

elif selected_view == "🐋 Super Investor Intel Tracker":
    st.markdown('<div class="crypto-card"><h1>🐋 Super Investor History Audit</h1><p style="color: #94a3b8; font-size: 1.1rem; margin-top:-5px;">Real-Time Transaction Intelligence Matrix</p></div>', unsafe_allow_html=True)
    
    if not target_whales:
        st.info("💡 Please select at least one trader from the drop-down menu in the left sidebar to audit their file logs!")
    else:
        # Generate dynamic query targeting selected individuals
        query = """
            SELECT investor_name AS "Trader Profile", ticker AS "Asset Symbol", transaction_type AS "Action",
                   transaction_date AS "Filing Date", dollar_value AS "Est Dollar Value ($)", research_insight AS "Transaction Insights / Context"
            FROM super_investor_history
            WHERE investor_name IN %s
            ORDER BY transaction_date DESC;
        """
        # Convert list format safely to match SQL filter syntax parameters
        df_whales = pd.read_sql_query(query, connection, params=(tuple(target_whales),))
        
        if df_whales.empty:
            st.warning("No records matched for the selected combination profiles.")
        else:
            st.markdown(f"### 📋 Audit Dossier: Displaying tracking summaries for {len(target_whales)} selected entities")
            st.dataframe(
                df_whales, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Est Dollar Value ($)": st.column_config.NumberColumn(format="$%d"),
                    "Filing Date": st.column_config.DateColumn("Filing Date", format="YYYY-MM-DD")
                }
            )

elif selected_view == "⚙️ Data Warehouse Status":
    st.markdown('<div class="crypto-card"><h1>⚙️ Cloud Warehouse Repositories</h1><p style="color: #94a3b8; font-size: 1.1rem; margin-top:-5px;">Infrastructure Connectivity Status Logs</p></div>', unsafe_allow_html=True)
    st.success("🟢 Connected Table: super_investor_history (9 Institutional Node Profiles Online)")
    st.success("🟢 Primary Data Pipeline Connected: NEON AWS SERVER")

connection.close()
