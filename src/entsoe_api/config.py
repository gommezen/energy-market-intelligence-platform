# ------------------------------------------------------------
# ENTSO-E API Configuration
# ------------------------------------------------------------

BASE_URL = "https://transparency.entsoe.eu/api"             # REST root
FILE_LIBRARY_URL = "https://transparency.entsoe.eu/file-library/api"  # File endpoints

# File-library product codes:
# Congestion Income (Flow-Based Allocations): Category 12.1.E
CONGESTION_INCOME_CATEGORY = "12.1.E"

# ENTSO-E uses domain codes such as:
#   DK_2 → 10YDK-2--------M
DOMAIN_MAP = {
    "DK_2": "10YDK-2--------M",
    "DK_1": "10YDK-1--------W",
    "SE_4": "10Y1001A1001A82H"
}
