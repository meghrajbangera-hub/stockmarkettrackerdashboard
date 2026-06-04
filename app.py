import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

st.set_page_config(
    page_title="Nifty 50 + Top 20 Live Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0e0f13; }
    .main .block-container { padding: 1rem 1.5rem; }
    .metric-card {
        background: #151820;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 10px;
    }
    .pos { color: #22c55e; }
    .neg { color: #ef4444; }
    .stDataFrame { border-radius: 10px; }
    div[data-testid="stMetricValue"] { font-size: 1.4rem; }
    .stSelectbox > div, .stTextInput > div { background: #151820; }
    h1, h2, h3 { color: #e8eaf2; }
    .stMarkdown p { color: #8b90a7; }
</style>
""", unsafe_allow_html=True)

NIFTY50_TICKERS = {
    "Reliance Industries": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "ITC": "ITC.NS",
    "SBI": "SBIN.NS",
    "L&T": "LT.NS",
    "HCL Technologies": "HCLTECH.NS",
    "Axis Bank": "AXISBANK.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "Sun Pharma": "SUNPHARMA.NS",
    "Wipro": "WIPRO.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "UltraTech Cement": "ULTRACEMCO.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "Titan Company": "TITAN.NS",
    "Nestle India": "NESTLEIND.NS",
    "NTPC": "NTPC.NS",
    "Power Grid": "POWERGRID.NS",
    "Coal India": "COALINDIA.NS",
    "ONGC": "ONGC.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Tata Steel": "TATASTEEL.NS",
    "Hindalco": "HINDALCO.NS",
    "JSW Steel": "JSWSTEEL.NS",
    "M&M": "M&M.NS",
    "Dr Reddys Lab": "DRREDDY.NS",
    "Cipla": "CIPLA.NS",
    "Divis Labs": "DIVISLAB.NS",
    "Tech Mahindra": "TECHM.NS",
    "HUL": "HINDUNILVR.NS",
    "Bajaj Auto": "BAJAJ-AUTO.NS",
    "Eicher Motors": "EICHERMOT.NS",
    "Hero MotoCorp": "HEROMOTOCO.NS",
    "Grasim": "GRASIM.NS",
    "BEL": "BEL.NS",
    "Adani Ports": "ADANIPORTS.NS",
    "Adani Enterprises": "ADANIENT.NS",
    "Shriram Finance": "SHRIRAMFIN.NS",
    "SBI Life Insurance": "SBILIFE.NS",
    "HDFC Life": "HDFCLIFE.NS",
    "Trent": "TRENT.NS",
    "Jio Financial": "JIOFIN.NS",
    "Zomato": "ZOMATO.NS",
    "BPCL": "BPCL.NS",
    "IndusInd Bank": "INDUSINDBK.NS",
    "Britannia": "BRITANNIA.NS",
}

TOP20_TICKERS = {
    "Dixon Technologies": "DIXON.NS",
    "Varun Beverages": "VBL.NS",
    "Polycab India": "POLYCAB.NS",
    "IRFC": "IRFC.NS",
    "Zydus Lifesciences": "ZYDUSLIFE.NS",
    "Pidilite Industries": "PIDILITIND.NS",
    "Dalmia Bharat": "DALBHARAT.NS",
    "Persistent Systems": "PERSISTENT.NS",
    "Torrent Power": "TORNTPOWER.NS",
    "Cholamandalam": "CHOLAFIN.NS",
    "Max Healthcare": "MAXHEALTH.NS",
    "Avenue Supermarts": "DMART.NS",
    "Cummins India": "CUMMINSIND.NS",
    "ABB India": "ABB.NS",
    "Tata Consumer": "TATACONSUM.NS",
    "Info Edge (Naukri)": "NAUKRI.NS",
    "Muthoot Finance": "MUTHOOTFIN.NS",
    "KPIT Technologies": "KPITTECH.NS",
    "Astral": "ASTRAL.NS",
    "Page Industries": "PAGEIND.NS",
}

SECTORS = {
    "RELIANCE.NS": "Energy", "TCS.NS": "IT", "HDFCBANK.NS": "Banking",
    "INFY.NS": "IT", "ICICIBANK.NS": "Banking", "BHARTIARTL.NS": "Telecom",
    "ITC.NS": "FMCG", "SBIN.NS": "Banking", "LT.NS": "Infra",
    "HCLTECH.NS": "IT", "AXISBANK.NS": "Banking", "BAJFINANCE.NS": "Finance",
    "KOTAKBANK.NS": "Banking", "SUNPHARMA.NS": "Pharma", "WIPRO.NS": "IT",
    "MARUTI.NS": "Auto", "ULTRACEMCO.NS": "Cement", "ASIANPAINT.NS": "Consumer",
    "TITAN.NS": "Consumer", "NESTLEIND.NS": "FMCG", "NTPC.NS": "Energy",
    "POWERGRID.NS": "Infra", "COALINDIA.NS": "Energy", "ONGC.NS": "Energy",
    "TATAMOTORS.NS": "Auto", "TATASTEEL.NS": "Metals", "HINDALCO.NS": "Metals",
    "JSWSTEEL.NS": "Metals", "M&M.NS": "Auto", "DRREDDY.NS": "Pharma",
    "CIPLA.NS": "Pharma", "DIVISLAB.NS": "Pharma", "TECHM.NS": "IT",
    "HINDUNILVR.NS": "FMCG", "BAJAJ-AUTO.NS": "Auto", "EICHERMOT.NS": "Auto",
    "HEROMOTOCO.NS": "Auto", "GRASIM.NS": "Cement", "BEL.NS": "Infra",
    "ADANIPORTS.NS": "Infra", "ADANIENT.NS": "Infra", "SHRIRAMFIN.NS": "Finance",
    "SBILIFE.NS": "Finance", "HDFCLIFE.NS": "Finance", "TRENT.NS": "Consumer",
    "JIOFIN.NS": "Finance", "ZOMATO.NS": "Consumer", "BPCL.NS": "Energy",
    "INDUSINDBK.NS": "Banking", "BRITANNIA.NS": "FMCG",
    "DIXON.NS": "Consumer", "VBL.NS": "FMCG", "POLYCAB.NS": "Infra",
    "IRFC.NS": "Finance", "ZYDUSLIFE.NS": "Pharma", "PIDILITIND.NS": "Consumer",
    "DALBHARAT.NS": "Cement", "PERSISTENT.NS": "IT", "TORNTPOWER.NS": "Energy",
    "CHOLAFIN.NS": "Finance", "MAXHEALTH.NS": "Pharma", "DMART.NS": "Consumer",
    "CUMMINSIND.NS": "Infra", "ABB.NS": "Infra", "TATACONSUM.NS": "FMCG",
    "NAUKRI.NS": "IT", "MUTHOOTFIN.NS": "Finance", "KPITTECH.NS": "IT",
    "ASTRAL.NS": "Infra", "PAGEIND.NS": "Consumer",
}

@st.cache_data(ttl=300)
def fetch_stock_data(tickers_dict, period="5y"):
    results = []
    ticker_list = list(tickers_dict.values())
    try:
        data = yf.download(ticker_list, period=period, progress=False, auto_adjust=True)
        close = data["Close"] if "Close" in data else data
        for name, ticker in tickers_dict.items():
            try:
                if ticker not in close.columns:
                    continue
                prices = close[ticker].dropna()
                if len(prices) < 2:
                    continue
                cmp = round(prices.iloc[-1], 2)
                prev = prices.iloc[-2]
                chg1d = round(((cmp - prev) / prev) * 100, 2)
                w1 = prices.iloc[-6] if len(prices) >= 6 else prices.iloc[0]
                m1 = prices.iloc[-22] if len(prices) >= 22 else prices.iloc[0]
                y1 = prices.iloc[-252] if len(prices) >= 252 else prices.iloc[0]
                y5 = prices.iloc[0]
                chg1w = round(((cmp - w1) / w1) * 100, 2)
                chg1m = round(((cmp - m1) / m1) * 100, 2)
                chg1y = round(((cmp - y1) / y1) * 100, 2)
                chg5y = round(((cmp - y5) / y5) * 100, 2)
                results.append({
                    "Name": name,
                    "Ticker": ticker.replace(".NS", ""),
                    "Sector": SECTORS.get(ticker, "Other"),
                    "CMP (₹)": cmp,
                    "1D %": chg1d,
                    "1W %": chg1w,
                    "1M %": chg1m,
                    "1Y %": chg1y,
                    "5Y %": chg5y,
                    "_ticker": ticker,
                    "_prices": prices,
                })
            except Exception:
                continue
    except Exception as e:
        st.error(f"Error fetching data: {e}")
    return results

@st.cache_data(ttl=300)
def fetch_index_data():
    try:
        nifty = yf.Ticker("^NSEI")
        hist = nifty.history(period="2d")
        if len(hist) >= 2:
            curr = hist["Close"].iloc[-1]
            prev = hist["Close"].iloc[-2]
            chg = round(((curr - prev) / prev) * 100, 2)
            return round(curr, 2), chg
    except:
        pass
    return None, None

def signal(row):
    score = 0
    if row["1D %"] > 0.5: score += 1
    if row["1W %"] > 1: score += 1
    if row["1M %"] > 3: score += 1
    if row["1Y %"] > 10: score += 2
    if row["1Y %"] < -25: score -= 3
    if row["1M %"] < -5: score -= 2
    if row["1D %"] < -1.5: score -= 1
    if score >= 3: return "BUY"
    if score <= -3: return "SELL"
    if score >= 1: return "WATCH"
    return "HOLD"

def color_pct(val):
    if val > 0:
        return f'<span style="color:#22c55e;font-weight:500">+{val:.2f}%</span>'
    elif val < 0:
        return f'<span style="color:#ef4444;font-weight:500">{val:.2f}%</span>'
    return f'<span style="color:#8b90a7">{val:.2f}%</span>'

def signal_badge(s):
    colors = {"BUY": ("#22c55e", "#0a2010"), "HOLD": ("#f59e0b", "#1a1200"),
              "WATCH": ("#3b82f6", "#0a1020"), "SELL": ("#ef4444", "#1a0808")}
    c, bg = colors.get(s, ("#8b90a7", "#151820"))
    return f'<span style="background:{bg};color:{c};padding:2px 10px;border-radius:20px;font-size:12px;font-weight:600;border:1px solid {c}40">{s}</span>'

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    auto_refresh = st.toggle("Auto-refresh (5 min)", value=True)
    show_top20 = st.toggle("Include Top 20", value=True)
    period_map = {"1 Month": "1mo", "3 Months": "3mo", "6 Months": "6mo",
                  "1 Year": "1y", "2 Years": "2y", "5 Years": "5y"}
    chart_period = st.selectbox("Chart period", list(period_map.keys()), index=5)
    sector_filter = st.selectbox("Filter by sector", ["All"] + sorted(set(SECTORS.values())))
    signal_filter = st.selectbox("Filter by signal", ["All", "BUY", "HOLD", "WATCH", "SELL"])
    sort_col = st.selectbox("Sort by", ["1D %", "1W %", "1M %", "1Y %", "5Y %", "CMP (₹)"])
    sort_asc = st.toggle("Sort ascending", value=False)
    st.markdown("---")
    st.markdown("**⚠️ Disclaimer**")
    st.markdown("Data from Yahoo Finance. Signals are algorithmic — not financial advice. Consult a SEBI-registered advisor.", unsafe_allow_html=False)
    st.markdown(f"*Last updated: {datetime.now().strftime('%d %b %Y, %H:%M')}*")

st.markdown("# 📈 Nifty 50 + Top 20 Live Tracker")
st.markdown(f"*Live data via Yahoo Finance · {datetime.now().strftime('%A, %d %B %Y')}*")

nifty_val, nifty_chg = fetch_index_data()

with st.spinner("Fetching live prices..."):
    nifty_data = fetch_stock_data(NIFTY50_TICKERS, period_map[chart_period])
    top20_data = fetch_stock_data(TOP20_TICKERS, period_map[chart_period]) if show_top20 else []

all_data = nifty_data + top20_data
for row in all_data:
    row["Signal"] = signal(row)

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    if nifty_val:
        st.metric("Nifty 50", f"₹{nifty_val:,.2f}", f"{nifty_chg:+.2f}%")
    else:
        st.metric("Nifty 50", "–", "–")
with c2:
    buys = sum(1 for r in all_data if r["Signal"] == "BUY")
    st.metric("Buy signals", buys, f"of {len(all_data)} stocks")
with c3:
    gainers = sum(1 for r in all_data if r["1D %"] > 0)
    st.metric("Today's gainers", gainers)
with c4:
    losers = sum(1 for r in all_data if r["1D %"] < 0)
    st.metric("Today's losers", losers)
with c5:
    avg1d = round(sum(r["1D %"] for r in all_data) / len(all_data), 2) if all_data else 0
    st.metric("Avg 1D move", f"{avg1d:+.2f}%")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📋 Watchlist", "📊 Charts", "⭐ Recommendations", "🔍 Stock Deep Dive"])

with tab1:
    search = st.text_input("Search company or ticker", placeholder="e.g. TCS, Infosys, Banking...")
    display = all_data.copy()
    if search:
        display = [r for r in display if search.lower() in r["Name"].lower() or search.lower() in r["Ticker"].lower()]
    if sector_filter != "All":
        display = [r for r in display if r["Sector"] == sector_filter]
    if signal_filter != "All":
        display = [r for r in display if r["Signal"] == signal_filter]
    display.sort(key=lambda r: r[sort_col], reverse=not sort_asc)

    st.markdown(f"**Showing {len(display)} of {len(all_data)} stocks**")

    if display:
        header_cols = ["Name", "Ticker", "Sector", "CMP (₹)", "1D %", "1W %", "1M %", "1Y %", "5Y %", "Signal"]
        header_html = "".join(f'<th style="padding:8px 12px;font-size:11px;font-weight:600;letter-spacing:0.5px;text-transform:uppercase;color:#8b90a7;background:#1c1f2b;border-bottom:1px solid rgba(255,255,255,0.07);text-align:left">{h}</th>' for h in header_cols)
        rows_html = ""
        for i, r in enumerate(display):
            bg = "#151820" if i % 2 == 0 else "#1c1f2b"
            is_top20 = r["_ticker"] + ".NS" in TOP20_TICKERS.values() or r["_ticker"] in [t.replace(".NS","") for t in TOP20_TICKERS.values()]
            name_cell = r["Name"] + (' <span style="background:#2d1b6b;color:#a78bfa;padding:1px 5px;border-radius:4px;font-size:10px">Top20</span>' if r["_ticker"] not in [t.replace(".NS","") for t in NIFTY50_TICKERS.values()] else "")
            rows_html += f"""<tr style="background:{bg}">
                <td style="padding:8px 12px;color:#e8eaf2">{name_cell}</td>
                <td style="padding:8px 12px;color:#8b90a7;font-family:monospace;font-size:12px">{r["Ticker"]}</td>
                <td style="padding:8px 12px"><span style="background:#242838;color:#8b90a7;padding:2px 7px;border-radius:4px;font-size:11px">{r["Sector"]}</span></td>
                <td style="padding:8px 12px;color:#e8eaf2;font-weight:500;font-family:monospace">₹{r["CMP (₹)"]:,.2f}</td>
                <td style="padding:8px 12px">{color_pct(r["1D %"])}</td>
                <td style="padding:8px 12px">{color_pct(r["1W %"])}</td>
                <td style="padding:8px 12px">{color_pct(r["1M %"])}</td>
                <td style="padding:8px 12px">{color_pct(r["1Y %"])}</td>
                <td style="padding:8px 12px">{color_pct(r["5Y %"])}</td>
                <td style="padding:8px 12px">{signal_badge(r["Signal"])}</td>
            </tr>"""
        table_html = f'<div style="overflow-x:auto;border-radius:10px;border:1px solid rgba(255,255,255,0.07)"><table style="width:100%;border-collapse:collapse"><thead><tr>{header_html}</tr></thead><tbody>{rows_html}</tbody></table></div>'
        st.markdown(table_html, unsafe_allow_html=True)

with tab2:
    if all_data:
        col1, col2 = st.columns(2)
        with col1:
            selected_stocks = st.multiselect(
                "Compare stocks (5-year chart)",
                options=[r["Name"] for r in all_data],
                default=["TCS", "ICICI Bank", "Bharti Airtel"] if len(all_data) > 3 else [all_data[0]["Name"]]
            )
        with col2:
            normalize = st.toggle("Normalize to 100 (indexed comparison)", value=True)

        if selected_stocks:
            fig = go.Figure()
            colors = ["#3b82f6","#22c55e","#f59e0b","#ef4444","#a78bfa","#f97316","#14b8a6","#ec4899"]
            for i, name in enumerate(selected_stocks):
                row = next((r for r in all_data if r["Name"] == name), None)
                if row and "_prices" in row:
                    prices = row["_prices"]
                    y = (prices / prices.iloc[0] * 100).round(2) if normalize else prices.round(2)
                    fig.add_trace(go.Scatter(
                        x=prices.index, y=y,
                        name=name, line=dict(color=colors[i % len(colors)], width=2),
                        hovertemplate=f"<b>{name}</b><br>%{{x|%d %b %Y}}<br>{'Index: ' if normalize else '₹'}%{{y:.2f}}<extra></extra>"
                    ))
            fig.update_layout(
                paper_bgcolor="#151820", plot_bgcolor="#0e0f13",
                font=dict(color="#8b90a7", family="DM Sans"),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)", showgrid=True),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)", showgrid=True,
                           tickprefix="" if normalize else "₹"),
                legend=dict(bgcolor="#151820", bordercolor="rgba(255,255,255,0.07)", borderwidth=1),
                hovermode="x unified", margin=dict(l=0,r=0,t=20,b=0), height=380
            )
            st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            sects = {}
            for r in all_data:
                sects[r["Sector"]] = sects.get(r["Sector"], 0) + 1
            fig2 = px.pie(values=list(sects.values()), names=list(sects.keys()),
                         title="Sector distribution", hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Set3)
            fig2.update_layout(paper_bgcolor="#151820", plot_bgcolor="#0e0f13",
                               font=dict(color="#8b90a7"), height=300, margin=dict(t=40,b=0,l=0,r=0))
            st.plotly_chart(fig2, use_container_width=True)

        with c2:
            sorted_1y = sorted(all_data, key=lambda r: r["1Y %"], reverse=True)
            top5 = sorted_1y[:5]
            bot5 = sorted_1y[-5:]
            items = top5 + bot5
            fig3 = go.Figure(go.Bar(
                x=[r["1Y %"] for r in items],
                y=[r["Ticker"] for r in items],
                orientation="h",
                marker_color=["#22c55e" if r["1Y %"] >= 0 else "#ef4444" for r in items],
                text=[f"{r['1Y %']:+.1f}%" for r in items],
                textposition="outside"
            ))
            fig3.update_layout(
                title="Top 5 gainers vs losers (1Y)", paper_bgcolor="#151820",
                plot_bgcolor="#0e0f13", font=dict(color="#8b90a7"),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)", ticksuffix="%"),
                yaxis=dict(autorange="reversed"), height=300, margin=dict(t=40,b=0,l=60,r=60)
            )
            st.plotly_chart(fig3, use_container_width=True)

with tab3:
    buys_list = sorted([r for r in all_data if r["Signal"] == "BUY"], key=lambda r: r["1Y %"], reverse=True)
    watches_list = sorted([r for r in all_data if r["Signal"] == "WATCH"], key=lambda r: r["1D %"], reverse=True)
    holds_list = [r for r in all_data if r["Signal"] == "HOLD"]
    sells_list = [r for r in all_data if r["Signal"] == "SELL"]

    st.markdown(f"### 🟢 Buy signals ({len(buys_list)} stocks)")
    for r in buys_list[:8]:
        with st.container():
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.markdown(f"**{r['Name']}** `{r['Ticker']}` · {r['Sector']}")
                reasons = []
                if r["1Y %"] < -15: reasons.append(f"Down {abs(r['1Y %']):.0f}% in 1Y — potential value")
                if r["1D %"] > 0: reasons.append(f"Positive momentum today (+{r['1D %']:.1f}%)")
                if r["1M %"] > 3: reasons.append(f"Strong 1-month trend (+{r['1M %']:.1f}%)")
                if r["5Y %"] > 100: reasons.append(f"Proven 5Y compounder (+{r['5Y %']:.0f}%)")
                st.caption(" · ".join(reasons) if reasons else "Strong momentum across timeframes")
            with c2:
                chg_color = "normal" if r["1D %"] >= 0 else "inverse"
                st.metric("Today", f"{r['1D %']:+.2f}%")
            with c3:
                st.metric("1Y", f"{r['1Y %']:+.1f}%")
            st.divider()

    if watches_list:
        st.markdown(f"### 🔵 Watch list ({len(watches_list)} stocks)")
        wcols = st.columns(min(len(watches_list), 3))
        for i, r in enumerate(watches_list[:6]):
            with wcols[i % 3]:
                st.markdown(f"**{r['Name']}**")
                st.caption(f"`{r['Ticker']}` · {r['Sector']}")
                st.markdown(f"Today: {r['1D %']:+.2f}% | 1Y: {r['1Y %']:+.1f}%")

    if sells_list:
        st.markdown(f"### 🔴 Caution signals ({len(sells_list)} stocks)")
        for r in sells_list:
            st.markdown(f"⚠️ **{r['Name']}** — 1D: {r['1D %']:+.2f}%, 1M: {r['1M %']:+.1f}%, 1Y: {r['1Y %']:+.1f}%")

    st.info("⚠️ Signals are computed algorithmically from price momentum. Not financial advice.", icon="ℹ️")

with tab4:
    selected = st.selectbox("Select a stock for deep dive", options=[r["Name"] for r in all_data])
    stock_row = next((r for r in all_data if r["Name"] == selected), None)
    if stock_row:
        ticker_obj = yf.Ticker(stock_row["_ticker"])
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Current Price", f"₹{stock_row['CMP (₹)']:,.2f}", f"{stock_row['1D %']:+.2f}%")
        with c2: st.metric("1 Week", f"{stock_row['1W %']:+.2f}%")
        with c3: st.metric("1 Year", f"{stock_row['1Y %']:+.1f}%")
        with c4: st.metric("5 Year", f"{stock_row['5Y %']:+.0f}%")

        prices = stock_row["_prices"]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=prices.index, y=prices.round(2),
            fill="tozeroy", fillcolor="rgba(59,130,246,0.08)",
            line=dict(color="#3b82f6", width=2),
            hovertemplate="₹%{y:,.2f}<br>%{x|%d %b %Y}<extra></extra>"
        ))
        fig.update_layout(
            paper_bgcolor="#151820", plot_bgcolor="#0e0f13",
            font=dict(color="#8b90a7"), height=320,
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickprefix="₹"),
            margin=dict(l=0,r=0,t=10,b=0), showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

        try:
            info = ticker_obj.info
            st.markdown("#### Company info")
            cc1, cc2, cc3, cc4 = st.columns(4)
            with cc1: st.metric("Market Cap", f"₹{info.get('marketCap',0)/1e12:.2f}T" if info.get('marketCap') else "–")
            with cc2: st.metric("P/E Ratio", f"{info.get('trailingPE', 0):.1f}x" if info.get('trailingPE') else "–")
            with cc3: st.metric("52W High", f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}" if info.get('fiftyTwoWeekHigh') else "–")
            with cc4: st.metric("52W Low", f"₹{info.get('fiftyTwoWeekLow', 0):,.2f}" if info.get('fiftyTwoWeekLow') else "–")
            if info.get("longBusinessSummary"):
                with st.expander("About the company"):
                    st.write(info["longBusinessSummary"])
        except:
            st.caption("Additional info unavailable")

if auto_refresh:
    time.sleep(300)
    st.rerun()
