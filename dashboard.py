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

st.set_page_config(page_title="AlphaQuant Terminal", layout="wide", initial_sidebar_state="collapsed")

# Demo gate credential (Streamlit Cloud UI gate — not real auth)
ACCESS_CODE = "alphaquant"

# ── Polistocks / PoliTrade–inspired design tokens (AlphaQuant branding) ──
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
    :root {
        --aq-bg: #070b14;
        --aq-surface: #0d1320;
        --aq-card: #111827;
        --aq-border: rgba(255,255,255,0.08);
        --aq-navy: #0a1f44;
        --aq-navy-bright: #1a3a6b;
        --aq-accent: #3b82f6;
        --aq-text: #f4f6f9;
        --aq-muted: #8b9bb4;
        --aq-gain: #10b981;
        --aq-loss: #ef4444;
    }
    .stApp { background: radial-gradient(1200px 600px at 50% -10%, #0a1f44 0%, #070b14 45%, #05070e 100%) !important; }
    .main { background: transparent !important; }
    .block-container { padding-top: 1.25rem !important; max-width: 1180px !important; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    #MainMenu, footer, header { visibility: hidden; }

    h1, h2, h3, .aq-serif {
        font-family: 'Fraunces', Georgia, serif !important;
        color: var(--aq-text) !important;
        letter-spacing: -0.02em;
        font-weight: 600;
    }
    p, span, label, .stMarkdown, .stTextInput label {
        font-family: 'Inter', system-ui, sans-serif !important;
        color: var(--aq-muted) !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--aq-text) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700;
        font-size: 1.45rem !important;
    }
    [data-testid="stMetricLabel"] { color: var(--aq-muted) !important; }

    /* Brand header */
    .aq-brand-bar {
        display: flex; align-items: center; justify-content: space-between;
        gap: 12px; margin-bottom: 18px; padding: 4px 2px 14px;
        border-bottom: 1px solid var(--aq-border);
    }
    .aq-brand {
        display: flex; align-items: center; gap: 12px;
    }
    .aq-mark {
        width: 36px; height: 36px; border-radius: 10px;
        background: linear-gradient(145deg, #1a3a6b, #0a1f44);
        border: 1px solid rgba(255,255,255,0.12);
        display: flex; align-items: center; justify-content: center;
        color: #f4f6f9; font-family: 'Fraunces', serif; font-weight: 700; font-size: 1.05rem;
    }
    .aq-brand-name {
        font-family: 'Fraunces', Georgia, serif; font-size: 1.35rem; font-weight: 700;
        color: #f4f6f9; letter-spacing: -0.03em; line-height: 1.1;
    }
    .aq-brand-sub {
        font-family: 'Inter', sans-serif; font-size: 0.72rem; color: #8b9bb4;
        text-transform: uppercase; letter-spacing: 0.08em; margin-top: 2px;
    }
    .aq-pill {
        font-family: 'Inter', sans-serif; font-size: 0.72rem; font-weight: 600;
        color: #93c5fd; background: rgba(59,130,246,0.12);
        border: 1px solid rgba(59,130,246,0.25); border-radius: 999px;
        padding: 6px 12px;
    }

    /* Cards */
    .aq-card {
        background: rgba(17, 24, 39, 0.72);
        border: 1px solid var(--aq-border);
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 16px;
        backdrop-filter: blur(8px);
    }
    .aq-card h1 { font-size: 1.55rem !important; margin: 0 0 6px 0 !important; }
    .aq-card p { margin: 0 !important; color: var(--aq-muted) !important; font-size: 0.92rem; }
    .bio-card {
        background: rgba(17, 24, 39, 0.85);
        border-left: 3px solid #3b82f6;
        border: 1px solid var(--aq-border);
        border-left-width: 3px;
        border-radius: 0 12px 12px 0;
        padding: 16px 18px;
        margin-top: 10px;
    }
    .news-box { border-bottom: 1px solid var(--aq-border); padding: 14px 0; }
    .news-box a { color: #f4f6f9 !important; text-decoration: none; font-family: 'Inter', sans-serif; font-weight: 600; }
    .news-box a:hover { color: #93c5fd !important; }
    .stDataFrame {
        border: 1px solid var(--aq-border);
        border-radius: 12px;
        overflow: hidden;
        background-color: #0d1320;
    }

    /* Auth gate */
    .aq-gate-wrap {
        max-width: 420px; margin: 4vh auto 0; text-align: center;
    }
    .aq-gate-card {
        background: rgba(13, 19, 32, 0.92);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 18px;
        padding: 36px 28px 28px;
        box-shadow: 0 24px 60px rgba(0,0,0,0.45), 0 0 0 1px rgba(10,31,68,0.5);
        text-align: left;
    }
    .aq-gate-mark {
        width: 48px; height: 48px; border-radius: 14px; margin: 0 auto 18px;
        background: linear-gradient(145deg, #1a3a6b, #0a1f44);
        border: 1px solid rgba(255,255,255,0.14);
        display: flex; align-items: center; justify-content: center;
        color: #fff; font-family: 'Fraunces', serif; font-weight: 700; font-size: 1.35rem;
    }
    .aq-gate-title {
        font-family: 'Fraunces', Georgia, serif !important;
        font-size: 1.85rem !important; font-weight: 700 !important;
        color: #f4f6f9 !important; text-align: center; margin: 0 0 8px 0 !important;
        letter-spacing: -0.03em;
    }
    .aq-gate-sub {
        text-align: center; color: #8b9bb4 !important; font-size: 0.95rem !important;
        margin: 0 0 22px 0 !important; line-height: 1.45;
    }
    .aq-divider {
        display: flex; align-items: center; gap: 12px; margin: 14px 0 8px;
        color: #6b7c94; font-size: 0.78rem; font-family: 'Inter', sans-serif;
    }
    .aq-divider::before, .aq-divider::after {
        content: ""; flex: 1; height: 1px; background: rgba(255,255,255,0.1);
    }
    .aq-hint {
        text-align: center; font-size: 0.78rem; color: #6b7c94 !important; margin-top: 14px !important;
    }
    .aq-footer-nav {
        display: flex; justify-content: center; flex-wrap: wrap; gap: 18px;
        margin-top: 28px; padding-top: 8px;
        font-family: 'Inter', sans-serif; font-size: 0.78rem; color: #6b7c94;
    }

    /* Tabs */
    div.stTabs [data-baseweb="tab-list"] {
        display: flex; justify-content: space-around;
        background: rgba(13, 19, 32, 0.9);
        border: 1px solid var(--aq-border);
        border-radius: 12px;
        padding: 5px;
        margin-bottom: 16px;
        gap: 4px;
    }
    div.stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #8b9bb4 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.82rem;
        padding: 10px 12px;
        border-radius: 8px;
    }
    div.stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #1a3a6b, #0a1f44) !important;
        color: #f4f6f9 !important;
        box-shadow: 0 1px 0 rgba(255,255,255,0.08) inset;
    }
    div.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

    /* Inputs / buttons */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #0a0f1a !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        color: #f4f6f9 !important;
    }
    .stButton > button[kind="primary"], .stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(180deg, #1e4a82, #0a1f44) !important;
        border: 1px solid rgba(255,255,255,0.14) !important;
        color: #fff !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stButton > button[kind="secondary"], .stButton > button[data-testid="baseButton-secondary"] {
        background: rgba(17,24,39,0.8) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #c5d0e0 !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ── Session state ──
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "active_tf" not in st.session_state:
    st.session_state.active_tf = "1M"
if "gate_error" not in st.session_state:
    st.session_state.gate_error = ""

company_ticker_map = {
    "TESLA": "TSLA", "ELON MUSK": "TSLA", "NVIDIA": "NVDA", "JENSEN HUANG": "NVDA",
    "APPLE": "AAPL", "IPHONE": "AAPL", "AMAZON": "AMZN", "JEFF BEZOS": "AMZN",
    "MICROSOFT": "MSFT", "BILL GATES": "MSFT", "META": "META", "FACEBOOK": "META",
    "MARK ZUCKERBERG": "META", "COSTCO": "COST", "AMD": "AMD", "NETFLIX": "NFLX",
    "GOOGLE": "GOOGL", "ALPHABET": "GOOGL"
}


def render_gate():
    """Polistocks-style centered sign-in gate (session_state only)."""
    st.markdown("""
        <div class="aq-gate-wrap">
            <div class="aq-gate-mark">A</div>
            <h1 class="aq-gate-title">Welcome back</h1>
            <p class="aq-gate-sub">Track signals, whale ledgers, and market news in your AlphaQuant terminal.</p>
        </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.35, 1])
    with col_c:
        st.markdown('<div class="aq-gate-card">', unsafe_allow_html=True)

        if st.button("Continue as guest explorer", use_container_width=True, type="secondary", key="guest_btn"):
            st.session_state.authenticated = True
            st.session_state.gate_error = ""
            st.rerun()

        st.markdown('<div class="aq-divider">or</div>', unsafe_allow_html=True)

        with st.form("aq_auth_form", clear_on_submit=False):
            email = st.text_input("Email", placeholder="you@firm.com", key="gate_email")
            password = st.text_input(
                "Access code",
                type="password",
                placeholder="Enter access code",
                key="gate_password",
                help=f"Demo code: {ACCESS_CODE}",
            )
            submitted = st.form_submit_button("Sign in", use_container_width=True, type="primary")

            if submitted:
                email_ok = bool(email and "@" in email and "." in email.split("@")[-1])
                code_ok = (password or "").strip().lower() == ACCESS_CODE
                if email_ok and code_ok:
                    st.session_state.authenticated = True
                    st.session_state.gate_error = ""
                    st.rerun()
                else:
                    st.session_state.gate_error = "Use a valid email and the demo access code."

        if st.session_state.gate_error:
            st.error(st.session_state.gate_error)

        st.markdown(
            f'<p class="aq-hint">New here? Use any email + access code <b style="color:#93c5fd">{ACCESS_CODE}</b></p>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="aq-footer-nav">
            <span>Explore</span><span>Signals</span><span>Investors</span><span>News</span><span>Help</span>
        </div>
    """, unsafe_allow_html=True)


def get_connection():
    if "postgres" in st.secrets:
        db_secrets = st.secrets["postgres"]
        host = db_secrets["host"]
        password = db_secrets["password"]
    else:
        host = "ep-mute-tooth-adtz6q0f.c-2.us-east-1.aws.neon.tech"
        password = "npg_AYovDKM7VL8s"
    return psycopg2.connect(
        host=host, port="5432", user="neondb_owner",
        password=password, database="neondb", sslmode="require",
    )


# ── Auth gate (unlocks main terminal) ──
if not st.session_state.authenticated:
    render_gate()
    st.stop()

# ── Main terminal ──
st.markdown("""
    <div class="aq-brand-bar">
        <div class="aq-brand">
            <div class="aq-mark">A</div>
            <div>
                <div class="aq-brand-name">AlphaQuant</div>
                <div class="aq-brand-sub">Core Terminal</div>
            </div>
        </div>
        <div class="aq-pill">Live markets · Institutional view</div>
    </div>
""", unsafe_allow_html=True)

connection = get_connection()

cursor = connection.cursor()
try:
    cursor.execute("SELECT name FROM trader_registry ORDER BY annual_return DESC;")
    whale_names_list = [row[0] for row in cursor.fetchall()]
except Exception:
    whale_names_list = ["Nancy Pelosi", "Warren Buffett", "Michael Burry", "Bill Ackman", "Stanley Druckenmiller"]
cursor.close()

tab_explore, tab_signals, tab_whales, tab_news, tab_help = st.tabs([
    "EXPLORE",
    "SIGNALS",
    "INVESTORS",
    "READ",
    "HELP",
])

with tab_explore:
    st.markdown(
        '<div class="aq-card"><h1>Market Discovery</h1>'
        '<p>Search by ticker or company name. Filter horizons with live color signals.</p></div>',
        unsafe_allow_html=True,
    )

    search_input = st.text_input("Ticker or company", value="TSLA", key="univ_search_input").upper().strip()

    target_ticker = search_input
    for key, value in company_ticker_map.items():
        if key in search_input:
            target_ticker = value
            break

    if target_ticker:
        try:
            ticker_obj = yf.Ticker(target_ticker)
            ticker_info = ticker_obj.info

            st.markdown("##### Chart timeframe")
            tf_col1, tf_col2, tf_col3, tf_col4, tf_col5 = st.columns(5)
            tf_config = {"1D": ("1d", "5m"), "1W": ("5d", "30m"), "1M": ("1mo", "1d"), "1Y": ("1y", "1d"), "MAX": ("max", "1wk")}

            with tf_col1:
                if st.button("1 DAY", use_container_width=True, type="primary" if st.session_state.active_tf == "1D" else "secondary"):
                    st.session_state.active_tf = "1D"
                    st.rerun()
            with tf_col2:
                if st.button("1 WEEK", use_container_width=True, type="primary" if st.session_state.active_tf == "1W" else "secondary"):
                    st.session_state.active_tf = "1W"
                    st.rerun()
            with tf_col3:
                if st.button("1 MONTH", use_container_width=True, type="primary" if st.session_state.active_tf == "1M" else "secondary"):
                    st.session_state.active_tf = "1M"
                    st.rerun()
            with tf_col4:
                if st.button("1 YEAR", use_container_width=True, type="primary" if st.session_state.active_tf == "1Y" else "secondary"):
                    st.session_state.active_tf = "1Y"
                    st.rerun()
            with tf_col5:
                if st.button("LIFETIME", use_container_width=True, type="primary" if st.session_state.active_tf == "MAX" else "secondary"):
                    st.session_state.active_tf = "MAX"
                    st.rerun()

            chosen_p, chosen_i = tf_config[st.session_state.active_tf]
            ticker_history = ticker_obj.history(period=chosen_p, interval=chosen_i)

            if not ticker_history.empty:
                comp_name = ticker_info.get("longName", f"{target_ticker} Equity Profile")
                price_now = ticker_history["Close"].iloc[-1]
                price_start = ticker_history["Close"].iloc[0]
                net_change_pct = ((price_now - price_start) / price_start) * 100

                chart_color = "#10b981" if price_now >= price_start else "#ef4444"
                status_signal = "GAIN" if price_now >= price_start else "LOSS"

                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Company", comp_name)
                with col_m2:
                    st.metric("Live price", f"${price_now:.2f}", f"{net_change_pct:+.2f}%")
                with col_m3:
                    st.metric(f"{st.session_state.active_tf} status", status_signal)

                st.markdown(f"### {target_ticker} · {st.session_state.active_tf}")
                st.line_chart(pd.DataFrame({"Price ($)": ticker_history["Close"]}), color=chart_color)
            else:
                st.error("No price history for this period.")
        except Exception:
            st.error("Market data unavailable or rate-limited. Try again shortly.")

with tab_signals:
    st.markdown(
        '<div class="aq-card"><h1>Quantitative Signals</h1>'
        '<p>Aggregated public asset tracking scores from the research ledger.</p></div>',
        unsafe_allow_html=True,
    )
    query = (
        'SELECT s.ticker AS "Asset Ticker", c.name AS "Company Identity", '
        's.final_score AS "Master Quant Score", s.reasons AS "System Research Notes" '
        "FROM scores s JOIN companies c ON s.ticker = c.ticker ORDER BY s.final_score DESC;"
    )
    df = pd.read_sql_query(query, connection)
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No signal scores available yet.")

with tab_whales:
    st.markdown(
        '<div class="aq-card"><h1>Whale Ledger</h1>'
        '<p>Select a registered trader to open their historical execution sheet.</p></div>',
        unsafe_allow_html=True,
    )

    selected_whale_profile = st.selectbox(
        "Trader profile",
        whale_names_list,
        key="dedicated_whale_tab_selector",
    )

    if selected_whale_profile:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT category, annual_return, trading_style, biography FROM trader_registry WHERE name = %s;",
            (selected_whale_profile,),
        )
        whale_record = cursor.fetchone()
        cursor.close()

        if whale_record:
            cat, ret, style, bio = whale_record
            st.markdown(f"""
                <div class="bio-card">
                    <h3 style="margin:0; color:#f4f6f9; font-family:'Fraunces',serif;">{selected_whale_profile}</h3>
                    <p style="margin:4px 0 10px 0; color:#8b9bb4; font-weight:600; text-transform:uppercase; font-size:0.72rem; letter-spacing:0.06em;">
                        {cat} · {ret}% annualized · {style or "—"}
                    </p>
                    <p style="color:#8b9bb4; font-size:0.95rem; line-height:1.45; margin:0;">{bio}</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"### Execution history · {selected_whale_profile}")
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
                df_target_history["Action Type"] = df_target_history["Action Type"].apply(
                    lambda x: f"BUY · {x}" if "Buy" in str(x) or "Purchase" in str(x) else f"SELL · {x}"
                )
                st.dataframe(
                    df_target_history,
                    use_container_width=True,
                    hide_index=True,
                    column_config={"Est Allocation Value ($)": st.column_config.NumberColumn(format="$%d")},
                )
            else:
                st.info("No transactional filings for this profile.")

with tab_news:
    st.markdown(
        '<div class="aq-card"><h1>Market News</h1>'
        '<p>Live headlines from MarketWatch.</p></div>',
        unsafe_allow_html=True,
    )
    feed = feedparser.parse("https://marketwatch.com")
    if not feed.entries:
        st.info("No live headlines available right now.")
    else:
        for entry in feed.entries[:20]:
            st.markdown(
                f'<div class="news-box"><h4 style="margin:0;"><a href="{entry.get("link","#")}" target="_blank">'
                f'{entry.get("title","")}</a></h4>'
                f'<p style="font-size:0.78rem; color:#8b9bb4; margin-top:4px;">MarketWatch</p></div>',
                unsafe_allow_html=True,
            )

with tab_help:
    st.markdown(
        '<div class="aq-card"><h1>Research Co-Pilot</h1>'
        '<p>Ask about terms, calculations, or trader movements.</p></div>',
        unsafe_allow_html=True,
    )
    user_query = st.text_input("Your question", key="help_ai_input_box", placeholder="e.g. What does annualized return mean?")
    if user_query:
        with st.spinner("Analyzing..."):
            try:
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional hedge fund analyst. Give direct, precise financial answers without filler dialogue.",
                        },
                        {"role": "user", "content": user_query},
                    ],
                )
                st.markdown(
                    f'<div class="bio-card" style="border-left-color:#10b981;"><p style="color:#f4f6f9; font-size:0.95rem; line-height:1.5;">{response}</p></div>',
                    unsafe_allow_html=True,
                )
            except Exception:
                st.markdown(
                    '<div class="bio-card" style="border-left-color:#ef4444;"><p style="color:#f4f6f9;">Co-pilot busy. Re-submit your question.</p></div>',
                    unsafe_allow_html=True,
                )

connection.close()
