import json
import pytest
from pathlib import Path

from annotatorx.validators.schemas import AnnotationSet, AnnotationItem


def test_annotation_schema_valid():
    """Test that valid annotation data passes schema validation."""
    valid_data = {
        "version": 1,
        "items": [
            {
                "id": 1,
                "payload": {
                    "text": "Test text",
                    "label": "POSITIVE"
                },
                "meta": {
                    "source": "test",
                    "seed": 0
                }
            }
        ]
    }
    
    annotation_set = AnnotationSet.model_validate(valid_data)
    assert annotation_set.version == 1
    assert len(annotation_set.items) == 1
    assert annotation_set.items[0].id == 1


def test_annotation_schema_invalid_missing_version():
    """Test that missing version field fails validation."""
    invalid_data = {
        "items": [
            {
                "id": 1,
                "payload": {"text": "Test", "label": "POSITIVE"},
                "meta": {"source": "test"}
            }
        ]
    }
    
    with pytest.raises(Exception):  # pydantic.ValidationError
        AnnotationSet.model_validate(invalid_data)


def test_annotation_schema_invalid_missing_id():
    """Test that missing id field fails validation."""
    invalid_data = {
        "version": 1,
        "items": [
            {
                "payload": {"text": "Test", "label": "POSITIVE"},
                "meta": {"source": "test"}
            }
        ]
    }
    
    with pytest.raises(Exception):  # pydantic.ValidationError
        AnnotationSet.model_validate(invalid_data)


def test_annotation_item_optional_fields():
    """Test that payload and meta are optional with defaults."""
    minimal_data = {
        "version": 1,
        "items": [
            {"id": 1}
        ]
    }
    
    annotation_set = AnnotationSet.model_validate(minimal_data)
    item = annotation_set.items[0]
    assert item.payload == {}
    assert item.meta == {}


def test_annotation_schema_empty_items():
    """Test that empty items list is valid."""
    empty_data = {
        "version": 1,
        "items": []
    }
    
    annotation_set = AnnotationSet.model_validate(empty_data)
    assert len(annotation_set.items) == 0


def test_annotation_item_id_types():
    """Test that id can be int or string."""
    data_int_id = {
        "version": 1,
        "items": [{"id": 1}]
    }
    
    data_str_id = {
        "version": 1,
        "items": [{"id": "item_1"}]
    }
    
    # Both should be valid
    AnnotationSet.model_validate(data_int_id)
    AnnotationSet.model_validate(data_str_id)
