"""
03_query.py — Query document chunks about Unity, Unreal and Blender

Run from the milvuslite-kit folder:
    python examples/03_query.py
"""

from milvuslite_kit import MilvusLiteKit

with MilvusLiteKit.from_yaml("config.yaml") as kit:
    kit.sync_schema()

    # All Unity chunks
    print("--- category == unity ---")
    results = kit.query("documents", filters={"category": "unity"}, output_fields=["title", "category"])
    print(results[0])
    for r in results:
        print(f"  {r['id']}  |  {r['data']['title']}")
    

    # All published chunks
    print("\n--- published == True ---")
    results = kit.query("documents", filters={"published": {"eq": True}}, output_fields=["title", "category"])
    print(results[0])
    print(f"  {len(results)} published chunks")

    # Unpublished chunks (drafts)
    print("\n--- published == False ---")
    results = kit.query("documents", filters={"published": {"eq": False}}, output_fields=["title", "category"])
    print(results[0])
    for r in results:
        print(f"  {r['id']}  |  {r['data']['title']}")

    # High quality chunks (score >= 0.95)
    print("\n--- score >= 0.95 ---")
    results = kit.query("documents", filters={"score": {"gte": 0.95}}, output_fields=["title", "score"])
    print(results[0])
    for r in results:
        print(f"  {r['id']}  |  score={r['data']['score']}")

    # Unreal or Blender chunks
    print("\n--- category in [unreal, blender] ---")
    results = kit.query("documents", filters={"category": {"in": ["unreal", "blender"]}}, output_fields=["title", "category"])
    print(results[0])
    print(f"  {len(results)} chunks from unreal and blender")

    # All chunks for a specific document
    print("\n--- title == 'Unity Physics System' ---")
    results = kit.query("documents", filters={"title": "Unity Physics System"}, output_fields=["title", "content"])
    print(results[0])
    for r in results:
        print(f"  {r['id']}  |  {r['data']['content'][:65]}...")

    # Blender chunks with high score
    print("\n--- blender with score >= 0.95 ---")
    results = kit.query("documents",
                        filters={"category": "blender", "score": {"gte": 0.95}},
                        output_fields=["title", "score"])
    print(results[0])
    for r in results:
        print(f"  {r['id']}  |  {r['data']['title']}  score={r['data']['score']}")
