# ⚡ Open Power Analyst – Energy Market Intelligence Platform

## 🧭 Overview
Open Power Analyst is an open-source, local-first analytics platform for working with public electricity-market data from the ENTSO-E Transparency Platform.
It combines robust data processing with AI-assisted interpretation using fully local large-language models (via Ollama).

The goal is to provide a transparent, extensible, and offline-capable toolkit for analysts, researchers, and engineers who want clear insight into market volatility, congestion income, and flow-based coupling dynamics.

---

## 🔑 Core Capabilities

### **API-based A25 data ingestion**
Robust pipelines for downloading, parsing, and validating Flow-Based Congestion Income 
directly from the ENTSO-E Transparency Platform.

### **Feature-rich time-series engineering**
Automated construction of temporal structure (lags, rolling windows), volatility regimes, 
z-score signals, dispersion metrics, and microstructure indicators tailored for congestion 
income forecasting.

### **Baseline and model benchmarking**
Includes naïve, seasonal naïve, and rolling-mean baselines plus Random Forest regression 
with full metric evaluation (MAE, RMSE, MAPE, MASE).

### **Residual and volatility diagnostics**
Deep-dive error analysis including skewness, autocorrelation, max deviation, and noise structure.

### **Interactive visualisation**
Plotly-powered charts for intraday patterns, volatility behaviour, and model diagnostics.

### **Local LLM commentary**
Uses your own local model (via Ollama) to generate structured, narrative market evaluations 
based on the forecast metrics — grounded, reproducible, and domain-safe.

### **Automatic HTML reporting**
Both Notebook 1 and Notebook 2 can export standalone HTML reports combining plots, metrics, 
and LLM-generated market commentary.

---


## 🚀 Getting Started

1. **Create a virtual environment**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Add your ENTSO-E API key and local model settings**

   Create a `.env` file in the project root and add:
   ```bash
   ENTSOE_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   OLLAMA_MODEL=llama3.1:8b-instruct-q8_0
   OLLAMA_URL=http://localhost:11434
   ```

3. **Launch Jupyter Lab**
   ```bash
   jupyter lab
   ```

4. **Open and run the notebook**
   Start with:
   - Notebook 1 – API ingestion, cleaning, diagnostics, LLM report
   - Notebook 2 – Feature engineering, correlation, AI interpretation

---

## 🧪 Example Outputs ##

Interactive HTML reports are stored in:

/reports/
    congestion_income_report_<timestamp>.html
    feature_engineering_report_<timestamp>.html

---

## 🧰 Tech Stack

- **Python 3.11+**
- **Pandas · Plotly · NumPy**
- **Jupyter Lab** for reproducible workflows
- **Ollama + LLaMA 3.1 8B** for local generative analysis
- **ENTSO-E Transparency API** for open electricity-market data

---

## 📜 License & Attribution

Released under the **MIT License**.  
Data sourced from: [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/).

© 2025 Niels Gommesen
