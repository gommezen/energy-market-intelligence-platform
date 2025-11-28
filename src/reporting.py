# ================================================================
# src/reporting.py
# Utility functions for exporting analysis reports
# ================================================================

import json
import markdown
from pathlib import Path
from datetime import datetime
import plotly.io as pio


def export_notebook1_report(
    df_api,
    fig,
    analysis_text=None,
    model_name="llama3.1:8b-instruct-q4_0"
):
    """
    Export a clean HTML report for Notebook 1.

    Priority order for AI analysis:
    1) Use analysis_text provided by Notebook 1 (recommended)
    2) If missing, try loading Notebook 2 report from llm_market_summary.md
    3) If neither exists, show a safe fallback message
    """

    # -----------------------------------------------------------
    # 1. Resolve LLM analysis priority
    # -----------------------------------------------------------

    # Case 1 — Notebook 1 generated analysis
    if analysis_text and isinstance(analysis_text, str) and analysis_text.strip():
        analysis_html = markdown.markdown(
            analysis_text,
            extensions=["extra", "sane_lists"]
        )
        analysis_title = "🤖 LLM Market Analysis"

    else:
        # Case 2 — try to load Notebook 2’s market summary if available
        analysis_path = Path("data/processed/llm_market_summary.md")

        if analysis_path.exists():
            analysis_raw = analysis_path.read_text(encoding="utf-8")
            analysis_html = markdown.markdown(
                analysis_raw,
                extensions=["extra", "sane_lists"]
            )
            analysis_title = "🤖 Imported LLM Market Analysis (from Notebook 2)"

        else:
            # Case 3 — fallback
            fallback = (
                "No AI analysis was generated in Notebook 1. "
                "Notebook 2 will create a full feature-engineering analysis."
            )
            analysis_html = markdown.markdown(
                fallback,
                extensions=["extra", "sane_lists"]
            )
            analysis_title = "🤖 LLM Market Analysis (fallback)"


    # -----------------------------------------------------------
    # 2. Prepare export directory
    # -----------------------------------------------------------
    REPORTS_DIR = Path("reports")
    REPORTS_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_path = REPORTS_DIR / f"congestion_income_report_{timestamp}.html"

    # -----------------------------------------------------------
    # 3. Convert Plotly figure
    # -----------------------------------------------------------
    fig_html = pio.to_html(fig, full_html=False, include_plotlyjs="cdn")

    # -----------------------------------------------------------
    # 4. Format summary metrics
    # -----------------------------------------------------------
    mean_val = df_api["RevenueEUR"].mean()
    std_val = df_api["RevenueEUR"].std()
    min_val = df_api["RevenueEUR"].min()
    max_val = df_api["RevenueEUR"].max()
    dmin = df_api.index.min()
    dmax = df_api.index.max()

    summary_html = f"""
    <ul>
      <li><strong>Date range:</strong> {dmin} → {dmax}</li>
      <li><strong>Mean revenue:</strong> {mean_val:,.2f} EUR</li>
      <li><strong>Volatility (std):</strong> {std_val:,.2f} EUR</li>
      <li><strong>Max revenue:</strong> {max_val:,.2f} EUR</li>
      <li><strong>Min revenue:</strong> {min_val:,.2f} EUR</li>
    </ul>
    """

    # -----------------------------------------------------------
    # 5. Build full HTML layout
    # -----------------------------------------------------------
    html_header = f"""
    <h2>Flow-Based Congestion Income Report (DK2)</h2>
    <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    <p><strong>Model:</strong> {model_name}</p>
    """

    html_template = f"""
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Notebook 1 – Congestion Income Report</title>
    <style>
      body {{
        font-family: "Segoe UI", Arial, sans-serif;
        margin: 40px;
        color: #222;
        background-color: #fdfdfd;
        line-height: 1.6;
      }}
      h2 {{
        color: #2a3f5f;
        margin-bottom: 10px;
      }}
      h3 {{
        color: #3b5998;
        margin-top: 30px;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 5px;
      }}
      .analysis, .summary {{
        margin-top: 25px;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
      }}
      ul {{
        margin-left: 20px;
      }}
    </style>
    </head>
    <body>

    {html_header}

    <h3>📊 Interactive Revenue Plot</h3>
    {fig_html}

    <div class="summary">
    <h3>📄 Notebook 1 Summary</h3>
    {summary_html}
    <p>This dataset is now ready for feature engineering in Notebook 2.</p>
    </div>

    <div class="analysis">
    <h3>{analysis_title}</h3>
    {analysis_html}
    </div>

    </body>
    </html>
    """

    # -----------------------------------------------------------
    # 6. Save the report file
    # -----------------------------------------------------------
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"✅ Notebook 1 report saved → {report_path.resolve()}")
    return report_path
