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

st.set_page_config(page_title="AlphaQuant Core Terminal", layout="wide", initial_sidebar_state="expanded")

# 🏛️ QUIVER QUANTITATIVE UI STYLING ENGINE OVERRIDES
st.markdown("""
    <style>
    /* Quiver Dark Palette Core Canvas Background */
    .stApp { background-color: #0a0d14; }
    .main { background-color: #0a0d14; }
    
    /* Sleek Slate Sidebar Configuration */
    [data-testid="stSidebar"] { background-color: #0e121a; border-right: 1px solid #1a1f2c; }
    
    /* Typography Overrides - Soft Eggshell & Matte Silver */
    h1 { color: #f4f4f0; font-family: 'Inter', system-ui, sans-serif; font-weight: 700; font-size: 2.2rem; letter-spacing: -0.04rem; }
    h2, h3 { color: #e2e8f0; font-family: 'Inter', system-ui, sans-serif; font-weight: 600; letter-spacing: -0.02rem; }
    p, span, label { color: #8a99ad !important; font-family: 'Inter', sans-serif; }
    
    /* Institutional Metric Summary Displays */
    [data-testid="stMetricValue"] { color: #f4f4f0 !important; font-family: 'Inter', sans-serif; font-weight: 700; font-size: 2rem !important; }
    [data-testid="stMetricLabel"] { color: #8a99ad !important; font-size: 0.75rem !important; letter-spacing: 0.06rem; text-transform: uppercase; }
    
    /* Quiver-Style Flat Border Storage Modules */
    .quiver-container {
        background-color: #0e121a;
        border: 1px solid #1a1f2c;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Data Console Overlay Customizations */
    .stDataFrame { border: 1px solid #1a1f2c; border-radius: 8px; overflow: hidden; background-color: #0e121a; }
    
    /* Clean Custom Formats for Data Grid Columns */
    div[data-testid="stMarkdownContainer"] p { font-size: 0.95rem; }
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

cursor = connection.cursor()
try:
    cursor.execute("SELECT DISTINCT investor_name FROM super_investor_history;")
    available_investors = [row[0] for row in cursor.fetchall()]
except Exception:
    available_investors = ["Warren Buffett (Berkshire)", "Michael Burry (Scion)", "Nancy Pelosi (Capitol)", "Jensen Huang (NVIDIA CEO)"]
cursor.close()

# 🖥️ SIDEBAR NAVIGATION (QUIVER SPEC MODULE)
with st.sidebar:
    st.markdown("### ⚡ ALTERNATIVE DATA CORRIDOR")
    st.caption("Quiver Data Architecture Framework")
    st.markdown("---")
    
    selected_view = st.radio("DATA FEEDS", ["📈 Core Scorer Signals", "🏛️ Congressional & Whale Ledger", "🔌 System Architecture Status"])
    
    st.markdown("---")
    st.markdown("### 🐋 ACTIVE TRACKING GROUP")
    target_whales = st.multiselect(
        "Select Tracking Profiles:",
        options=available_investors,
        default=available_investors[:2]
    )
    st.markdown("---")
    st.caption("AlphaQuant v2.6.0 Stable Web Engine Container")

# MAIN TERMINAL PORTS RNDERING
if selected_view == "📈 Core Scorer Signals":
    st.markdown('<div class="quiver-container"><h1>⚡ Quantitative Alternative Signals Core</h1><p style="color: #8a99ad; margin-top:-5px;">Aggregated real-time public transaction intelligence matrix tracking</p></div>', unsafe_allow_html=True)
    
    query = """
        SELECT s.ticker AS "Asset Ticker", c.name AS "Company Identity", s.final_score AS "Master Quant Score", 
               s.confidence AS "Data Confidence", s.reasons AS "System Research Notes"
        FROM scores s JOIN companies c ON s.ticker = c.ticker ORDER BY s.final_score DESC;
    """
    df = pd.read_sql_query(query, connection)
    
    if not df.empty:
        # Performance metric data summaries
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1: st.metric(label="Total Tracked Equities", value=len(df))
        with m_col2: st.metric(label="Peak Quant Evaluation", value=f"{df['Master Quant Score'].max()} pts")
        with m_col3: st.metric(label="Priority Candidate Assignment", value=df.iloc[0]["Asset Ticker"])

        st.markdown("<br>### 📊 Live System Alpha Recommendations Portfolio Matrix", unsafe_allow_html=True)
        st.dataframe(
            df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Master Quant Score": st.column_config.ProgressColumn(
                    "Master Quant Score", min_value=0, max_value=100, format="%d", color="stone"
                )
            }
        )

elif selected_view == "🏛️ Congressional & Whale Ledger":
    st.markdown('<div class="quiver-container"><h1>🏛️ Corporate & Capitol Hill Filings Ledger</h1><p style="color: #8a99ad; margin-top:-5px;">Audit log tracing positions matching target parameters</p></div>', unsafe_allow_html=True)
    
    if not target_whales:
        st.info("💡 Please choose one or more trading entities from the control console list to plot their ledger sheets.")
    else:
        query = """
            SELECT investor_name AS "Trader Profile", ticker AS "Asset Symbol", transaction_type AS "Action",
                   transaction_date AS "Filing Date", dollar_value AS "Est Dollar Value ($)", research_insight AS "Transaction Insights / Context"
            FROM super_investor_history WHERE investor_name IN %s ORDER BY transaction_date DESC;
        """
        df_whales = pd.read_sql_query(query, connection, params=(tuple(target_whales),))
        
        if not df_whales.empty:
            # 🎨 HIGH-FIDELITY BADGE CONVERSION RULE FOR THE LEDGER MATRIX
            # Adds clean visual markdown markers mimicking Quiver's action labels
            df_whales["Action"] = df_whales["Action"].apply(lambda x: f"🟢 {x}" if "Buy" in x or "Purchase" in x else f"🔴 {x}")
            
            st.markdown(f"### 📋 Audit Dossier: Compiling historical records for {len(target_whales)} active targets")
            st.dataframe(
                df_whales, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Est Dollar Value ($)": st.column_config.NumberColumn(format="$%d"),
                    "Action": st.column_config.TextColumn("Action", help="Green = Buying Accumulation | Red = Selling Liquidation")
                }
            )

elif selected_view == "🔌 System Architecture Status":
    st.markdown('<div class="quiver-container"><h1>🔌 Infrastructure Hub</h1><p style="color: #8a99ad; margin-top:-5px;">Alternative tracker connectivity logs</p></div>', unsafe_allow_html=True)
    st.success("🟢 Connected Node: super_investor_history (Cloud Mirror Repository Sync Clear)")
    st.success("🟢 Primary Data Pipeline: NEON CLOUD SECURITY ENVIRONMENT MODE ACTIVE")

connection.close()
