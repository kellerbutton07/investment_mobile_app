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

st.title("AlphaQuant Core Investment Terminal")
st.caption("Institutional-grade cross-signal quantitative screening dashboard matrix")
st.markdown("---")

try:
    connection = psycopg2.connect(
        "postgresql://neondb_owner:npg_AYovDKM7VL8s@ep-mute-tooth-adtz6q0f.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
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
        st.error("No metrics calculated. Please type 'python score_engine.py' in your application terminal.")
    else:
        # Create an asset tracking metric row summary layout
        total_tracked = len(df)
        highest_score = df["Master Quant Score"].max()
        top_asset = df.iloc[0]["Asset Ticker"]

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric(label="Active Qualified Assets Screened", value=total_tracked)
        with metric_col2:
            st.metric(label="Maximum Quant Score Detected", value=f"{highest_score} pts")
        with metric_col3:
            st.metric(label="Top Priority Candidate", value=top_asset, delta="Valuation Priority")

        st.markdown("### Live System Alpha Recommendations Portfolio Matrix")
        st.markdown("Stocks costing more than **$500 per share are auto-filtered out**. Lower-valuation assets are heavily favored.")
        
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
