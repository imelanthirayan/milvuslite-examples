# milvuslite-kit Examples

Hands-on examples for [**milvuslite-kit**](https://github.com/imelanthirayan/milvuslite-kit) — a lightweight, YAML-driven Python wrapper for [Milvus Lite](https://milvus.io/docs/milvus_lite.md) that gives you vector search with zero server setup.

---

## 📦 Get the Kit

```bash
git clone https://github.com/imelanthirayan/milvuslite-kit.git
cd milvuslite-kit
pip install -e .
```

---

## 📂 What's in This Folder

| File | What it covers |
|------|----------------|
| `config.yaml` | Collection schema, index, and logging config |
| `01_schema.py` | Create, validate, list, describe, reset collections |
| `02_insert.py` | Insert single records and bulk-insert hundreds of chunks |
| `03_query.py` | Filter records by field values (exact, range, boolean, list) |
| `04_search.py` | Semantic vector search with optional filters |
| `05_delete.py` | Delete records by ID, field value, or filter expression |

The examples use a **documents** collection containing chunked articles about Unity, Unreal Engine, and Blender — similar to a real RAG pipeline.

---

## ⚙️ Config (`config.yaml`)

All examples share a single config file. It defines the database path, logging options, and the `documents` collection schema:

```yaml
database:
  name: examples_db
  path: ./data/examples.db

logging:
  enabled: true
  level: INFO
  log_to_console: true
  redact_vectors: true

collections:
  documents:
    enabled: true
    primary_key:
      field: id
      auto_id: false
    columns:
      - name: title
        type: text
      - name: content
        type: text
      - name: category
        type: text
      - name: score
        type: float
      - name: published
        type: bool
      - name: metadata
        type: json
      - name: embedding
        type: vector
        dimension: 128
        metric_type: COSINE
        index:
          enabled: true
          type: FLAT
```

---

## 🚀 Running the Examples

Run each script from the `milvuslite-examples` folder in order:

```bash
# 1. Set up the schema
python 01_schema.py

# 2. Insert data
python 02_insert.py

# 3. Query by filters
python 03_query.py

# 4. Semantic vector search
python 04_search.py

# 5. Delete records
python 05_delete.py
```

---

## 1️⃣ Schema (`01_schema.py`)

Covers collection lifecycle operations — all driven from `config.yaml`.

```python
from milvuslite_kit import MilvusLiteKit

with MilvusLiteKit.from_yaml("config.yaml") as kit:

    # Create collections and indexes from config
    kit.sync_schema()

    # Check that fields and dimensions match the config
    kit.validate_schema()

    # List all collections in the database
    print(kit.list_collections())

    # Check if a collection exists
    print(kit.collection_exists("documents"))

    # Show collection details (fields, types, index)
    print(kit.describe_collection("documents"))

    # Drop and recreate a collection (erases all data)
    kit.reset_collection("documents")
```

---

## 2️⃣ Insert (`02_insert.py`)

Inserts hundreds of document chunks (simulating a RAG pipeline). Each document is split into multiple chunks sharing the same title but with unique IDs.

```python
from milvuslite_kit import MilvusLiteKit
import random

DIM = 128

def random_vector():
    return [random.uniform(0, 1) for _ in range(DIM)]

with MilvusLiteKit.from_yaml("config.yaml") as kit:
    kit.sync_schema()

    # Insert a single record
    kit.insert("documents", {
        "id": "doc-001",
        "title": "Getting Started with Unity",
        "content": "Unity is a cross-platform game engine...",
        "category": "unity",
        "score": 0.97,
        "published": True,
        "embedding": random_vector(),
    })

    # Bulk insert multiple records at once
    kit.bulk_insert("documents", [
        {"id": "doc-002", "title": "...", "content": "...", "embedding": random_vector()},
        {"id": "doc-003", "title": "...", "content": "...", "embedding": random_vector()},
    ])
```

---

## 3️⃣ Query (`03_query.py`)

Fetch records using field-level filters — no vectors needed.

```python
from milvuslite_kit import MilvusLiteKit

with MilvusLiteKit.from_yaml("config.yaml") as kit:
    kit.sync_schema()

    # Exact match (shorthand)
    results = kit.query("documents", filters={"category": "unity"},
                        output_fields=["title", "category"])

    # Boolean filter
    results = kit.query("documents", filters={"published": {"eq": True}},
                        output_fields=["title", "category"])

    # Range filter
    results = kit.query("documents", filters={"score": {"gte": 0.95}},
                        output_fields=["title", "score"])

    # List filter
    results = kit.query("documents", filters={"category": {"in": ["unreal", "blender"]}},
                        output_fields=["title", "category"])

    # Combined filters
    results = kit.query("documents",
                        filters={"category": "blender", "score": {"gte": 0.95}},
                        output_fields=["title", "score"])
```

**Filter operators:**

| Operator | Meaning |
|----------|---------|
| `eq` | `==` |
| `ne` | `!=` |
| `gt` | `>` |
| `gte` | `>=` |
| `lt` | `<` |
| `lte` | `<=` |
| `in` | `in [...]` |

Shorthand: `{"field": "value"}` is equivalent to `{"field": {"eq": "value"}}`.

---

## 4️⃣ Search (`04_search.py`)

Semantic vector search — find the most similar records to a query vector, with optional filters.

```python
from milvuslite_kit import MilvusLiteKit
import random

DIM = 128
query_vector = [random.uniform(0, 1) for _ in range(DIM)]

with MilvusLiteKit.from_yaml("config.yaml") as kit:
    kit.sync_schema()

    # Top 5 most similar across all records
    results = kit.search("documents", vector=query_vector,
                         vector_column="embedding", limit=5,
                         output_fields=["title", "content", "category"])

    # Filtered search — Unity only
    results = kit.search("documents", vector=query_vector,
                         vector_column="embedding", limit=5,
                         filters={"category": "unity"},
                         output_fields=["title", "content"])

    # Filtered search — published only
    results = kit.search("documents", vector=query_vector,
                         vector_column="embedding", limit=5,
                         filters={"published": {"eq": True}},
                         output_fields=["title", "category"])

    for r in results:
        print(r["id"], r["score"], r["data"]["title"])
```

**Result format:**
```python
{"id": "doc-001", "score": 0.9741, "collection": "documents", "data": {"title": "...", "content": "..."}}
```

---

## 5️⃣ Delete (`05_delete.py`)

Delete records by ID, field value, range, or any filter expression.

```python
from milvuslite_kit import MilvusLiteKit

with MilvusLiteKit.from_yaml("config.yaml") as kit:
    kit.sync_schema()

    # Delete a single record by ID
    count = kit.delete("documents", filters={"id": {"eq": "unity-gs-chunk-01"}})

    # Delete all chunks of a specific document
    count = kit.delete("documents", filters={"title": "Unreal Niagara Particle System"})

    # Delete all unpublished records
    count = kit.delete("documents", filters={"published": {"eq": False}})

    # Delete low-quality records
    count = kit.delete("documents", filters={"score": {"lt": 0.80}})

    print(f"Deleted: {count}")
```

---

## 🔗 Links

- **Kit repository:** https://github.com/imelanthirayan/milvuslite-kit
- **Milvus Lite docs:** https://milvus.io/docs/milvus_lite.md
- **pymilvus:** https://github.com/milvus-io/pymilvus
