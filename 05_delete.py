"""
05_delete.py — Delete document chunks about Unity, Unreal and Blender

Run from the milvuslite-kit folder:
    python examples/05_delete.py
"""

from milvuslite_kit import MilvusLiteKit

with MilvusLiteKit.from_yaml("config.yaml") as kit:
    kit.sync_schema()

    # Total chunks before deleting
    print("--- before delete ---")
    all_chunks = kit.query("documents", filters={}, output_fields=["category"])
    print(f"  Total chunks: {len(all_chunks)}")

    # Delete a single chunk by id
    print("\n--- delete one chunk (unity-gs-chunk-01) ---")
    count = kit.delete("documents", filters={"id": {"eq": "unity-gs-chunk-01"}})
    print(f"  Deleted: {count}")

    # Delete all chunks of a specific document
    print("\n--- delete all chunks of 'Unreal Niagara Particle System' ---")
    count = kit.delete("documents", filters={"title": "Unreal Niagara Particle System"})
    print(f"  Deleted: {count}")

    # Delete all chunks of 'Blender Python Scripting' (also unpublished)
    print("\n--- delete all Blender Python Scripting chunks ---")
    count = kit.delete("documents", filters={"title": "Blender Python Scripting"})
    print(f"  Deleted: {count}")

    # Delete all unpublished chunks
    print("\n--- delete all unpublished chunks ---")
    count = kit.delete("documents", filters={"published": {"eq": False}})
    print(f"  Deleted: {count}")

    # Delete low quality chunks (score < 0.80)
    print("\n--- delete low quality chunks (score < 0.80) ---")
    count = kit.delete("documents", filters={"score": {"lt": 0.80}})
    print(f"  Deleted: {count}")

    # Remaining chunks after all deletes
    print("\n--- after delete ---")
    remaining = kit.query("documents", filters={}, output_fields=["category"])
    from collections import Counter
    counts = Counter(r["data"]["category"] for r in remaining)
    print(f"  Total remaining: {len(remaining)}")
    for cat, n in sorted(counts.items()):
        print(f"    {cat}: {n} chunks")
