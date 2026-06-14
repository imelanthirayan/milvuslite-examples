"""
04_search.py — Search for similar chunks about Unity, Unreal and Blender

Run from the milvuslite-kit folder:
    python examples/04_search.py
"""

import random
from milvuslite_kit import MilvusLiteKit

DIM = 128

def random_vector():
    return [random.uniform(0, 1) for _ in range(DIM)]

with MilvusLiteKit.from_yaml("config.yaml") as kit:
    kit.sync_schema()

    query_vector = random_vector()

    # Top 5 most similar chunks across all documents
    print("--- top 5 similar chunks (all categories) ---")
    results = kit.search("documents", vector=query_vector, vector_column="embedding", limit=5,
                         output_fields=["title", "content", "category"])
    print(results[0])
    for r in results:
        print(f"  [{r['data']['category']}]  {r['id']}  score={r['score']:.4f}")
        print(f"    {r['data']['content'][:70]}...")

    # Search only within Unity chunks
    print("\n--- top 5 similar Unity chunks ---")
    results = kit.search("documents", vector=query_vector, vector_column="embedding", limit=5,
                         filters={"category": "unity"},
                         output_fields=["title", "content"])
    print(results[0])
    for r in results:
        print(f"  {r['id']}  score={r['score']:.4f}")
        print(f"    {r['data']['content'][:70]}...")

    # Search only within Unreal chunks
    print("\n--- top 5 similar Unreal chunks ---")
    results = kit.search("documents", vector=query_vector, vector_column="embedding", limit=5,
                         filters={"category": "unreal"},
                         output_fields=["title", "content"])
    print(results[0])
    for r in results:
        print(f"  {r['id']}  score={r['score']:.4f}")
        print(f"    {r['data']['content'][:70]}...")

    # Search only within Blender chunks
    print("\n--- top 5 similar Blender chunks ---")
    results = kit.search("documents", vector=query_vector, vector_column="embedding", limit=5,
                         filters={"category": "blender"},
                         output_fields=["title", "content"])
    print(results[0])
    for r in results:
        print(f"  {r['id']}  score={r['score']:.4f}")
        print(f"    {r['data']['content'][:70]}...")

    # Search only published chunks
    print("\n--- top 5 from published chunks only ---")
    results = kit.search("documents", vector=query_vector, vector_column="embedding", limit=5,
                         filters={"published": {"eq": True}},
                         output_fields=["title", "category", "published"])
    print(results[0])
    for r in results:
        print(f"  [{r['data']['category']}]  {r['id']}  score={r['score']:.4f}  |  {r['data']['title']}")

    # Search within a specific document by title
    print("\n--- top 5 chunks from 'Blender Rendering with Cycles and EEVEE' ---")
    results = kit.search("documents", vector=query_vector, vector_column="embedding", limit=5,
                         filters={"title": "Blender Rendering with Cycles and EEVEE"},
                         output_fields=["title", "content"])
    print(results[0])
    for r in results:
        print(f"  {r['id']}  score={r['score']:.4f}")
        print(f"    {r['data']['content'][:70]}...")
