import json
from pytask_pro.exporter import DataExporter
from pytask_pro.models import Record

def test_json_round_trip(tmp_path):
    path = tmp_path / "data.json"
    records = [Record("Book", "$10", "Three", "In stock", "https://example.com")]
    DataExporter().to_json(records, path)
    loaded = DataExporter().from_json(path)
    assert loaded == records

def test_csv_export(tmp_path):
    path = tmp_path / "data.csv"
    DataExporter().to_csv([Record("Book")], path)
    assert "title,price,rating,availability,source_url" in path.read_text()
