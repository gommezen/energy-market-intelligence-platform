import json
import os
import requests
import re


def generate_llm_evaluation(input_data: dict) -> str:
    """
    Generate a structured LLM evaluation of forecasting metrics.
    Always returns a string (either JSON or an error message).
    """

    # ----------------------------------------------------------------------
    # 0. Validate input
    # ----------------------------------------------------------------------
    required_keys = [
        "rf_metrics",
        "baseline_metrics",
        "feature_importance",
        "residual_statistics",
        "time_range"
    ]
    for key in required_keys:
        if key not in input_data:
            return f"[Error: Missing required key '{key}']"

    # ----------------------------------------------------------------------
    # 1. Convert input to JSON BEFORE prompt
    # ----------------------------------------------------------------------
    MODEL_INPUT_JSON = json.dumps(input_data, indent=2)

    # ----------------------------------------------------------------------
    # 2. Load Ollama settings
    # ----------------------------------------------------------------------
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b-instruct-q4_0")

    # ----------------------------------------------------------------------
    # 3. Prompt
    # ----------------------------------------------------------------------
    prompt = f"""
You are an electricity market analyst. You will generate a structured evaluation
based only on the numerical metrics provided.

Your output MUST be a single valid JSON object with the fields:
section_1, section_2, section_3, section_4, section_5, section_6, section_7.
Each field must be a string.

GENERAL RULES
-------------
- Do NOT use the words: better, worse, weaker, stronger, superior, inferior.
- All comparisons MUST use: "X is larger than Y", "X is smaller than Y", or "X is equal to Y".
- Do NOT speculate about causes, external events, operations, or grid conditions.
- Do NOT invent data or refer to unobserved variables.

MANDATORY NUMERIC SELF-CHECK
----------------------------
Before writing any comparison, you MUST internally evaluate whether it is TRUE.
Do NOT write a comparison unless the numeric relation is correct.

SECTION RULES
-------------
Section 1:
- Describe RF MAE, RMSE, MAPE, MASE.
- End with: "Hard facts:\n- ...".

Section 2:
- Compare RF metrics to each baseline using ONLY numeric comparisons.
- End with Hard facts.

Section 3:
- Describe residual mean, std, skewness, max_abs_error, autocorrelation.
- End with Hard facts.

Section 4:
- Describe volatility using the same residual statistics.
- End with Hard facts.

Section 5:
If the input does NOT contain any FBMC variables named "RAM", "PTDF", or "CZC",
then section_5 MUST be exactly:
"This cannot be determined from the provided metrics.\n\nHard facts:\n- No FBMC-specific variables provided."

Section 6:
- Describe feature_importance.
- End with Hard facts.

Section 7:
- Short numerical summary using only previously stated information.
- End with Hard facts.

OUTPUT FORMAT
-------------
Return ONLY this JSON object:

{{
  "section_1": "...",
  "section_2": "...",
  "section_3": "...",
  "section_4": "...",
  "section_5": "...",
  "section_6": "...",
  "section_7": "..."
}}

INPUT DATA:
{MODEL_INPUT_JSON}
"""

    # ----------------------------------------------------------------------
    # 4. Send to Ollama
    # ----------------------------------------------------------------------
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_predict": 1500,
            "temperature": 0.2
        }
    }

    try:
        response_text = ""

        with requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            stream=True,
            timeout=180
        ) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line:
                    data = json.loads(line.decode())
                    response_text += data.get("response", "")

        raw = response_text.strip()

        # ------------------------------------------------------------------
        # 5. Extract JSON (in case model wrapped extra text)
        # ------------------------------------------------------------------
        match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
        if not match:
            return "[Error: LLM did not return valid JSON.]"

        clean_json = match.group(0)

        parsed = json.loads(clean_json)

        return json.dumps(parsed, indent=2)

    except Exception as e:
        return f"[LLM unavailable: {e}]"
