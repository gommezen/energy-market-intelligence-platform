"""
parser.py — Unified ENTSO-E XML/CSV parsing helpers
---------------------------------------------------
This module supports two distinct data sources:

1) Transparency Platform file downloads
   - CSV or older XML format
   - Parsed by parse_congestion_income_file()

2) ENTSO-E REST API XML (new flow-based API)
   - Contains <TimeSeries><Period><Point> structure
   - Parsed by parse_entsoe_api_xml()

Both return tidy DataFrames with:
    Timestamp index
    RevenueEUR column
"""

import pandas as pd
from pathlib import Path
from io import StringIO, BytesIO
import xml.etree.ElementTree as ET

# Namespace for ENTSO-E API XML (A25)
NAMESP = {"ns": "urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:0"}

# Possible numeric fields inside <Point>
CANDIDATE_VALUE_FIELDS = [
    "quantity",
    "price.amount",
    "flowAmount",
    "amount",
    "quantity_Measure_Unit.name",
]


# ----------------------------------------------------------------------
# Helper: extract numeric value from <Point>
# ----------------------------------------------------------------------
def extract_point_value(pt):
    """
    Try multiple possible XML child elements to find the numeric congestion income value.
    Returns float or None.
    """
    for tag in CANDIDATE_VALUE_FIELDS:
        node = pt.find(f"ns:{tag}", NAMESP)
        if node is not None and node.text not in (None, ""):
            try:
                return float(node.text)
            except:
                pass
    return None


# ======================================================================
# 1) PARSER FOR REST API XML (A25/B10)
# ======================================================================
def parse_entsoe_api_xml(xml_bytes: bytes) -> pd.DataFrame:
    """
    Parses ENTSO-E REST API XML using <TimeSeries> → <Period> → <Point> structure.
    Returns DataFrame with Timestamp index + RevenueEUR column.
    """

    try:
        tree = ET.parse(BytesIO(xml_bytes))
        root = tree.getroot()
    except Exception as e:
        raise ValueError(f"XML parsing error: {e}")

    series = root.findall(".//ns:TimeSeries", NAMESP)
    if not series:
        raise ValueError("No <TimeSeries> elements found – not valid A25 API XML")

    all_rows = []

    for ts in series:
        periods = ts.findall(".//ns:Period", NAMESP)
        for p in periods:

            start_node = p.find("ns:timeInterval/ns:start", NAMESP)
            if start_node is None:
                continue

            period_start = pd.to_datetime(start_node.text)

            points = p.findall("ns:Point", NAMESP)
            for pt in points:

                pos_node = pt.find("ns:position", NAMESP)
                if pos_node is None:
                    continue

                pos = int(pos_node.text)
                value = extract_point_value(pt)

                if value is None:
                    continue

                timestamp = period_start + pd.Timedelta(minutes=15 * (pos - 1))

                all_rows.append((timestamp, value))

    if not all_rows:
        raise ValueError("No numeric values found in API XML")

    df = pd.DataFrame(all_rows, columns=["Timestamp", "RevenueEUR"])
    df = df.set_index("Timestamp").sort_index()
    return df


# ======================================================================
# 2) PARSER FOR LOCAL CSV/XML FILES (old style)
# ======================================================================
def parse_congestion_income_file(path: Path) -> pd.DataFrame:
    """
    Parses raw ENTSO-E congestion income file (XML or CSV) into a tidy dataframe.

    Supports both old XML/CSV exports from the Transparency Platform.
    """

    suffix = path.suffix.lower()

    # --------------------------------------------------------
    # CSV / TXT files
    # --------------------------------------------------------
    if suffix in [".csv", ".txt"]:
        df = pd.read_csv(path)
        df = df.rename(columns={
            "start": "Start",
            "end": "End",
            "revenue": "RevenueEUR",
            "Revenue (EUR)": "RevenueEUR"
        })

    # --------------------------------------------------------
    # XML files (old style)
    # --------------------------------------------------------
    elif suffix == ".xml":
        try:
            xml_text = path.read_text(encoding="utf-8")
            df = pd.read_xml(StringIO(xml_text))
        except Exception:
            raise ValueError(f"Cannot parse XML file: {path}")

        df = df.rename(columns={
            "Period.start": "Start",
            "Period.end": "End",
            "CongestionIncome.amount": "RevenueEUR"
        })

    else:
        raise ValueError(f"Unsupported file format: {suffix}")

    # --------------------------------------------------------
    # Cleaning
    # --------------------------------------------------------
    for col in ["Start", "End"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    if "RevenueEUR" in df.columns:
        df["RevenueEUR"] = pd.to_numeric(df["RevenueEUR"], errors="coerce")

    df = df.dropna(subset=["Start", "RevenueEUR"])

    return df[["Start", "End", "RevenueEUR"]].sort_values("Start")


# ======================================================================
# 3) HIGH-LEVEL WRAPPER
# ======================================================================
def parse_local_or_api(content: bytes = None, path: Path = None):
    """
    Automatically parse:

      - REST API XML if 'content' (bytes) is provided
      - Local CSV/XML file if 'path' is provided

    Returns: tidy DataFrame
    """
    if content is not None:
        return parse_entsoe_api_xml(content)

    if path is not None:
        return parse_congestion_income_file(path)

    raise ValueError("Either 'content' or 'path' must be provided.")
