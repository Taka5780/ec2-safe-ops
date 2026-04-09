import csv
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, List


class CSVReporter:
    def __init__(self, output_dir: str = "reports") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(self, data_list: List[Any], prefix: str = "report") -> str:
        if not data_list:
            print("[INFO] No data to export")
            return ""
        try:
            rows = [asdict(item) for item in data_list]
            header = list(rows[0].keys())

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = self.output_dir / f"{prefix}_{timestamp}.csv"

            with open(file_path, "w", newline="", encoding="utf_8_sig") as f:
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writeheader()
                writer.writerows(rows)

            return str(file_path.absolute())
        except Exception as e:
            print(f"[ERROR][CSV] {e}")
            return ""
