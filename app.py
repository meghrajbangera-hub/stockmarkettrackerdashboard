import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
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

    /* Fix all text to be clearly visible */
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    p, span, div, label { color: #e8eaf2; }

    /* Metric cards — make values and labels bright */
    div[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 1.5rem !important; font-weight: 700 !important; }
    div[data-testid="stMetricLabel"] { color: #c0c4d8 !important; font-size: 0.85rem !important; }
    div[data-testid="stMetricDelta"] { font-size: 0.9rem !important; }

    /* Sidebar text */
    section[data-testid="stSidebar"] { background-color: #151820; }
    section[data-testid="stSidebar"] * { color: #e8eaf2 !important; }

    /* Tab labels */
    button[data-baseweb="tab"] { color: #c0c4d8 !important; font-size: 14px !important; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #ffffff !important; }

    /* Input fields */
    input, select, textarea { color: #ffffff !important; background-color: #1c1f2b !important; }

    /* Caption text */
    .stCaption, small { color: #a0a4b8 !important; }

    /* General text color boost */
    .stMarkdown, .stText { color: #e8eaf2 !important; }

    /* Dropdown / selectbox fix */
    div[data-baseweb="select"] * { color: #111111 !important; background-color: #ffffff !important; }
    div[data-baseweb="select"] input { color: #111111 !important; }
    div[data-baseweb="popover"] * { color: #111111 !important; background-color: #ffffff !important; }
    ul[data-baseweb="menu"] li { color: #111111 !important; font-size: 14px !important; font-weight: 500 !important; }
    ul[data-baseweb="menu"] li:hover { background-color: #f0f4ff !important; }
    div[data-baseweb="select"] div { color: #111111 !important; }

    /* Text input fix */
    div[data-baseweb="input"] input { color: #111111 !important; background-color: #ffffff !important; }

    /* Sidebar selects stay light on dark */
    section[data-testid="stSidebar"] div[data-baseweb="select"] * { color: #e8eaf2 !important; background-color: #1c1f2b !important; }
</style>
""", unsafe_allow_html=True)

NIFTY50_TICKERS = {
    "Reliance Industries": "RELIANCE.NS", "TCS": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS", "Infosys": "INFY.NS",
    "ICICI Bank": "ICICIBANK.NS", "Bharti Airtel": "BHARTIARTL.NS",
    "ITC": "ITC.NS", "SBI": "SBIN.NS", "L&T": "LT.NS",
    "HCL Technologies": "HCLTECH.NS", "Axis Bank": "AXISBANK.NS",
    "Bajaj Finance": "BAJFINANCE.NS", "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "Sun Pharma": "SUNPHARMA.NS", "Wipro": "WIPRO.NS",
    "Maruti Suzuki": "MARUTI.NS", "UltraTech Cement": "ULTRACEMCO.NS",
    "Asian Paints": "ASIANPAINT.NS", "Titan Company": "TITAN.NS",
    "Nestle India": "NESTLEIND.NS", "NTPC": "NTPC.NS",
    "Power Grid": "POWERGRID.NS", "Coal India": "COALINDIA.NS",
    "ONGC": "ONGC.NS", "Tata Motors": "TATAMOTORS.NS",
    "Tata Steel": "TATASTEEL.NS", "Hindalco": "HINDALCO.NS",
    "JSW Steel": "JSWSTEEL.NS", "M&M": "M&M.NS",
    "Dr Reddys Lab": "DRREDDY.NS", "Cipla": "CIPLA.NS",
    "Divis Labs": "DIVISLAB.NS", "Tech Mahindra": "TECHM.NS",
    "HUL": "HINDUNILVR.NS", "Bajaj Auto": "BAJAJ-AUTO.NS",
    "Eicher Motors": "EICHERMOT.NS", "Hero MotoCorp": "HEROMOTOCO.NS",
    "Grasim": "GRASIM.NS", "BEL": "BEL.NS",
    "Adani Ports": "ADANIPORTS.NS", "Adani Enterprises": "ADANIENT.NS",
    "Shriram Finance": "SHRIRAMFIN.NS", "SBI Life Insurance": "SBILIFE.NS",
    "HDFC Life": "HDFCLIFE.NS", "Trent": "TRENT.NS",
    "Jio Financial": "JIOFIN.NS", "Zomato": "ZOMATO.NS",
    "BPCL": "BPCL.NS", "IndusInd Bank": "INDUSINDBK.NS",
    "Britannia": "BRITANNIA.NS",
}

TOP20_TICKERS = {
    "Dixon Technologies": "DIXON.NS", "Varun Beverages": "VBL.NS",
    "Polycab India": "POLYCAB.NS", "IRFC": "IRFC.NS",
    "Zydus Lifesciences": "ZYDUSLIFE.NS", "Pidilite Industries": "PIDILITIND.NS",
    "Dalmia Bharat": "DALBHARAT.NS", "Persistent Systems": "PERSISTENT.NS",
    "Torrent Power": "TORNTPOWER.NS", "Cholamandalam": "CHOLAFIN.NS",
    "Max Healthcare": "MAXHEALTH.NS", "Avenue Supermarts": "DMART.NS",
    "Cummins India": "CUMMINSIND.NS", "ABB India": "ABB.NS",
    "Tata Consumer": "TATACONSUM.NS", "Info Edge (Naukri)": "NAUKRI.NS",
    "Muthoot Finance": "MUTHOOTFIN.NS", "KPIT Technologies": "KPITTECH.NS",
    "Astral": "ASTRAL.NS", "Page Industries": "PAGEIND.NS",
}

SECTORS = {
    "RELIANCE.NS":"Energy","TCS.NS":"IT","HDFCBANK.NS":"Banking","INFY.NS":"IT",
    "ICICIBANK.NS":"Banking","BHARTIARTL.NS":"Telecom","ITC.NS":"FMCG","SBIN.NS":"Banking",
    "LT.NS":"Infra","HCLTECH.NS":"IT","AXISBANK.NS":"Banking","BAJFINANCE.NS":"Finance",
    "KOTAKBANK.NS":"Banking","SUNPHARMA.NS":"Pharma","WIPRO.NS":"IT","MARUTI.NS":"Auto",
    "ULTRACEMCO.NS":"Cement","ASIANPAINT.NS":"Consumer","TITAN.NS":"Consumer",
    "NESTLEIND.NS":"FMCG","NTPC.NS":"Energy","POWERGRID.NS":"Infra","COALINDIA.NS":"Energy",
    "ONGC.NS":"Energy","TATAMOTORS.NS":"Auto","TATASTEEL.NS":"Metals","HINDALCO.NS":"Metals",
    "JSWSTEEL.NS":"Metals","M&M.NS":"Auto","DRREDDY.NS":"Pharma","CIPLA.NS":"Pharma",
    "DIVISLAB.NS":"Pharma","TECHM.NS":"IT","HINDUNILVR.NS":"FMCG","BAJAJ-AUTO.NS":"Auto",
    "EICHERMOT.NS":"Auto","HEROMOTOCO.NS":"Auto","GRASIM.NS":"Cement","BEL.NS":"Infra",
    "ADANIPORTS.NS":"Infra","ADANIENT.NS":"Infra","SHRIRAMFIN.NS":"Finance",
    "SBILIFE.NS":"Finance","HDFCLIFE.NS":"Finance","TRENT.NS":"Consumer",
    "JIOFIN.NS":"Finance","ZOMATO.NS":"Consumer","BPCL.NS":"Energy",
    "INDUSINDBK.NS":"Banking","BRITANNIA.NS":"FMCG","DIXON.NS":"Consumer",
    "VBL.NS":"FMCG","POLYCAB.NS":"Infra","IRFC.NS":"Finance","ZYDUSLIFE.NS":"Pharma",
    "PIDILITIND.NS":"Consumer","DALBHARAT.NS":"Cement","PERSISTENT.NS":"IT",
    "TORNTPOWER.NS":"Energy","CHOLAFIN.NS":"Finance","MAXHEALTH.NS":"Pharma",
    "DMART.NS":"Consumer","CUMMINSIND.NS":"Infra","ABB.NS":"Infra",
    "TATACONSUM.NS":"FMCG","NAUKRI.NS":"IT","MUTHOOTFIN.NS":"Finance",
    "KPITTECH.NS":"IT","ASTRAL.NS":"Infra","PAGEIND.NS":"Consumer",
}

@st.cache_data(ttl=60)
def fetch_all(period="5y"):
    all_tickers = {**NIFTY50_TICKERS, **TOP20_TICKERS}
    results = []
    try:
        data = yf.download(list(all_tickers.values()), period=period, progress=False, auto_adjust=True)
        close = data["Close"]
        for name, ticker in all_tickers.items():
            try:
                prices = close[ticker].dropna()
                if len(prices) < 2: continue
                cmp = round(float(prices.iloc[-1]), 2)
                prev = float(prices.iloc[-2])
                w1 = float(prices.iloc[-6]) if len(prices)>=6 else float(prices.iloc[0])
                m1 = float(prices.iloc[-22]) if len(prices)>=22 else float(prices.iloc[0])
                y1 = float(prices.iloc[-252]) if len(prices)>=252 else float(prices.iloc[0])
                y5 = float(prices.iloc[0])
                results.append({
                    "Name": name,
                    "Ticker": ticker.replace(".NS",""),
                    "Sector": SECTORS.get(ticker,"Other"),
                    "List": "Nifty 50" if ticker in NIFTY50_TICKERS.values() else "Top 20",
                    "CMP (₹)": cmp,
                    "1D %": round(((cmp-prev)/prev)*100,2),
                    "1W %": round(((cmp-w1)/w1)*100,2),
                    "1M %": round(((cmp-m1)/m1)*100,2),
                    "1Y %": round(((cmp-y1)/y1)*100,2),
                    "5Y %": round(((cmp-y5)/y5)*100,2),
                    "_ticker": ticker,
                    "_prices": prices,
                })
            except: continue
    except Exception as e:
        st.error(f"Data fetch error: {e}")
    return results

@st.cache_data(ttl=60)
def fetch_nifty_index():
    try:
        h = yf.Ticker("^NSEI").history(period="2d")
        if len(h)>=2:
            c,p = float(h["Close"].iloc[-1]), float(h["Close"].iloc[-2])
            return round(c,2), round(((c-p)/p)*100,2)
    except: pass
    return None, None

def get_signal(r):
    s = 0
    if r["1D %"] > 0.5: s+=1
    if r["1W %"] > 1: s+=1
    if r["1M %"] > 3: s+=1
    if r["1Y %"] > 10: s+=2
    if r["5Y %"] > 100: s+=1
    if r["1Y %"] < -25: s-=3
    if r["1M %"] < -5: s-=2
    if r["1D %"] < -1.5: s-=1
    if s >= 3: return "🟢 BUY"
    if s <= -3: return "🔴 SELL"
    if s >= 1: return "🔵 WATCH"
    return "🟡 HOLD"

def pct(v):
    c = "#22c55e" if v>0 else "#ef4444" if v<0 else "#8b90a7"
    return f'<span style="color:{c};font-weight:500">{v:+.2f}%</span>'

# ── SIDEBAR ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Controls")
    period_map = {"1 Month":"1mo","3 Months":"3mo","6 Months":"6mo","1 Year":"1y","2 Years":"2y","5 Years":"5y"}
    period = st.selectbox("Chart period", list(period_map.keys()), index=5)
    sector_f = st.selectbox("Sector", ["All"]+sorted(set(SECTORS.values())))
    list_f   = st.selectbox("List", ["All","Nifty 50","Top 20"])
    signal_f = st.selectbox("Signal", ["All","🟢 BUY","🔵 WATCH","🟡 HOLD","🔴 SELL"])
    sort_col = st.selectbox("Sort by", ["1D %","1W %","1M %","1Y %","5Y %","CMP (₹)"])
    sort_asc = st.checkbox("Sort ascending", False)
    auto_ref = st.toggle("Auto-refresh every 5 min", True)
    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%d %b %Y %H:%M')}")
    st.caption("⚠️ Not financial advice. Data: Yahoo Finance.")

# ── HEADER ───────────────────────────────────────────────
st.title("📈 Nifty 50 + Top 20 Live Tracker")
st.caption(f"Live NSE data · Refreshes every 5 min · {datetime.now().strftime('%A, %d %B %Y')}")

nifty_val, nifty_chg = fetch_nifty_index()

with st.spinner("⏳ Fetching live prices for 70 stocks..."):
    data = fetch_all(period_map[period])

for r in data:
    r["Signal"] = get_signal(r)

# ── TOP METRICS ───────────────────────────────────────────
c1,c2,c3,c4,c5,c6 = st.columns(6)
with c1: st.metric("Nifty 50", f"₹{nifty_val:,.0f}" if nifty_val else "–", f"{nifty_chg:+.2f}%" if nifty_chg else "–")
with c2: st.metric("Stocks tracked", len(data))
with c3: st.metric("🟢 Buy signals", sum(1 for r in data if "BUY" in r["Signal"]))
with c4: st.metric("🔵 Watch", sum(1 for r in data if "WATCH" in r["Signal"]))
with c5: st.metric("Today gainers", sum(1 for r in data if r["1D %"]>0))
with c6: st.metric("Today losers",  sum(1 for r in data if r["1D %"]<0))

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📋 Watchlist", "📊 Charts", "⭐ Today's Picks", "🔍 Deep Dive"])

# ── TAB 1: WATCHLIST ─────────────────────────────────────
with tab1:

    st.markdown("#### ⚡ Quick filters")
    quick_options = [
        "📋 All stocks",
        "🚀 Top 20 gainers today",
        "📉 Top 20 losers today (buy opportunity)",
        "🟢 Top 20 Buy signals",
        "⭐ Top 20 by 1-month performance",
        "🏆 Top 20 by 1-year performance",
        "🔥 Top 20 by 5-year performance",
        "💥 Top 20 biggest fall from 52W high",
    ]
    quick = st.selectbox("Show me →", quick_options, index=0)
    st.markdown("---")

    search = st.text_input("🔍 Search", placeholder="Company name or ticker...")

    display = [r for r in data
               if (not search or search.lower() in r["Name"].lower() or search.lower() in r["Ticker"].lower())
               and (sector_f=="All" or r["Sector"]==sector_f)
               and (list_f=="All" or r["List"]==list_f)
               and (signal_f=="All" or r["Signal"]==signal_f)]

    if quick == "🚀 Top 20 gainers today":
        display = sorted(display, key=lambda r: r["1D %"], reverse=True)[:20]
    elif quick == "📉 Top 20 losers today (buy opportunity)":
        display = sorted(display, key=lambda r: r["1D %"])[:20]
    elif quick == "🟢 Top 20 Buy signals":
        buys_only = [r for r in display if "BUY" in r["Signal"]]
        display = sorted(buys_only, key=lambda r: r["1Y %"], reverse=True)[:20]
    elif quick == "⭐ Top 20 by 1-month performance":
        display = sorted(display, key=lambda r: r["1M %"], reverse=True)[:20]
    elif quick == "🏆 Top 20 by 1-year performance":
        display = sorted(display, key=lambda r: r["1Y %"], reverse=True)[:20]
    elif quick == "🔥 Top 20 by 5-year performance":
        display = sorted(display, key=lambda r: r["5Y %"], reverse=True)[:20]
    elif quick == "💥 Top 20 biggest fall from 52W high":
        display = sorted(display, key=lambda r: r["1Y %"])[:20]
    else:
        display.sort(key=lambda r: r[sort_col], reverse=not sort_asc)

    label_map = {
        "🚀 Top 20 gainers today": "🚀 Top 20 stocks gaining the most today",
        "📉 Top 20 losers today (buy opportunity)": "📉 Top 20 stocks down the most today — possible buy opportunities",
        "🟢 Top 20 Buy signals": "🟢 Top 20 stocks with strongest Buy signals right now",
        "⭐ Top 20 by 1-month performance": "⭐ Top 20 best performers this month",
        "🏆 Top 20 by 1-year performance": "🏆 Top 20 best performers this year",
        "🔥 Top 20 by 5-year performance": "🔥 Top 20 best long-term compounders (5 years)",
        "💥 Top 20 biggest fall from 52W high": "💥 Top 20 stocks most beaten down — deep value watch",
    }
    if quick != "📋 All stocks":
        st.markdown(f"**{label_map.get(quick,'')}**")
    st.caption(f"Showing {len(display)} stocks")

    if display:
        rows = ""
        for i,r in enumerate(display):
            bg = "#151820" if i%2==0 else "#1a1e2a"
            top20_tag = '<span style="background:#2d1b6b;color:#a78bfa;padding:1px 5px;border-radius:4px;font-size:10px;margin-left:5px">Top20</span>' if r["List"]=="Top 20" else ""
            sig_colors = {"🟢 BUY":("#22c55e","#0a2010"),"🔵 WATCH":("#3b82f6","#0a1020"),"🟡 HOLD":("#f59e0b","#1a1200"),"🔴 SELL":("#ef4444","#1a0808")}
            sc,sbg = sig_colors.get(r["Signal"],("#8b90a7","#151820"))
            sig_html = f'<span style="background:{sbg};color:{sc};padding:2px 10px;border-radius:20px;font-size:11px;font-weight:600;border:1px solid {sc}40">{r["Signal"]}</span>'
            rows += f"""<tr style="background:{bg}">
              <td style="padding:8px 12px;color:#e8eaf2;font-weight:500">{r["Name"]}{top20_tag}</td>
              <td style="padding:8px 12px;color:#8b90a7;font-family:monospace;font-size:12px">{r["Ticker"]}</td>
              <td style="padding:8px 12px"><span style="background:#242838;color:#8b90a7;padding:2px 7px;border-radius:4px;font-size:11px">{r["Sector"]}</span></td>
              <td style="padding:8px 12px;color:#e8eaf2;font-family:monospace;font-weight:600">₹{r["CMP (₹)"]:,.2f}</td>
              <td style="padding:8px 12px">{pct(r["1D %"])}</td>
              <td style="padding:8px 12px">{pct(r["1W %"])}</td>
              <td style="padding:8px 12px">{pct(r["1M %"])}</td>
              <td style="padding:8px 12px">{pct(r["1Y %"])}</td>
              <td style="padding:8px 12px">{pct(r["5Y %"])}</td>
              <td style="padding:8px 12px">{sig_html}</td>
            </tr>"""
        hdr = "".join(f'<th style="padding:9px 12px;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;color:#8b90a7;background:#1c1f2b;border-bottom:1px solid rgba(255,255,255,0.07);text-align:left">{h}</th>'
                      for h in ["Company","Ticker","Sector","CMP (₹)","1D %","1W %","1M %","1Y %","5Y %","Signal"])
        st.markdown(f'<div style="overflow-x:auto;border-radius:10px;border:1px solid rgba(255,255,255,0.07)"><table style="width:100%;border-collapse:collapse"><thead><tr>{hdr}</tr></thead><tbody>{rows}</tbody></table></div>', unsafe_allow_html=True)

# ── TAB 2: CHARTS ─────────────────────────────────────────
with tab2:
    names = [r["Name"] for r in data]
    sel = st.multiselect("Compare stocks", names, default=names[:3] if len(names)>=3 else names)
    norm = st.toggle("Index to 100 (easier comparison)", True)

    if sel:
        fig = go.Figure()
        colors = ["#3b82f6","#22c55e","#f59e0b","#ef4444","#a78bfa","#f97316","#14b8a6","#ec4899","#84cc16","#06b6d4"]
        for i,name in enumerate(sel):
            row = next((r for r in data if r["Name"]==name),None)
            if row:
                p = row["_prices"]
                y = (p/p.iloc[0]*100).round(2) if norm else p.round(2)
                fig.add_trace(go.Scatter(x=p.index, y=y, name=name,
                    line=dict(color=colors[i%len(colors)],width=2), mode="lines",
                    hovertemplate=f"<b>{name}</b><br>%{{x|%d %b %Y}}<br>{'Index: ' if norm else '₹'}%{{y:.2f}}<extra></extra>"))
        fig.update_layout(paper_bgcolor="#151820",plot_bgcolor="#0e0f13",font=dict(color="#8b90a7"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            legend=dict(bgcolor="#151820",bordercolor="rgba(255,255,255,0.1)",borderwidth=1),
            hovermode="x unified",margin=dict(l=0,r=0,t=20,b=0),height=400)
        st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2)
    with col1:
        sects = {}
        for r in data: sects[r["Sector"]]=sects.get(r["Sector"],0)+1
        fig2 = px.pie(values=list(sects.values()),names=list(sects.keys()),hole=0.4,title="Sector split")
        fig2.update_layout(paper_bgcolor="#151820",font=dict(color="#8b90a7"),height=320,margin=dict(t=40,b=0,l=0,r=0))
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        s1y = sorted(data,key=lambda r:r["1Y %"],reverse=True)
        items = s1y[:5]+s1y[-5:]
        fig3 = go.Figure(go.Bar(x=[r["1Y %"] for r in items],y=[r["Ticker"] for r in items],orientation="h",
            marker_color=["#22c55e" if r["1Y %"]>=0 else "#ef4444" for r in items],
            text=[f"{r['1Y %']:+.1f}%" for r in items],textposition="outside"))
        fig3.update_layout(title="Top 5 gainers & losers (1Y)",paper_bgcolor="#151820",plot_bgcolor="#0e0f13",
            font=dict(color="#8b90a7"),xaxis=dict(gridcolor="rgba(255,255,255,0.05)",ticksuffix="%"),
            yaxis=dict(autorange="reversed"),height=320,margin=dict(t=40,b=0,l=60,r=60))
        st.plotly_chart(fig3, use_container_width=True)

# ── TAB 3: RECOMMENDATIONS ────────────────────────────────
with tab3:
    st.markdown(f"### Today's signals — {datetime.now().strftime('%d %b %Y')}")
    buys   = sorted([r for r in data if "BUY"   in r["Signal"]], key=lambda r:r["1Y %"],reverse=True)
    watches= sorted([r for r in data if "WATCH"  in r["Signal"]], key=lambda r:r["1D %"],reverse=True)
    sells  = [r for r in data if "SELL" in r["Signal"]]

    if buys:
        st.markdown("#### 🟢 Buy signals")
        for r in buys:
            with st.expander(f"{r['Name']}  —  Today: {r['1D %']:+.2f}%  |  1Y: {r['1Y %']:+.1f}%"):
                c1,c2,c3,c4 = st.columns(4)
                c1.metric("CMP",f"₹{r['CMP (₹)']:,.2f}")
                c2.metric("1D",f"{r['1D %']:+.2f}%")
                c3.metric("1M",f"{r['1M %']:+.1f}%")
                c4.metric("1Y",f"{r['1Y %']:+.1f}%")
                reasons=[]
                if r["1Y %"]<-15: reasons.append(f"📉 Down {abs(r['1Y %']):.0f}% in 1Y — potential value buy")
                if r["1D %"]>0: reasons.append(f"📈 Positive momentum today")
                if r["1M %"]>3: reasons.append(f"✅ Strong 1-month trend")
                if r["5Y %"]>100: reasons.append(f"🏆 Proven long-term compounder (+{r['5Y %']:.0f}% in 5Y)")
                for reason in reasons: st.caption(reason)

    if watches:
        st.markdown("#### 🔵 Worth watching")
        cols = st.columns(3)
        for i,r in enumerate(watches[:6]):
            with cols[i%3]:
                st.markdown(f"**{r['Name']}**")
                st.caption(f"`{r['Ticker']}` · {r['Sector']}")
                st.caption(f"1D: {r['1D %']:+.2f}% | 1Y: {r['1Y %']:+.1f}%")

    if sells:
        st.markdown("#### 🔴 Caution")
        for r in sells:
            st.warning(f"**{r['Name']}** — 1D: {r['1D %']:+.2f}%, 1M: {r['1M %']:+.1f}%, 1Y: {r['1Y %']:+.1f}%")

    st.info("Signals are algorithmic — based on price momentum only. Not financial advice.", icon="ℹ️")

# ── TAB 4: DEEP DIVE ──────────────────────────────────────
with tab4:
    pick = st.selectbox("Select a stock", [r["Name"] for r in data])
    row = next((r for r in data if r["Name"]==pick), None)
    if row:
        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("CMP",    f"₹{row['CMP (₹)']:,.2f}", f"{row['1D %']:+.2f}%")
        c2.metric("1 Week", f"{row['1W %']:+.2f}%")
        c3.metric("1 Month",f"{row['1M %']:+.1f}%")
        c4.metric("1 Year", f"{row['1Y %']:+.1f}%")
        c5.metric("5 Year", f"{row['5Y %']:+.0f}%")

        p = row["_prices"]
        fig = go.Figure(go.Scatter(x=p.index, y=p.round(2), fill="tozeroy",
            fillcolor="rgba(59,130,246,0.08)", line=dict(color="#3b82f6",width=2),
            hovertemplate="₹%{y:,.2f}<br>%{x|%d %b %Y}<extra></extra>"))
        fig.update_layout(paper_bgcolor="#151820",plot_bgcolor="#0e0f13",
            font=dict(color="#8b90a7"),height=350,showlegend=False,
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)",tickprefix="₹"),
            margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

        try:
            info = yf.Ticker(row["_ticker"]).info
            cc1,cc2,cc3,cc4 = st.columns(4)
            cc1.metric("Market Cap", f"₹{info.get('marketCap',0)/1e12:.1f}T" if info.get('marketCap') else "–")
            cc2.metric("P/E Ratio",  f"{info.get('trailingPE',0):.1f}x"       if info.get('trailingPE') else "–")
            cc3.metric("52W High",   f"₹{info.get('fiftyTwoWeekHigh',0):,.0f}" if info.get('fiftyTwoWeekHigh') else "–")
            cc4.metric("52W Low",    f"₹{info.get('fiftyTwoWeekLow',0):,.0f}"  if info.get('fiftyTwoWeekLow') else "–")
            if info.get("longBusinessSummary"):
                with st.expander("About the company"):
                    st.write(info["longBusinessSummary"])
        except: st.caption("Detailed info unavailable")

if auto_ref:
    time.sleep(60)
    st.rerun()
