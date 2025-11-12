# ⚡ Open Power Analyst – Energy Market Intelligence Platform

**Phase 1: Core Data & AI-Assisted Reporting**

_“A local-first exploration of transparency, volatility, and foresight in the European power system.”_

---

## 🧭 Overview

**Open Power Analyst** is a local-first, open-source platform for exploring, cleaning, and forecasting electricity-market dynamics using public data from the **ENTSO-E Transparency Platform**.  

The project demonstrates how reproducible, data-driven energy analysis can be combined with **local large-language-model (LLM) interpretation** to generate readable, explainable insights — entirely offline.

It’s built for analysts, researchers, and engineers who want to understand the drivers of market volatility and congestion revenues while keeping computation, data, and models on their own machines.

---

## 🧠 Key Features

- **Automated Data Ingestion & Cleaning**  
  Scripts and notebooks for importing, parsing, and validating ENTSO-E datasets (day-ahead prices, load, congestion income, etc.).

- **Structured Time-Series Analysis**  
  Tools for computing volatility, mean revenue, and coefficient of variation on intraday or hourly resolution.

- **Interactive Visualisation**  
  Built with Plotly for high-resolution, exploratory analysis.

- **AI-Assisted Market Commentary**  
  Local LLMs (via **Ollama** and models like `llama3.1:8b-instruct-q8_0`) generate concise textual summaries interpreting market metrics.

- **Automatic Report Export**  
  Each analysis run can produce a standalone HTML report combining visuals, numerical summaries, and LLM commentary.

---

## 📁 Repository Structure

energy-market-intelligence-platform/
├── notebooks/ # Jupyter workflows (e.g. 1_data_ingestion.ipynb)
├── src/ # Modular Python source code
├── data/
│ ├── raw/ # Local input data (excluded from Git)
│ └── processed/ # Cleaned parquet files
├── reports/
│ ├── example_congestion_income_report.html # Sample AI-assisted output
│ └── README.md
├── requirements.txt
└── README.md


---

## 🧩 Example Output

An example interactive report is included at  
`reports/example_congestion_income_report.html`

It visualises flow-based congestion-income data for the **DK2 bidding zone**, with:
- 15-minute resolution time series,
- volatility and hourly spread metrics, and
- automatically generated interpretation written by a local LLM.

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
   - Start with: `1_data_ingestion.ipynb`
   - This notebook ingests, cleans, visualizes, and generates AI-assisted reports.

---

## 🧭 Roadmap

**Phase 2 – Feature Engineering & Forecasting**  
Lag features, rolling statistics, and model training (Prophet, XGBoost, etc.).

**Phase 3 – Optimization & Decision Support**  
Integrating forecasts with asset portfolios and dispatch optimization.

**Phase 4 – Explainability & Participatory Insights**  
Multi-agent LLMs and explainable dashboards for citizen-science and policy engagement.

---

## 🧰 Tech Stack

- **Python 3.11+**
- **Pandas · Plotly · DuckDB · Polars**
- **Jupyter Lab** for reproducible workflows
- **Ollama + LLaMA 3.1 8B** for local generative analysis
- **ENTSO-E Transparency API** for open electricity-market data

---

## 📜 License & Attribution

Released under the **MIT License**.  
Data courtesy of the [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/).

© 2025 Niels Gommesen
