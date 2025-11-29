import json
import os
import requests


def generate_llm_evaluation(input_data: dict) -> str:
    """
    Generate a markdown forecast evaluation using a local LLM (Ollama).
    Returns markdown text or a descriptive error message.
    """

    # ----------------------------------------------------------------------
    # 0. Validate input keys (defensive programming)
    # ----------------------------------------------------------------------
    required = [
        "rf_metrics",
        "baseline_metrics",
        "feature_importance",
        "residual_statistics",
        "time_range",
    ]

    for key in required:
        if key not in input_data:
            return f"[Error: Missing required key '{key}' in LLM input data]"

    # Convert input to well-escaped JSON for the LLM
    MODEL_INPUT_JSON = json.dumps(input_data, indent=2)

    # ----------------------------------------------------------------------
    # 1. Load Ollama configuration
    # ----------------------------------------------------------------------
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b-instruct-q4_0")

    # ----------------------------------------------------------------------
    # 2. Final Prompt (markdown-only output, no JSON)
    # ----------------------------------------------------------------------

    # -------------------------
    # 2. Balanced, analytical prompt (final recommended version)
    # -------------------------
    prompt = f"""
You are a senior electricity market analyst. You will receive structured forecasting
metrics in a JSON object. Every data point you use MUST come directly from this JSON.

You must NOT perform your own calculations, comparisons, or transformations.
All numeric values, comparisons, feature names, and statistical indicators MUST
be taken directly from the JSON input exactly as provided.

============================================================
WHERE THE MODEL INPUT COMES FROM
============================================================
All information comes from the JSON object shown at the bottom of this prompt.
You must extract your analysis ONLY from these fields:

- rf_metrics  → Random Forest MAE, RMSE, MAPE, MASE and internal stats  
- baseline_metrics  → Naive, Seasonal Naive, Rolling Mean metrics  
- residual_statistics  → mean, std, max error, min error, skewness, autocorr  
- feature_importance  → feature names and scores  
- rf_vs_naive  → {"larger", "smaller", "equal"} comparisons for MAE/RMSE/MAPE/MASE  
- rf_vs_seasonal  → same structure  
- rf_vs_roll  → same structure  
- time_range  → the forecast evaluation window  

You must NOT infer or compute anything beyond these fields.

============================================================
GENERAL RULES
============================================================
- Use ONLY values that appear in the input JSON.  
- If something cannot be determined from the JSON, write:
  "This cannot be determined from the provided metrics."

- All comparisons between RF and baselines MUST come ONLY from:
  rf_vs_naive, rf_vs_seasonal, rf_vs_roll.
  These dicts contain the authoritative labels:
  "larger", "smaller", "equal".
  You must use them exactly as provided.

- You may restate numeric values from rf_metrics and baseline_metrics
  when explaining comparisons, but you may NOT perform numerical reasoning.

- Do NOT introduce new metrics (R², correlation, trend, CV, skewness not provided).
- Do NOT speculate about causes (weather, outages, system conditions).
- Do NOT introduce new features; only use names from feature_importance.

============================================================
STRUCTURE (MANDATORY)
============================================================
You MUST produce a report with exactly these 7 sections,
in this exact order, with these exact headings:

1. Random Forest Model Performance  
2. Comparison With Baseline Models  
3. Systematic Bias (Residual Analysis)  
4. Volatility Behaviour  
5. FBMC Contextual Interpretation  
6. Feature Importance Analysis  
7. Summary and Conclusions  

Each section MUST:  
- Contain 4–7 analytical sentences  
- Use all relevant data from the JSON  
- End with a **Hard facts** block:

**Hard facts:**
- bullet list of exactly the numbers, labels, or feature names used in this section.

============================================================
FBMC RULE (SECTION 5)
============================================================
If the JSON contains NO fields named RAM, PTDF, or CZC, then Section 5 MUST be:

This cannot be determined from the provided metrics.

**Hard facts:**
- No FBMC-specific variables provided.

============================================================
DETAILED CONTENT GUIDANCE
============================================================

SECTION 1: Random Forest Model Performance  
Use rf_metrics. Describe magnitude of errors and behaviour across MAE/RMSE/MAPE/MASE.  
You may mention stability or noise if visible.

SECTION 2: Comparison With Baseline Models  
Use ONLY rf_vs_naive, rf_vs_seasonal, rf_vs_roll.  
Explain for each baseline where RF is larger/smaller/equal.

SECTION 3: Systematic Bias (Residual Analysis)  
Use residual_statistics. Describe direction (mean), dispersion (std), asymmetry (skewness),
extreme errors (max/min), and any persistence (autocorr).

SECTION 4: Volatility Behaviour  
Use residual_stats + rf_metrics to describe variability and instability.  
No invented volatility metrics.

SECTION 5: FBMC Contextual Interpretation  
Use only data that exists.  
If RAM/PTDF/CZC are missing → return the fixed fallback.

SECTION 6: Feature Importance Analysis  
Use only keys inside feature_importance.  
Describe dominance patterns, distribution, clustering of importance.

SECTION 7: Summary and Conclusions  
Synthesize all findings neutrally and factually.

============================================================
OUTPUT FORMAT (STRICT)
============================================================
You must return ONLY one valid JSON object.

IMPORTANT RULES:
- Every "section_x" value MUST be ONE SINGLE STRING.
- The string may contain newlines and markdown, but must remain a single string.
- Do NOT return nested objects, lists, dictionaries, or arrays.
- Put all bullet lists INSIDE the string, not as JSON arrays. Use "- " for bullets.
- Do NOT escape markdown symbols; normal markdown inside the string is allowed.
- Do NOT wrap the JSON in backticks.
- If you cannot produce valid JSON for any reason, return the fallback JSON.

The required object structure is:

{{
  "section_1": "text…\n\n**Hard facts:**\n- fact1\n- fact2",
  "section_2": "text…\n\n**Hard facts:**\n- fact1\n- fact2",
  "section_3": "text…\n\n**Hard facts:**\n- fact1\n- fact2",
  "section_4": "text…\n\n**Hard facts:**\n- fact1\n- fact2",
  "section_5": "text…\n\n**Hard facts:**\n- fact1\n- fact2",
  "section_6": "text…\n\n**Hard facts:**\n- fact1\n- fact2",
  "section_7": "text…\n\n**Hard facts:**\n- fact1\n- fact2"
}}


FALLBACK (use only if necessary):

{{
  "section_1": "ERROR",
  "section_2": "ERROR",
  "section_3": "ERROR",
  "section_4": "ERROR",
  "section_5": "ERROR",
  "section_6": "ERROR",
  "section_7": "ERROR"
}}

No markdown. No extra commentary. No prose outside the JSON object.
Do NOT write anything before the JSON.
Do NOT write anything after the JSON.
Output ONLY the JSON object. Exactly one object.

INPUT DATA (SOURCE OF ALL FACTS):
{MODEL_INPUT_JSON}

"""

    # ----------------------------------------------------------------------
    # 3. Build payload for Ollama
    # ----------------------------------------------------------------------
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.25,
            "num_predict": 2000,
        },
    }

    # ----------------------------------------------------------------------
    # 4. Query Ollama safely
    # ----------------------------------------------------------------------
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=180,
        )
        r.raise_for_status()

        data = r.json()
        text = data.get("response", "").strip()

        if not text:
            return "[LLM returned empty response — check model or prompt.]"

        return text

    except Exception as e:
        return f"[LLM unavailable: {e}]"


    # ----------------------------------------------------------------------
    # 3. Call Ollama API
    # ----------------------------------------------------------------------
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/v1/chat/completions",
            json={
                "model": OLLAMA_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2000,
                "temperature": 0.2,
            },
            timeout=120,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        return f"[Error: Ollama API request failed: {str(e)}]"

    try:
        llm_output = response.json()
        markdown_text = llm_output["choices"][0]["message"]["content"]
    except (KeyError, json.JSONDecodeError) as e:
        return f"[Error: Failed to parse Ollama response: {str(e)}]"

    return markdown_text