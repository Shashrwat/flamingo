# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import plotly.graph_objects as go
import io
import numpy as np
import plotly.io as pio
from scipy.stats import gaussian_kde
import random

# ------------------ Data Functions ------------------
@st.cache_data(ttl=86400)
def get_nse_symbols():
    try:
        url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        df = pd.read_csv(io.StringIO(response.text))
        return df['SYMBOL'].unique().tolist()
    except Exception as e:
        st.error(f"Error fetching symbols: {e}")
        return []

@st.cache_data(ttl=3600)
def get_stock_data(symbol, period):
    try:
        ticker = yf.Ticker(f"{symbol}.NS")
        hist = ticker.history(period=period)
        return hist, ticker.info
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame(), {}

# ------------------ Visual Design ------------------
def set_cosmic_design():
    st.markdown("""
    <style>
    /* Base cosmic animation */
    @keyframes cosmic-glow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Enhanced Header Animation */
    @keyframes header-glow {
        0% { text-shadow: 0 0 10px #00f2fe, 0 0 20px #4facfe; }
        50% { text-shadow: 0 0 30px #00f2fe, 0 0 40px #4facfe; }
        100% { text-shadow: 0 0 10px #00f2fe, 0 0 20px #4facfe; }
    }

    .stApp {
        background: linear-gradient(-45deg, 
            #0f0c29, #1a1a4a, #2a2a6e, #3d3d8f,
            #0f0c29, #1a1a4a);
        background-size: 400% 400%;
        animation: cosmic-glow 20s ease infinite;
        color: white;
        font-family: 'Roboto', sans-serif;
    }

    /* ---------- Header Styles ---------- */
    .header-container {
        text-align: center;
        margin-bottom: 40px;
        perspective: 1000px;
    }

    .header-text {
        font-size: 2.8rem !important;
        color: #00f2fe !important;
        animation: header-glow 2s ease-in-out infinite;
        margin-bottom: 0 !important;
        transform: translateZ(50px);
    }

    .header-line {
        height: 3px;
        background: linear-gradient(90deg, transparent, #ff0000, transparent);
        width: 60%;
        margin: 5px auto;
        animation: header-glow 2s ease-in-out infinite;
    }

    /* ---------- Interactive Elements ---------- */
    /* Select Box Enhancements */
    .select-box {
        background: rgba(0,0,0,0.4) !important;
        border: 2px solid transparent !important;
        border-radius: 10px !important;
        padding: 8px !important;
        color: white !important;
        font-size: 1.1rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }

    .select-box:hover {
        border-image: linear-gradient(45deg, #00f2fe, #4facfe) !important;
        border-image-slice: 1 !important;
        box-shadow: 0 8px 16px rgba(0, 242, 254, 0.2) !important;
        transform: translateY(-2px);
    }

    /* Metric Card Enhancements */
    .metric-glow {
        position: relative;
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
        transform: translateZ(0);
    }

    .metric-glow:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 24px -12px rgba(0, 242, 254, 0.3) !important;
    }

    .metric-glow::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(120deg,
            rgba(79, 172, 254, 0.1),
            rgba(0, 242, 254, 0.2));
        opacity: 0;
        transition: opacity 0.4s ease;
    }

    .metric-glow:hover::before {
        opacity: 1;
    }

    /* Chart Container Effects */
    .plot-container.plotly {
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border-radius: 15px !important;
        overflow: hidden !important;
    }

    .plot-container.plotly:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 242, 254, 0.2) !important;
    }

    /* AI Section Enhancements */
    .ai-pulse {
        position: relative;
        border: 2px solid #00f2fe;
        border-radius: 15px;
        padding: 20px;
        margin-top: 40px;
        background: rgba(0,0,0,0.3);
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        transform-style: preserve-3d;
    }

    .ai-pulse:hover {
        transform: perspective(1000px) rotateX(5deg) rotateY(5deg) translateZ(20px);
        box-shadow: 0 20px 40px rgba(0, 242, 254, 0.15) !important;
    }

    .ai-pulse::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at 50% 50%,
            rgba(79, 172, 254, 0.15),
            transparent 70%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }

    .ai-pulse:hover::after {
        opacity: 1;
    }

    /* Universal Hover Transition */
    [data-testid="stVerticalBlock"] > div:not(.stAlert) {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    [data-testid="stVerticalBlock"] > div:not(.stAlert):hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 242, 254, 0.1) !important;
    }

    /* Disclaimer Animation */
    .disclaimer {
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)

# ------------------ Chart Functions ------------------
def create_main_chart(hist, symbol, chart_type):
    fig = go.Figure()
    
    if chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(
            x=hist.index,
            open=hist.Open,
            high=hist.High,
            low=hist.Low,
            close=hist.Close,
            increasing_line_color='#00f2fe',
            decreasing_line_color='#ff6b6b'
        ))
    else:
        mode = 'lines' if chart_type == "Line" else 'lines'
        fig.add_trace(go.Scatter(
            x=hist.index,
            y=hist.Close,
            mode=mode,
            line=dict(color='#00f2fe', width=2),
            fill='toself' if chart_type == "Area" else None
        ))
    
    fig.update_layout(
        title=dict(text=f'<b>{symbol} {chart_type.upper()} ANALYSIS</b>', 
                 font=dict(size=24, color='#00f2fe')),
        height=500,
        xaxis_rangeslider_visible=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0.3)',
        font=dict(color='white')
    )
    return fig

def create_volume_bars(hist):
    fig = go.Figure(go.Bar(
        x=hist.index,
        y=hist.Volume,
        marker=dict(
            color=hist.Volume,
            colorscale='Tealgrn',
            line=dict(width=0))
    ))
    fig.update_layout(
        title=dict(text='<b>VOLUME ANALYSIS</b>', 
                 font=dict(size=20, color='#00f2fe')),
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0.3)',
        font=dict(color='white'))
    return fig

def create_analytics_pie():
    fig = go.Figure(go.Pie(
        labels=['Institutional', 'Retail', 'Insider'],
        values=[45, 35, 20],
        hole=0.5,
        marker=dict(
            colors=['#00f2fe', '#4facfe', '#ff6b6b'],
            line=dict(color='white', width=2))
    ))
    fig.update_layout(
        title=dict(text='<b>OWNERSHIP STRUCTURE</b>', 
                 font=dict(size=20, color='#00f2fe')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0.3)',
        font=dict(color='white'))
    return fig

def create_returns_wave(hist):
    returns = hist.Close.pct_change().dropna()
    x = np.linspace(returns.min(), returns.max(), 100)
    kde = gaussian_kde(returns)
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=returns,
        histnorm='probability density',
        marker=dict(color='rgba(79,172,254,0.6)')
    ))
    fig.add_trace(go.Scatter(
        x=x, y=kde(x),
        mode='lines',
        line=dict(color='#00f2fe', width=2)
    ))
    fig.update_layout(
        title=dict(text='<b>RETURNS DISTRIBUTION</b>', 
                 font=dict(size=20, color='#00f2fe')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0.3)',
        font=dict(color='white'))
    return fig

# ------------------ AI Section ------------------
def show_ai_section():
    bullish = random.randint(40, 85)
    bearish = 100 - bullish
    forecast = round(random.uniform(-3.5, 5.5), 1)
    
    st.markdown(f"""
    <div class='ai-pulse'>
        <h2 style='color: #00f2fe; text-align: center;'>AI MARKET INSIGHTS 🔮</h2>
        <div style='display: flex; justify-content: center; gap: 30px; margin: 20px 0;'>
            <div style='text-align: center;'>
                <h3 style='color: #4facfe;'>7-Day Forecast</h3>
                <div style='font-size: 2em; color: {'#00f2fe' if forecast >= 0 else '#ff6b6b'}'>
                    {forecast}%
                </div>
            </div>
            <div style='text-align: center;'>
                <h3 style='color: #4facfe;'>Market Sentiment</h3>
                <div style='font-size: 2em; color: #00f2fe;'>{bullish}%</div>
                <div style='color: #ff6b6b;'>Bearish {bearish}%</div>
            </div>
        </div>
        <div class='disclaimer'>
            📌 Note: AI predictions are simulated for demonstration purposes only. 
            This is not financial advice. Past performance does not guarantee future results. 
            Always conduct your own research.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ------------------ Main App ------------------
def main():
    st.set_page_config(page_title="Flamingo Stocks", layout="wide")
    set_cosmic_design()

    st.markdown("""
    <div class='header-container'>
        <h1 class='header-text'>FLAMINGO STOCK ANALYTICS</h1>
        <div class='header-line'></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        symbols = get_nse_symbols()
        symbol = st.selectbox("Select Stock", symbols, index=0, 
                            format_func=lambda x: f"📈 {x}",
                            key='stock_select')

    with col2:
        period = st.selectbox("Period", ['1mo','3mo','6mo','1y','5y'], 
                             index=3, key='period_select')

    with col3:
        chart_type = st.selectbox("Chart Style", ["Candlestick", "Line", "Area"], 
                                key='chart_select')

    hist, info = get_stock_data(symbol, period)
    
    if not hist.empty:
        cols = st.columns(4)
        top_metrics = {
            'Current Price': hist['Close'][-1],
            '52W High': info.get('fiftyTwoWeekHigh'),
            'P/E Ratio': info.get('trailingPE'),
            'Market Cap': info.get('marketCap')
        }
        
        for idx, (metric, value) in enumerate(top_metrics.items()):
            with cols[idx]:
                if value is not None:
                    st.markdown(f"""
                    <div class='metric-glow'>
                        <h3 style='color: #4facfe; margin:0'>{metric}</h3>
                        <h2 style='color: #00f2fe; margin:0'>{
                            f'₹{value:,.2f}' if isinstance(value, (int, float)) and metric != 'P/E Ratio' else
                            f'{value:.2f}' if value else 'N/A'
                        }</h2>
                    </div>
                    """, unsafe_allow_html=True)

        st.plotly_chart(create_main_chart(hist, symbol, chart_type), use_container_width=True)

        if info.get('longBusinessSummary'):
            st.markdown(f"""
            <div class='metric-glow'>
                <h3 style='color: #00f2fe; margin-top:0'>{symbol} Overview</h3>
                <p style='line-height: 1.6;'>{info['longBusinessSummary']}</p>
                <div style='margin-top: 15px;'>
                    <strong>Industry:</strong> {info.get('industry', 'N/A')}<br>
                    <strong>Sector:</strong> {info.get('sector', 'N/A')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            cols = st.columns(3)
            secondary_metrics = {
                'Dividend Yield': info.get('dividendYield'),
                'Beta': info.get('beta'),
                'EPS': info.get('trailingEps')
            }
            
            for idx, (metric, value) in enumerate(secondary_metrics.items()):
                with cols[idx]:
                    if value is not None:
                        st.markdown(f"""
                        <div class='metric-glow'>
                            <h3 style='color: #4facfe; margin:0'>{metric}</h3>
                            <h2 style='color: #00f2fe; margin:0'>{
                                f'{value*100:.2f}%' if 'Yield' in metric else
                                f'{value:.2f}' if value else 'N/A'
                            }</h2>
                        </div>
                        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.plotly_chart(create_volume_bars(hist), use_container_width=True)
        with col2:
            st.plotly_chart(create_analytics_pie(), use_container_width=True)
        with col3:
            st.plotly_chart(create_returns_wave(hist), use_container_width=True)

        show_ai_section()

    else:
        st.warning("Data not available for selected stock")

if __name__ == "__main__":
    main() 
