# flamingo
AI-powered Stock Screener, Streamlit based website

```markdown
# 🔥 Flamingo Stock Analytics

## 🌌 Features
- **Real-time NSE/BSE Data** through Yahoo Finance API
- **Interactive Visualizations**: Candlestick/Line/Area Charts
- **AI-Powered Insights**: 7-day Forecast & Market Sentiment
- **Advanced Analytics**:
  - Ownership Structure Breakdown
  - Returns Distribution (Gaussian KDE)
  - Volume Analysis
- **Cosmic UI/UX** with Animated Elements
- **Key Metrics**: P/E Ratio, Market Cap, 52W High/Low

## 🚀 Installation
1. Clone repository:
```bash
git clone https://github.com/yourusername/flamingo-stocks.git
cd flamingo-stocks
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📈 Usage
Start the Streamlit app:
```bash
streamlit run app.py
```

**Interface Guide**:
1. Select stock from NSE dropdown
2. Choose analysis period (1mo to 5Y)
3. Switch between chart types
4. Explore AI predictions in bottom section

## 🛠️ Dependencies
```txt
streamlit>=1.22
yfinance>=0.2.18
pandas>=1.5.0
plotly>=5.11.0
scipy>=1.10.0
numpy>=1.23.0
requests>=2.28.0
```

## 🤝 Contributing
1. Fork the project
2. Create your feature branch:
```bash
git checkout -b feature/amazing-feature
```
3. Commit changes:
```bash
git commit -m 'Add some amazing feature'
```
4. Push to branch:
```bash
git push origin feature/amazing-feature
```
5. Open a Pull Request

## 📜 License
Distributed under MIT License. See `LICENSE` for details.

## ☄️ Acknowledgments
- Yahoo Finance API via `yfinance`
- Streamlit for interactive web framework
- Plotly for advanced visualizations

---
