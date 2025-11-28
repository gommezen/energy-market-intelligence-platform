# src/reporting/notebook2_report.py

from pathlib import Path
from datetime import datetime
from collections import defaultdict
import markdown

def export_notebook2_report(feature_descriptions, analysis_text, corr_fig_html,
                            model_name="llama3.1:8b-instruct-q4_0",
                            output_dir="reports"):

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    safe_stamp = timestamp.replace(":", "").replace(" ", "_")
    report_path = output_dir / f"feature_engineering_report_{safe_stamp}.html"

    # Convert AI text to HTML
    analysis_html = markdown.markdown(
        analysis_text,
        extensions=["extra", "sane_lists"]
    )

    # -------- GROUP FEATURES --------
    groups = defaultdict(list)

    for name, desc in feature_descriptions.items():
        if name.startswith("lag_"):
            groups["Lag & Memory Features"].append((name, desc))
        elif name.startswith("roll_mean"):
            groups["Rolling Means"].append((name, desc))
        elif name.startswith("roll_std"):
            groups["Rolling Volatility"].append((name, desc))
        elif name.startswith("roll_max"):
            groups["Rolling Maxima"].append((name, desc))
        elif name.startswith("roll_min"):
            groups["Rolling Minima"].append((name, desc))
        elif name.startswith("diff"):
            groups["Microstructure / Momentum"].append((name, desc))
        elif name in ["hour", "day_of_week", "is_weekend"]:
            groups["Intraday Structure"].append((name, desc))
        elif name in ["month", "quarter", "week_of_year", "is_month_end"]:
            groups["Seasonal / Structural Features"].append((name, desc))
        else:
            groups["Other"].append((name, desc))

    # -------- HTML TEMPLATE --------
    html = f"""
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Feature Engineering Report</title>
    <style>
      body {{
        font-family: "Segoe UI", Arial, sans-serif;
        margin: 40px;
        color: #222;
        background-color: #fafafa;
        line-height: 1.6;
      }}
      h2, h3 {{
        color: #2a3950;
        margin-bottom: 6px;
      }}
      .section {{
        margin-bottom: 35px;
      }}
      .card {{
        background: #ffffff;
        border: 1px solid #e3e6ea;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
      }}
      table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.92rem;
        margin-top: 10px;
      }}
      th {{
        background: #f0f3f7;
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #d0d4d9;
      }}
      td {{
        padding: 6px 8px;
        border-bottom: 1px solid #eee;
        vertical-align: top;
      }}
      code {{
        background: #e6e8eb;
        padding: 2px 4px;
        border-radius: 4px;
      }}
    </style>
    </head>

    <body>

    <h2>Feature Engineering Report</h2>
    <p><strong>Generated:</strong> {timestamp}<br>
    <strong>Model:</strong> {model_name}</p>

    <h3>Engineered Feature Groups</h3>
    <p>The following features were derived from the DK2 congestion income time series:</p>
    """

    # -------- INSERT FEATURE GROUP TABLES --------
    for group, items in groups.items():
        html += f"<div class='section card'><h3>{group}</h3>"
        html += "<table><tr><th>Feature</th><th>Description</th></tr>"
        for name, desc in items:
            html += f"<tr><td><code>{name}</code></td><td>{desc}</td></tr>"
        html += "</table></div>"

    # -------- INSERT CORRELATION MATRIX --------
    html += f"""
    <div class="section card">
    <h3>📊 Correlation Matrix</h3>
    {corr_fig_html}
    </div>
    """

    # -------- INSERT AI ANALYSIS --------
    html += f"""
    <div class="section card">
    <h3>🤖 AI Feature Analysis</h3>
    {analysis_html}
    </div>

    </body>
    </html>
    """

    report_path.write_text(html, encoding="utf-8")
    print(f"📄 Notebook 2 report saved → {report_path.resolve()}")
    return report_path
