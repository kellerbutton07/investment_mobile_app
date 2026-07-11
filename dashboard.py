import subprocess
import sys

try:
    import streamlit as st
    import pandas as pd
    import feedparser
    import yfinance as yf
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit pandas feedparser yfinance"])
    import streamlit as st
    import pandas as pd
    import feedparser
    import yfinance as yf

try:
    import psycopg2
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
    import psycopg2

st.set_page_config(page_title="AlphaQuant Core Terminal", layout="wide", initial_sidebar_state="collapsed")

# 🏛️ INSTITUTIONAL UI THEME & BOTTOM ICON NAVIGATION OVERRIDES
st.markdown("""
    <style>
    .stApp { background-color: #0a0d14; padding-bottom: 80px; }
    .main { background-color: #0a0d14; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    
    h1 { color: #f4f4f0; font-family: 'Inter', system-ui, sans-serif; font-weight: 700; font-size: 1.8rem; letter-spacing: -0.04rem; margin-top: 5px; }
    h2, h3 { color: #e2e8f0; font-family: 'Inter', system-ui, sans-serif; font-weight: 600; letter-spacing: -0.02rem; }
    p, span, label { color: #8a99ad !important; font-family: 'Inter', sans-serif; }
    [data-testid="stMetricValue"] { color: #f4f4f0 !important; font-family: 'Inter', sans-serif; font-weight: 700; font-size: 1.5rem !important; }
    
    .quiver-container { background-color: #0e121a; border: 1px solid #1a1f2c; border-radius: 8px; padding: 15px; margin-bottom: 15px; }
    .bio-card { background-color: #0e121a; border-left: 4px solid #f4f4f0; border-top: 1px solid #1a1f2c; border-right: 1px solid #1a1f2c; border-bottom: 1px solid #1a1f2c; border-radius: 0 8px 8px 0; padding: 20px; margin-top: 15px; }
    .news-box { border-bottom: 1px solid #1a1f2c; padding: 12px 0; }
    .stDataFrame { border: 1px solid #1a1f2c; border-radius: 8px; overflow: hidden; background-color: #0e121a; }
    .sector-btn { background-color: #1a1f2c; border: 1px solid #2d3748; padding: 12px; border-radius: 8px; text-align: center; color: #f4f4f0; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# Secure cloud database parameters
if "postgres" in st.secrets:
    db_secrets = st.secrets["postgres"]
    host = db_secrets["host"]
    password = db_secrets["password"]
else:
    host = "ep-mute-tooth-adtz6q0f.c-2.us-east-1.aws.neon.tech"
    password = "npg_AYovDKM7VL8s"

connection = psycopg2.connect(host=host, port="5432", user="neondb_owner", password=password, database="neondb", sslmode="require")

if "current_view" not in st.session_state:
    st.session_state.current_view = "🔍 EXPLORE"
if "timeframe" not in st.session_state:
    st.session_state.timeframe = "1M"  # Default timeline to 1 Month

# Pinned Bottom Style Icon Selection Bar Layout Rows
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
with nav_col1:
    if st.button("🔍\n\nEXPLORE", use_container_width=True, type="primary" if st.session_state.current_view == "🔍 EXPLORE" else "secondary"):
        st.session_state.current_view = "🔍 EXPLORE"
        st.rerun()
with nav_col2:
    if st.button("📈\n\nSIGNALS", use_container_width=True, type="primary" if st.session_state.current_view == "📈 SIGNALS" else "secondary"):
        st.session_state.current_view = "📈 SIGNALS"
        st.rerun()
with nav_col3:
    if st.button("🐋\n\nWHALES", use_container_width=True, type="primary" if st.session_state.current_view == "🐋 WHALES" else "secondary"):
        st.session_state.current_view = "🐋 WHALES"
        st.rerun()
with nav_col4:
    if st.button("📰\n\nNEWS", use_container_width=True, type="primary" if st.session_state.current_view == "📰 NEWS" else "secondary"):
        st.session_state.current_view = "📰 NEWS"
        st.rerun()

st.markdown("---")

# ----------------- NATIVE ROUTING ROUTINES -----------------

if st.session_state.current_view == "🔍 EXPLORE":
    st.markdown('<div class="quiver-container"><h1>🔍 Market Discovery Explorer</h1><p style="color: #8a99ad; margin:0;">Search global financial channels powered by Yahoo Finance engines</p></div>', unsafe_allow_html=True)

    st.markdown("### 🔎 Universal Asset Search Engine")
    user_search_ticker = st.text_input("TYPE IN ANY TICKER SYMBOL (e.g., TSLA, NVDA, AAPL, AMZN):", value="TSLA").upper().strip()

    if user_search_ticker:
        try:
            ticker_obj = yf.Ticker(user_search_ticker)
            ticker_info = ticker_obj.info

            # --- INTERACTIVE TIMEFRAME INTERVAL MAPPER SELECTION BAR ---
            st.markdown("##### ⏱️ Select Tracking Chart Timeframe")
            t_col1, t_col2, t_col3, t_col4, t_col5 = st.columns(5)

            # Mapping readable labels directly to official Yahoo intervals
            tf_mapping = {"1D": ("1d", "15m"), "1W": ("5d", "60m"), "1M": ("1mo", "1d"), "1Y": ("1y", "1d"), "MAX": ("max", "1wk")}

            with t_col1:
                if st.button("1 DAY", use_container_width=True, type="primary" if st.session_state.timeframe == "1D" else "secondary"):
                    st.session_state.timeframe = "1D"
                    st.rerun()
            with t_col2:
                if st.button("1 WEEK", use_container_width=True, type="primary" if st.session_state.timeframe == "1W" else "secondary"):
                    st.session_state.timeframe = "1W"
                    st.rerun()
            with t_col3:
                if st.button("1 MONTH", use_container_width=True, type="primary" if st.session_state.timeframe == "1M" else "secondary"):
                    st.session_state.timeframe = "1M"
                    st.rerun()
            with t_col4:
                if st.button("1 YEAR", use_container_width=True, type="primary" if st.session_state.timeframe == "1Y" else "secondary"):
                    st.session_state.timeframe = "1Y"
                    st.rerun()
            with t_col5:
                if st.button("LIFETIME", use_container_width=True, type="primary" if st.session_state.timeframe == "MAX" else "secondary"):
                    st.session_state.timeframe = "MAX"
                    st.rerun()

            # Execute live data pulling using chosen interval settings
            chosen_period, chosen_interval = tf_mapping[st.session_state.timeframe]
            ticker_history = ticker_obj.history(period=chosen_period, interval=chosen_interval)

            if not ticker_history.empty:
                company_title = ticker_info.get("longName", f"{user_search_ticker} Equity Profile")
                live_price = ticker_history["Close"].iloc[-1]

                # --- COLOR ENGINE LOGIC CALCULATION ROUTINES ---
                # Check performance relative to chart execution baseline start point
                start_price = ticker_history["Close"].iloc[0]
                price_return_pct = ((live_price - start_price) / start_price) * 100

                # Choose color badges mimicking official Quiver terminal styles
                if live_price >= start_price:
                    chart_line_color = "#10b981"  # Elegant Mint Green
                    direction_label = "🟢 UP"
                else:
                    chart_line_color = "#ef4444"  # Stark Coral Red
                    direction_label = "🔴 DOWN"

                # Display accurate stats blocks
                stat_col1, stat_col2, stat_col3 = st.columns(3)
                with stat_col1:
                    st.metric("Asset Identity", company_title)
                with stat_col2:
                    st.metric("Live Market Price", f"${live_price:.2f}", f"{price_return_pct:+.2f}% Over Timeline")
                with stat_col3:
                    st.metric("Timeline Performance Status", direction_label)

                # --- RENDER DYNAMIC LINE DIAGRAM WITH ACTIVE COLOR MIXINGS ---
                st.markdown(f"### 📈 {user_search_ticker} Price Chart ({st.session_state.timeframe} Window)")
                chart_data = pd.DataFrame({"Price ($)": ticker_history["Close"]})

                # Render chart inside app grid using native lines and custom color injection tracking
                st.line_chart(chart_data, color=chart_line_color)
            else:
                st.error("Ticker registry empty for choice configuration parameters.")
        except Exception as err:
            st.error(f"Failed to compile dynamic performance diagram charts: {err}")

elif st.session_state.current_view == "📈 SIGNALS":
    st.markdown('<div class="quiver-container"><h1>⚡ Quantitative Signals Matrix</h1><p style="color: #8a99ad; margin:0;">Alternative data tracking clusters</p></div>', unsafe_allow_html=True)
    query = "SELECT s.ticker AS \"Asset Ticker\", c.name AS \"Company Identity\", s.final_score AS \"Master Quant Score\", s.confidence AS \"Data Confidence\", s.reasons AS \"System Research Notes\" FROM scores s JOIN companies c ON s.ticker = c.ticker ORDER BY s.final_score DESC;"
    df = pd.read_sql_query(query, connection)
    if not df.empty:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Master Quant Score": st.column_config.ProgressColumn(
                    "Master Quant Score",
                    min_value=0,
                    max_value=100,
                    format="%d",
                )
            },
        )

elif st.session_state.current_view == "🐋 WHALES":
    st.markdown('<div class="quiver-container"><h1>🐋 Whale Performance Registry</h1><p style="color: #8a99ad; margin:0;">Dossier profile matrix tracking annualized fund returns</p></div>', unsafe_allow_html=True)
    query_roster = 'SELECT name AS "Trader Profile", category AS "Classification", annual_return AS "3-Yr Return (%)", trading_style AS "Execution Focus" FROM trader_registry ORDER BY annual_return DESC;'
    df_roster = pd.read_sql_query(query_roster, connection)
    st.dataframe(
        df_roster,
        use_container_width=True,
        hide_index=True,
        column_config={"3-Yr Return (%)": st.column_config.NumberColumn(format="%.1f%%")},
    )

elif st.session_state.current_view == "📰 NEWS":
    st.markdown('<div class="quiver-container"><h1>📰 Live Market News Terminal</h1><p style="color: #8a99ad; margin:0;">Streaming alternative macro text alerts</p></div>', unsafe_allow_html=True)
    feed = feedparser.parse("https://marketwatch.com")
    if not feed.entries:
        st.info("No live headlines available right now.")
    else:
        for entry in feed.entries[:5]:
            st.markdown(
                f'<div class="news-box"><h4 style="margin:0;"><a href="{entry.get("link","#")}" target="_blank" style="color:#f4f4f0; text-decoration:none;">{entry.get("title","")}</a></h4></div>',
                unsafe_allow_html=True,
            )

connection.close()
