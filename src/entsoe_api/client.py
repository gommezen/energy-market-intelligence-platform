import os, requests, datetime
from pathlib import Path
from typing import List, Dict, Optional
from .config import FILE_LIBRARY_URL, DOMAIN_MAP, CONGESTION_INCOME_CATEGORY

# ------------------------------------------------------------
# ENTSO-E File Library Client
# Handles:
#   1) Authentication using API token
#   2) Listing available files for a product/category
#   3) Downloading raw files for local storage
# ------------------------------------------------------------

class EntsoeClient:
    def __init__(self, token: str):
        """
        Parameters
        ----------
        token : str
            ENTSO-E API token (stored in .env as ENTSOE_API_TOKEN)
        """
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}"
        })

    # --------------------------------------------------------
    # Utility: simple GET wrapper with error-handling
    # --------------------------------------------------------
    def _get(self, url: str, params: dict = None):
        r = self.session.get(url, params=params)
        if not r.ok:
            raise ValueError(
                f"ENTSO-E Request failed ({r.status_code}): {r.text[:500]}"
            )
        return r

    # --------------------------------------------------------
    # 1) List available files in file library
    # --------------------------------------------------------
    def list_files(
        self,
        category: str,
        start: str,
        end: str,
        bidding_zone: str,
        limit: int = 200
    ) -> List[Dict]:
        """
        Query ENTSO-E file library for metadata for a given date range.

        This returns *metadata only*, not files.
        """
        domain = DOMAIN_MAP[bidding_zone]

        params = {
            "page": 0,
            "size": limit,
            "psrType": "",              # not needed for congestion income
            "category": category,
            "searchFrom": start,
            "searchTo": end,
            "area": domain,
        }

        url = f"{FILE_LIBRARY_URL}/v1/files"
        r = self._get(url, params=params)
        data = r.json()

        return data.get("content", [])

    # --------------------------------------------------------
    # 2) Download a single file by ID
    # --------------------------------------------------------
    def download_file(self, file_id: str, dest_path: Path) -> Path:
        """
        Downloads a file given its fileId.
        Saves raw XML/CSV into the data/raw folder.
        """
        url = f"{FILE_LIBRARY_URL}/v1/files/{file_id}/download"

        r = self._get(url)
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        with open(dest_path, "wb") as f:
            f.write(r.content)

        return dest_path

    # --------------------------------------------------------
    # 3) Convenience: find and download all congestion income files
    # --------------------------------------------------------
    def fetch_congestion_income(
        self,
        bidding_zone: str,
        start: str,
        end: str,
        raw_dir: Path
    ) -> List[Path]:
        """
        High-level helper:
        - Lists files for 12.1.E congestion income
        - Downloads all found files
        """
        meta = self.list_files(
            category=CONGESTION_INCOME_CATEGORY,
            start=start,
            end=end,
            bidding_zone=bidding_zone
        )

        if len(meta) == 0:
            print("⚠️ No files found for given period.")
            return []

        saved_files = []

        for m in meta:
            file_id = m["fileId"]
            fname = m["fileName"]
            dest = raw_dir / fname

            print(f"⬇️ Downloading {fname} ...")
            saved_files.append(
                self.download_file(file_id, dest)
            )

        return saved_files
