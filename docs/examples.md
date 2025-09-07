# AnnotatorX Examples

This document provides practical examples of using AnnotatorX for data annotation workflows.

## Basic Workflow Example

### 1. Prepare Your Dataset

Create a CSV file with your data:

```csv
id,text
1,"I love this new feature!"
2,"The interface is confusing."
3,"It works as expected."
4,"Terrible performance issues."
5,"Great customer support team."
```

Save as `my_reviews.csv`.

### 2. Ingest the Dataset

```bash
python -m annotatorx ingest my_reviews.csv --name product_reviews
```

This copies the file to `datasets/product_reviews.csv`.

### 3. Annotate the Data

```bash
python -m annotatorx annotate product_reviews --seed 42 --output annotations/reviews_annotated.json
```

This creates annotations with deterministic labels based on seed 42.

### 4. Validate the Annotations

```bash
python -m annotatorx validate annotations/reviews_annotated.json
```

### 5. Export Results

```bash
# Export to CSV
python -m annotatorx export annotations/reviews_annotated.json --format csv --output results.csv

# Export to JSON
python -m annotatorx export annotations/reviews_annotated.json --format json --output results.json
```

### 6. View Statistics

```bash
python -m annotatorx stats annotations/reviews_annotated.json
```

Output:
```
┌─────────────────┬───────┐
│ Label           │ Count │
├─────────────────┼───────┤
│ NEGATIVE        │ 2     │
│ NEUTRAL         │ 1     │
│ POSITIVE        │ 2     │
│ TOTAL           │ 5     │
└─────────────────┴───────┘
```

## Custom Field Names Example

If your dataset uses different field names:

```csv
id,content
1,"I love this new feature!"
2,"The interface is confusing."
```

Use custom field names:

```bash
python -m annotatorx annotate my_dataset --text-field content --label-field sentiment
```

## JSON Dataset Example

Create a JSON dataset:

```json
{
  "data": [
    {"id": 1, "text": "Excellent product quality"},
    {"id": 2, "text": "Poor customer service"},
    {"id": 3, "text": "Average experience overall"}
  ]
}
```

Ingest and annotate:

```bash
python -m annotatorx ingest my_data.json --name json_dataset
python -m annotatorx annotate json_dataset --seed 0
```

## Docker Workflow Example

### Using Docker directly:

```bash
# Build the image
docker build -t annotatorx .

# Run annotation pipeline
docker run --rm \
  -v $(pwd)/datasets:/app/datasets \
  -v $(pwd)/annotations:/app/annotations \
  annotatorx \
  python -m annotatorx annotate example_dataset --seed 0
```

### Using docker-compose:

```bash
# Run tests
docker-compose run --rm test

# Validate example data
docker-compose run --rm validate

# Run custom annotation
docker-compose run --rm annotatorx python -m annotatorx annotate example_dataset --seed 42
```

## Batch Processing Example

Process multiple datasets:

```bash
#!/bin/bash

# List of datasets to process
datasets=("reviews_2023" "reviews_2024" "feedback_q1" "feedback_q2")

for dataset in "${datasets[@]}"; do
    echo "Processing $dataset..."
    
    # Annotate with different seeds for variety
    seed=$((RANDOM % 1000))
    python -m annotatorx annotate "$dataset" --seed "$seed" --output "annotations/${dataset}_annotated.json"
    
    # Validate
    python -m annotatorx validate "annotations/${dataset}_annotated.json"
    
    # Export to CSV
    python -m annotatorx export "annotations/${dataset}_annotated.json" --format csv --output "results/${dataset}_results.csv"
    
    # Show stats
    python -m annotatorx stats "annotations/${dataset}_annotated.json"
done
```

## Reproducibility Example

Ensure reproducible results by using the same seed:

```bash
# First run
python -m annotatorx annotate my_dataset --seed 123 --output annotations/run1.json

# Second run with same seed - should produce identical results
python -m annotatorx annotate my_dataset --seed 123 --output annotations/run2.json

# Compare results
diff annotations/run1.json annotations/run2.json
# Should show no differences
```

## Testing Example

Run the test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_pipeline.py -v

# Run with coverage
python -m pytest tests/ --cov=annotatorx --cov-report=html
```

## CI/CD Example

The included GitHub Actions workflow automatically:

1. Runs tests on every push
2. Validates example annotations
3. Tests Docker builds
4. Ensures reproducibility

View the workflow in `.github/workflows/ci.yml`.

## Custom Annotation Logic

To extend the annotation pipeline, modify `annotatorx/pipeline/annotate.py`:

```python
def custom_annotate_records(records, **kwargs):
    """Custom annotation logic."""
    items = []
    for idx, rec in enumerate(records):
        text = rec.get("text", "")
        
        # Custom annotation logic here
        if "great" in text.lower():
            label = "POSITIVE"
        elif "terrible" in text.lower():
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"
        
        items.append({
            "id": rec.get("id", idx),
            "payload": {"text": text, "label": label},
            "meta": {"source": "custom_annotator"}
        })
    
    return {"version": 1, "items": items}
```

## Error Handling Examples

### Invalid dataset format:
```bash
python -m annotatorx ingest invalid_file.txt
# Error: Unsupported format: txt
```

### Missing dataset:
```bash
python -m annotatorx annotate nonexistent_dataset
# Error: Dataset not found: nonexistent_dataset (.csv or .json)
```

### Invalid annotations:
```bash
python -m annotatorx validate invalid_annotations.json
# Error: Validation failed: [detailed Pydantic error]
```

## Performance Tips

1. **Use limits for large datasets:**
   ```bash
   python -m annotatorx annotate large_dataset --limit 1000
   ```

2. **Process in batches:**
   ```bash
   # Split large CSV into smaller files
   split -l 1000 large_dataset.csv batch_
   
   # Process each batch
   for file in batch_*; do
       python -m annotatorx ingest "$file"
       python -m annotatorx annotate "${file%.csv}"
   done
   ```

3. **Use Docker for isolation:**
   ```bash
   docker run --rm -v $(pwd):/workspace annotatorx \
     python -m annotatorx annotate dataset --seed 0
   ```
