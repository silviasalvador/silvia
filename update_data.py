import json
from datetime import datetime, timezone
from google.cloud import bigquery

client = bigquery.Client()

QUERY = """
SELECT
    CAST(created_by AS INT64) AS curator_id,
    type,
    comment,
    DATE(created_at) AS fecha,
    COUNT(*) AS total
FROM `fc-bi-common-pro-rev1.sources_mysql_freepik_manager.graphic_resource_reports`
WHERE created_at >= '2025-01-01'
  AND created_by IN (28,29,30,31,32,33,48,51,52,91,92,93,94,186,207,216,221,244,245,246,247,248,249,250,251,301)
GROUP BY curator_id, fecha, type, comment
ORDER BY curator_id, fecha, type
"""

print("Ejecutando query en BigQuery...")
rows = list(client.query(QUERY).result())
print(f"{len(rows)} filas obtenidas")

records = []
for row in rows:
    records.append({
        "curator_id": int(row.curator_id),
        "type":       row.type,
        "comment":    row.comment or "",
        "fecha":      str(row.fecha),
        "total":      int(row.total)
    })

data = {
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "records":    records
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

print("data.json generado correctamente")
