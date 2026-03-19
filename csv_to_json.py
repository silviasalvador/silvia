"""
Convierte data.json (formato CSV exportado de Hex) al formato JSON
que espera el dashboard.

Uso:
    python3 csv_to_json.py                    # lee y sobreescribe data.json
    python3 csv_to_json.py mi_export.csv      # lee desde otro archivo
"""
import csv
import json
import sys
from datetime import datetime, timezone

input_file  = sys.argv[1] if len(sys.argv) > 1 else "data.json"
output_file = "data.json"

records = []
with open(input_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        records.append({
            "curator_id": int(float(row["curator_id"])),
            "type":       row["type"],
            "comment":    row.get("comment", ""),
            "fecha":      row["fecha"],
            "total":      int(float(row["total"])),
        })

data = {
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "records":    records,
}

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

print(f"✓ {len(records)} registros convertidos → {output_file}")
