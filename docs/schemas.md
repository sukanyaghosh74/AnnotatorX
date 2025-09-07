# AnnotatorX Schema Documentation

This document describes the data schemas used in AnnotatorX for datasets and annotations.

## Dataset Schemas

### CSV Dataset Format

CSV datasets should have a header row with column names. The following columns are expected:

- `id`: Unique identifier for each record (integer or string)
- `text`: Text content to be annotated (string)

**Example:**
```csv
id,text
1,"This is a great product!"
2,"I hate this service."
3,"It's okay, nothing special."
```

### JSON Dataset Format

JSON datasets can be in two formats:

#### Format 1: Object with data array
```json
{
  "data": [
    {"id": 1, "text": "This is a great product!"},
    {"id": 2, "text": "I hate this service."},
    {"id": 3, "text": "It's okay, nothing special."}
  ]
}
```

#### Format 2: Direct array
```json
[
  {"id": 1, "text": "This is a great product!"},
  {"id": 2, "text": "I hate this service."},
  {"id": 3, "text": "It's okay, nothing special."}
]
```

## Annotation Schema

Annotations follow a structured JSON format defined by Pydantic models:

### AnnotationSet

The root container for all annotations:

```python
class AnnotationSet(BaseModel):
    version: int = 1
    items: List[AnnotationItem] = Field(default_factory=list)
```

**Fields:**
- `version`: Schema version (currently 1)
- `items`: List of annotation items

### AnnotationItem

Individual annotation records:

```python
class AnnotationItem(BaseModel):
    id: int | str
    payload: Dict[str, Any] = Field(default_factory=dict)
    meta: Dict[str, Any] = Field(default_factory=dict)
```

**Fields:**
- `id`: Unique identifier matching the original dataset record
- `payload`: Annotation data (text, labels, etc.)
- `meta`: Metadata about the annotation process

### Example Annotation

```json
{
  "version": 1,
  "items": [
    {
      "id": 1,
      "payload": {
        "text": "This is a great product!",
        "label": "POSITIVE"
      },
      "meta": {
        "source": "annotatorx.simple_labeler",
        "seed": 0
      }
    },
    {
      "id": 2,
      "payload": {
        "text": "I hate this service.",
        "label": "NEGATIVE"
      },
      "meta": {
        "source": "annotatorx.simple_labeler",
        "seed": 0
      }
    }
  ]
}
```

## Validation Rules

### Required Fields
- `AnnotationSet.version`: Must be present
- `AnnotationItem.id`: Must be present (int or string)

### Optional Fields
- `AnnotationItem.payload`: Defaults to empty dict
- `AnnotationItem.meta`: Defaults to empty dict

### Data Types
- `id`: Can be integer or string
- `payload`: Dictionary with any string keys and any values
- `meta`: Dictionary with any string keys and any values

## Label Values

The current annotation pipeline produces labels from the set:
- `"POSITIVE"`
- `"NEGATIVE"`
- `"NEUTRAL"`

Labels are assigned deterministically based on the input text and seed value.

## Schema Evolution

When extending the schema:

1. **Backward Compatibility**: New fields should be optional with sensible defaults
2. **Version Increment**: Update the version number for breaking changes
3. **Validation**: Add appropriate Pydantic validators
4. **Documentation**: Update this schema documentation
5. **Tests**: Add test cases for new schema features

## Custom Field Names

The CLI supports custom field names for different annotation tasks:

- `--text-field`: Specify the input text field name (default: "text")
- `--label-field`: Specify the output label field name (default: "label")

This allows flexibility in dataset formats while maintaining consistent annotation output.
