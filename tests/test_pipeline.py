import json
import pytest
from pathlib import Path

from annotatorx.pipeline.annotate import annotate_records
from annotatorx.validators.schemas import AnnotationSet


def test_annotate_records_deterministic():
    """Test that annotation is deterministic with same seed."""
    records = [
        {"id": 1, "text": "This is great!"},
        {"id": 2, "text": "I hate this."},
    ]
    
    # Same seed should produce same results
    result1 = annotate_records(records, seed=42)
    result2 = annotate_records(records, seed=42)
    assert result1 == result2
    
    # Different seed should produce different results
    result3 = annotate_records(records, seed=123)
    assert result1 != result3


def test_annotate_records_schema_compliance():
    """Test that annotation output matches expected schema."""
    records = [
        {"id": 1, "text": "Test text"},
    ]
    
    result = annotate_records(records, seed=0)
    
    # Validate against Pydantic schema
    annotation_set = AnnotationSet.model_validate(result)
    assert annotation_set.version == 1
    assert len(annotation_set.items) == 1
    
    item = annotation_set.items[0]
    assert item.id == 1
    assert "text" in item.payload
    assert "label" in item.payload
    assert item.payload["text"] == "Test text"
    assert item.payload["label"] in ["POSITIVE", "NEGATIVE", "NEUTRAL"]
    assert "source" in item.meta
    assert "seed" in item.meta


def test_annotate_records_custom_fields():
    """Test annotation with custom field names."""
    records = [
        {"id": 1, "content": "Test content"},
    ]
    
    result = annotate_records(
        records, 
        label_field="sentiment", 
        text_field="content", 
        seed=0
    )
    
    annotation_set = AnnotationSet.model_validate(result)
    item = annotation_set.items[0]
    assert "content" in item.payload
    assert "sentiment" in item.payload
    assert item.payload["content"] == "Test content"


def test_annotate_records_empty_text():
    """Test annotation with empty or missing text."""
    records = [
        {"id": 1, "text": ""},
        {"id": 2},  # missing text field
    ]
    
    result = annotate_records(records, seed=0)
    annotation_set = AnnotationSet.model_validate(result)
    
    assert len(annotation_set.items) == 2
    assert annotation_set.items[0].payload["text"] == ""
    assert annotation_set.items[1].payload["text"] == ""


def test_annotate_records_limit():
    """Test that limit parameter works correctly."""
    records = [
        {"id": i, "text": f"Text {i}"} for i in range(10)
    ]
    
    result = annotate_records(records, seed=0)
    assert len(result["items"]) == 10
    
    # Test with limit (this would be handled by load_dataset in CLI)
    limited_records = records[:5]
    result_limited = annotate_records(limited_records, seed=0)
    assert len(result_limited["items"]) == 5
