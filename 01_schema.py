"""
01_schema.py — Schema operations

Run from the milvuslite-kit folder:
    python examples/01_schema.py
"""

from milvuslite_kit import MilvusLiteKit

with MilvusLiteKit.from_yaml("config.yaml") as kit:

    # Create collections and indexes from config
    print("--- sync_schema ---")
    kit.sync_schema()

    # Check that fields and dimensions match the config
    print("\n--- validate_schema ---")
    kit.validate_schema()

    # List all collections in the database
    print("\n--- list_collections ---")
    print(kit.list_collections())

    # Check if a collection exists
    print("\n--- collection_exists ---")
    print("documents:", kit.collection_exists("documents"))
    print("nonexistent:", kit.collection_exists("nonexistent"))

    # Show collection details (fields, types, index)
    print("\n--- describe_collection ---")
    print(kit.describe_collection("documents"))

    # Drop and recreate a collection (erases all data)
    print("\n--- reset_collection ---")
    kit.reset_collection("documents")
    print("documents reset.")

    # Permanently delete a collection (uncomment to use)
    # kit.drop_collection("documents")
