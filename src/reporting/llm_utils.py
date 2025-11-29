import re
import json

def extract_sections_from_llm_output(text):
    """
    Extracts 'section_1' ... 'section_7' from imperfect JSON-like LLM output.
    Does NOT require valid JSON structure.
    """

    pattern = r'"section_(\d+)":\s*"((?:[^"\\]|\\.)*)"'
    matches = re.findall(pattern, text, flags=re.DOTALL)

    if not matches:
        raise ValueError(f"Could not extract any sections.\nRaw output:\n{text}")

    sections = {f"section_{num}": content.replace('\\"', '"')
                for num, content in matches}

    # verify we got all required sections
    for i in range(1, 8):
        key = f"section_{i}"
        if key not in sections:
            raise ValueError(
                f"Missing {key} in LLM output.\nRaw output:\n{text}"
            )

    return sections


def build_markdown_report(sections):
    """Formats a 7-section dict into a readable markdown report."""
    md = f"""
# 📈 LLM Forecast Evaluation Report

---

## 1. Random Forest Model Performance  
{sections['section_1']}

---

## 2. Comparison With Baseline Models  
{sections['section_2']}

---

## 3. Systematic Bias (Residual Analysis)  
{sections['section_3']}

---

## 4. Volatility Behaviour  
{sections['section_4']}

---

## 5. FBMC Contextual Interpretation  
{sections['section_5']}

---

## 6. Feature Importance Analysis  
{sections['section_6']}

---

## 7. Summary and Conclusions  
{sections['section_7']}

---
"""
    return md
