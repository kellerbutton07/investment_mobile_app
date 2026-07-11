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

# Configure professional enterprise application settings
st.set_page_config(page_title="AlphaQuant Core Terminal", layout="wide", initial_sidebar_state="expanded")

# Apply modern dark mode styling adjustments via clean CSS formatting
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #ffffff; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: 700; }
    .stDataFrame { border: 1px solid #1e293b; border-radius: 8px; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

st.title("🏛️ AlphaQuant Core Investment Terminal")
st.caption("Institutional-grade cross-signal quantitative screening dashboard matrix")
st.markdown("---")

# SAFELY CHECK FOR CLOUD DATABASE SECRETS
# This stops the app from crashing if it can't find your database passwords yet!
if "postgres" not in st.secrets:
    st.info("👋 Welcome to your live Mobile App interface shell!")
    st.warning("🔒 Cloud Database connection pending setup.")
    st.markdown("""
    ### Final Steps to Connect Your Data:
    1. Look at the bottom-right corner of this web page and click **Manage app** (or click the 3 dots menu at the top right).
    2. Click on **Settings**, then select **Secrets**.
    3. Paste your cloud data server settings inside the text box and click **Save**.
    
    Once saved, your phone app will securely sync with your stock market data tables!
    """)
else:
    try:
        # Load credentials directly from the secure cloud settings panel
        db_secrets = st.secrets["postgres"]
        
        connection = psycopg2.connect(
            host=db_secrets["host"],
            port=db_secrets["port"],
            user=db_secrets["user"],
            password=db_secrets["password"],
            database=db_secrets["database"]
        )
        
        query = """
            SELECT s.ticker AS "Asset Ticker", 
                   c.name AS "Company Identity",
                   s.final_score AS "Master Quant Score", 
                   s.confidence AS "Data Confidence", 
                   s.reasons AS "System Research Notes"
            FROM scores s
            JOIN companies c ON s.ticker = c.ticker
            ORDER BY s.final_score DESC;
        """
        
        df = pd.read_sql_query(query, connection)
        connection.close()

        if df.empty:
            st.error("No metrics calculated yet. Please run your calculation engine files in Cursor.")
        else:
            # Create an asset tracking metric row summary layout
            total_tracked = len(df)
            highest_score = df["Master Quant Score"].max()
            top_asset = df.iloc[0]["Asset Ticker"] if not df.empty else "N/A"

            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                st.metric(label="Active Qualified Assets Screened", value=total_tracked)
            with metric_col2:
                st.metric(label="Maximum Quant Score Detected", value=f"{highest_score} pts")
            with metric_col3:
                st.metric(label="Top Priority Candidate", value=top_asset, delta="Valuation Priority")

            st.markdown("### 📊 Live System Alpha Recommendations Portfolio Matrix")
            st.markdown("Stocks costing more than **$200 per share are auto-filtered out**. Lower-valuation assets are heavily favored.")
            
            # Display data inside an optimized interactive corporate table UI
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Master Quant Score": st.column_config.ProgressColumn(
                        "Master Quant Score", help="Aggregated signal calculation score matrix", min_value=0, max_value=100, format="%d"
                    ),
                    "Data Confidence": st.column_config.NumberColumn(format="%d%%")
                }
            )

    except Exception as error:
        st.error(f"Failed to generate dashboard presentation views: {error}")
