import json
import csv
import pytest
from pathlib import Path
import tempfile

from annotatorx.utils.io import (
    ensure_directories,
    resolve_path,
    load_dataset,
    save_annotations_json,
    save_annotations_csv,
)


def test_ensure_directories():
    """Test directory creation utility."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir) / "test" / "nested" / "dir"
        ensure_directories([test_dir])
        assert test_dir.exists()
        assert test_dir.is_dir()


def test_resolve_path():
    """Test path resolution utility."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("test content")
        
        resolved = resolve_path(test_file)
        assert resolved == test_file
        assert resolved.exists()
        
        # Test non-existent path
        with pytest.raises(FileNotFoundError):
            resolve_path(Path(tmpdir) / "nonexistent.txt")


def test_load_dataset_csv():
    """Test loading CSV dataset."""
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = Path(tmpdir) / "test.csv"
        csv_content = "id,text\n1,Hello\n2,World"
        csv_file.write_text(csv_content)
        
        records = load_dataset(csv_file)
        assert len(records) == 2
        assert records[0]["id"] == 1
        assert records[0]["text"] == "Hello"
        assert records[1]["id"] == 2
        assert records[1]["text"] == "World"


def test_load_dataset_json():
    """Test loading JSON dataset."""
    with tempfile.TemporaryDirectory() as tmpdir:
        json_file = Path(tmpdir) / "test.json"
        json_content = {
            "data": [
                {"id": 1, "text": "Hello"},
                {"id": 2, "text": "World"}
            ]
        }
        json_file.write_text(json.dumps(json_content))
        
        records = load_dataset(json_file)
        assert len(records) == 2
        assert records[0]["id"] == 1
        assert records[0]["text"] == "Hello"


def test_load_dataset_json_list():
    """Test loading JSON dataset with direct list format."""
    with tempfile.TemporaryDirectory() as tmpdir:
        json_file = Path(tmpdir) / "test.json"
        json_content = [
            {"id": 1, "text": "Hello"},
            {"id": 2, "text": "World"}
        ]
        json_file.write_text(json.dumps(json_content))
        
        records = load_dataset(json_file)
        assert len(records) == 2
        assert records[0]["id"] == 1


def test_save_annotations_json():
    """Test saving annotations as JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "annotations.json"
        annotations = {
            "version": 1,
            "items": [
                {
                    "id": 1,
                    "payload": {"text": "Hello", "label": "POSITIVE"},
                    "meta": {"source": "test"}
                }
            ]
        }
        
        save_annotations_json(output_file, annotations)
        assert output_file.exists()
        
        loaded = json.loads(output_file.read_text())
        assert loaded == annotations


def test_save_annotations_csv():
    """Test saving annotations as CSV."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "annotations.csv"
        items = [
            {
                "id": 1,
                "payload": {"text": "Hello", "label": "POSITIVE"}
            },
            {
                "id": 2,
                "payload": {"text": "World", "label": "NEGATIVE"}
            }
        ]
        
        save_annotations_csv(output_file, items)
        assert output_file.exists()
        
        # Read back and verify
        with output_file.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 2
        assert rows[0]["id"] == "1"
        assert rows[0]["text"] == "Hello"
        assert rows[0]["label"] == "POSITIVE"
        assert rows[1]["id"] == "2"
        assert rows[1]["text"] == "World"
        assert rows[1]["label"] == "NEGATIVE"


def test_save_annotations_csv_empty():
    """Test saving empty annotations as CSV."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "empty.csv"
        save_annotations_csv(output_file, [])
        assert output_file.exists()
        assert output_file.read_text() == ""
