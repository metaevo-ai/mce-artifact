#!/usr/bin/env python3
"""
Data filtering utility for selecting categories and splits, filtering by reconstruction_id_if_redacted.
"""

import json
import argparse
import sys
import random
from pathlib import Path
from typing import List, Set, Optional, Dict

# Base path for data
#DATA_BASE_PATH = Path(__file__).parent / "new-data"
DATA_BASE_PATH = Path(__file__).parent / "data"

# Available categories
AVAILABLE_CATEGORIES = [
    "Controlled_Regulated_Substances",
    "Copyright_Trademark_Plagiarism",
    "Criminal_Planning_Confessions",
    "Fraud_Deception",
    "Guns_and_Illegal_Weapons",
    "Harassment",
    "Hate_Identity_Hate",
    "High_Risk_Gov_Decision_Making",
    "Illegal_Activity",
    "Immoral_Unethical",
    "Malware",
    "Needs_Caution",
    "Other",
    "PII_Privacy",
    "Political_Misinformation_Conspiracy",
    "Profanity",
    "safe",
    "Sexual_minor",
    "Sexual",
    "Suicide_and_Self_Harm",
    "Threat",
    "Unauthorized_Advice",
    "Violence",
]

AVAILABLE_SPLITS = ["train", "valid", "test"]


def print_help():
    """Print help message with available categories and splits."""
    print("Data Filtering Utility")
    print("=" * 60)
    print()
    print("Available categories:")
    for i, cat in enumerate(AVAILABLE_CATEGORIES, 1):
        print(f"  {i}. {cat}")
    print()
    print(f"Available splits: {', '.join(AVAILABLE_SPLITS)}")
    print()
    print("Usage:")
    print("  python filter_data.py --categories CATEGORY1 CATEGORY2 ... --split SPLIT [OPTIONS]")
    print()
    print("Options:")
    print("  --extract-ids              Extract sample IDs instead of filtering data")
    print("  --sample-output FILE       Output file for sample IDs (default: sample_ids.jsonl)")
    print("  --output FILE              Output file for filtered data (default: temp.jsonl)")
    print("  --max-per-category N1 N2.. Max samples per category via random sampling")
    print("                             (space-separated, must match number of categories)")
    print("                             If not provided, all samples are extracted")
    print()
    print("Examples:")
    print("  # Filter data and keep records with null reconstruction_id_if_redacted")
    print("  python filter_data.py --categories safe --split valid")
    print()
    print("  # Extract sample IDs from multiple categories")
    print("  python filter_data.py --categories safe PII_Privacy --split train --extract-ids")
    print()
    print("  # Extract sample IDs with limit (max 100 from safe, max 50 from PII_Privacy)")
    print("  python filter_data.py --categories safe PII_Privacy --split valid --extract-ids --max-per-category 100 50")
    print()
    print("  # Extract sample IDs to custom output file with sampling")
    print("  python filter_data.py --categories safe --split test --extract-ids --max-per-category 50 --sample-output my_samples.jsonl")
    print()
    print("  # Show this message")
    print("  python filter_data.py --help-categories")
    print()


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Filter data by categories and split, extracting records with null reconstruction_id_if_redacted"
    )
    parser.add_argument(
        "--help-categories",
        action="store_true",
        help="Show available categories and splits, then exit",
    )
    parser.add_argument(
        "--categories",
        nargs="+",
        required=False,
        help="Categories to filter (space-separated)",
    )
    parser.add_argument(
        "--split",
        choices=AVAILABLE_SPLITS,
        required=False,
        help="Data split to use (train, valid, or test)",
    )
    parser.add_argument(
        "--output",
        default="temp.jsonl",
        help="Output file path (default: temp.jsonl)",
    )
    parser.add_argument(
        "--extract-ids",
        action="store_true",
        help="Extract id and categories to a sample ID file instead of filtering data",
    )
    parser.add_argument(
        "--sample-output",
        default="sample_ids.jsonl",
        help="Output file for sample IDs (default: sample_ids.jsonl)",
    )
    parser.add_argument(
        "--max-per-category",
        type=int,
        nargs="+",
        default=None,
        help="Maximum number of samples to extract per category (space-separated integers, must match number of categories). If not provided, all samples are extracted.",
    )

    args = parser.parse_args()

    # Show help and exit if requested
    if args.help_categories:
        print_help()
        sys.exit(0)

    # Validate that categories and split are provided if not showing help
    if not args.categories or not args.split:
        print("Error: --categories and --split are required")
        print("Use --help-categories to see available options")
        sys.exit(1)

    # Validate extract-ids mode
    if args.extract_ids and args.output != "temp.jsonl":
        print("Warning: --output is ignored when using --extract-ids. Use --sample-output instead.")

    # Validate max-per-category if provided
    if args.max_per_category is not None:
        if len(args.max_per_category) != len(args.categories):
            print(f"Error: --max-per-category must have {len(args.categories)} values (one per category)")
            print(f"You provided {len(args.max_per_category)} values")
            sys.exit(1)
        # Check all values are positive
        if any(x <= 0 for x in args.max_per_category):
            print("Error: All values in --max-per-category must be positive integers")
            sys.exit(1)

    return args


def validate_categories(categories: List[str]) -> Set[str]:
    """Validate that provided categories exist."""
    invalid_categories = set(categories) - set(AVAILABLE_CATEGORIES)
    if invalid_categories:
        print(f"Error: Invalid categories: {', '.join(invalid_categories)}")
        print(f"Available categories: {', '.join(AVAILABLE_CATEGORIES)}")
        sys.exit(1)
    return set(categories)


def filter_data(
    categories: Set[str], split: str, output_file: str, max_per_category: Optional[Dict[str, int]] = None
) -> None:
    """Filter data from JSONL files and save records with null reconstruction_id_if_redacted.

    Args:
        categories: Set of category names to process
        split: Data split to use (train, valid, test)
        output_file: Output file path
        max_per_category: Dict mapping category to max number of samples. If None, all samples are extracted.
    """
    output_path = Path(output_file)

    total_records = 0
    filtered_records = 0
    category_counts = {cat: 0 for cat in categories}

    with open(output_path, "w") as out_f:
        for category in sorted(categories):
            file_path = DATA_BASE_PATH / split / f"{category}.jsonl"

            if not file_path.exists():
                print(f"Warning: File not found: {file_path}")
                continue

            print(f"Processing: {file_path}")

            # Get max limit for this category
            max_limit = None if max_per_category is None else max_per_category.get(category)

            # If max_limit is set, collect all matching records first then sample
            if max_limit is not None:
                matching_records = []
                with open(file_path, "r") as in_f:
                    for line in in_f:
                        try:
                            record = json.loads(line.strip())
                            total_records += 1

                            # Filter by reconstruction_id_if_redacted being null
                            if record.get("reconstruction_id_if_redacted") is None:
                                matching_records.append(record)

                        except json.JSONDecodeError as e:
                            print(f"Warning: Invalid JSON in {file_path}: {e}")
                            continue

                # Sample from matching records
                num_to_sample = min(max_limit, len(matching_records))
                sampled_records = random.sample(matching_records, num_to_sample)

                for record in sampled_records:
                    out_f.write(json.dumps(record) + "\n")
                    filtered_records += 1
                    category_counts[category] += 1

            else:
                # No limit, extract all matching records
                with open(file_path, "r") as in_f:
                    for line in in_f:
                        try:
                            record = json.loads(line.strip())
                            total_records += 1

                            # Filter by reconstruction_id_if_redacted being null
                            if record.get("reconstruction_id_if_redacted") is None:
                                out_f.write(json.dumps(record) + "\n")
                                filtered_records += 1
                                category_counts[category] += 1

                        except json.JSONDecodeError as e:
                            print(f"Warning: Invalid JSON in {file_path}: {e}")
                            continue

    print()
    print("=" * 60)
    print(f"Filtering complete!")
    print(f"Total records processed: {total_records}")
    print(f"Filtered records (reconstruction_id_if_redacted is null): {filtered_records}")

    # Print per-category counts if sampling was applied
    if max_per_category is not None:
        print(f"\nFiltered records per category:")
        for cat in sorted(categories):
            limit = max_per_category.get(cat, "unlimited")
            count = category_counts[cat]
            print(f"  {cat}: {count} / {limit}")

    print(f"Output file: {output_path.absolute()}")


def extract_sample_ids(
    categories: Set[str], split: str, output_file: str, max_per_category: Optional[Dict[str, int]] = None
) -> None:
    """Extract sample IDs and categories from JSONL files with null reconstruction_id_if_redacted.

    Args:
        categories: Set of category names to process
        split: Data split to use (train, valid, test)
        output_file: Output file path
        max_per_category: Dict mapping category to max number of samples. If None, all samples are extracted.
    """
    output_path = Path(output_file)

    total_records = 0
    extracted_samples = 0
    category_counts = {cat: 0 for cat in categories}

    with open(output_path, "w") as out_f:
        for category in sorted(categories):
            file_path = DATA_BASE_PATH / split / f"{category}.jsonl"

            if not file_path.exists():
                print(f"Warning: File not found: {file_path}")
                continue

            print(f"Processing: {file_path}")

            # Get max limit for this category
            max_limit = None if max_per_category is None else max_per_category.get(category)

            # If max_limit is set, collect all matching records first then sample
            if max_limit is not None:
                matching_records = []
                with open(file_path, "r") as in_f:
                    for line in in_f:
                        try:
                            record = json.loads(line.strip())
                            total_records += 1

                            # Filter by reconstruction_id_if_redacted being null
                            if record.get("reconstruction_id_if_redacted") is None:
                                matching_records.append(record)

                        except json.JSONDecodeError as e:
                            print(f"Warning: Invalid JSON in {file_path}: {e}")
                            continue

                # Sample from matching records
                num_to_sample = min(max_limit, len(matching_records))
                sampled_records = random.sample(matching_records, num_to_sample)

                for record in sampled_records:
                    sample_record = {
                        "id": record.get("id"),
                        "categories": [category]
                    }
                    out_f.write(json.dumps(sample_record) + "\n")
                    extracted_samples += 1
                    category_counts[category] += 1

            else:
                # No limit, extract all matching records
                with open(file_path, "r") as in_f:
                    for line in in_f:
                        try:
                            record = json.loads(line.strip())
                            total_records += 1

                            # Filter by reconstruction_id_if_redacted being null
                            if record.get("reconstruction_id_if_redacted") is None:
                                sample_record = {
                                    "id": record.get("id"),
                                    "categories": [category]
                                }
                                out_f.write(json.dumps(sample_record) + "\n")
                                extracted_samples += 1
                                category_counts[category] += 1

                        except json.JSONDecodeError as e:
                            print(f"Warning: Invalid JSON in {file_path}: {e}")
                            continue

    print()
    print("=" * 60)
    print(f"Sample ID extraction complete!")
    print(f"Total records processed: {total_records}")
    print(f"Sample IDs extracted (reconstruction_id_if_redacted is null): {extracted_samples}")

    # Print per-category counts
    if max_per_category is not None:
        print(f"\nSamples per category:")
        for cat in sorted(categories):
            limit = max_per_category.get(cat, "unlimited")
            count = category_counts[cat]
            print(f"  {cat}: {count} / {limit}")

    print(f"Output file: {output_path.absolute()}")


def main():
    args = parse_arguments()

    # Validate categories
    categories = validate_categories(args.categories)

    print(f"Selected categories: {', '.join(sorted(categories))}")
    print(f"Selected split: {args.split}")

    # Build max_per_category mapping if provided
    max_per_category = None
    if args.max_per_category is not None:
        sorted_categories = sorted(categories)
        max_per_category = dict(zip(sorted_categories, args.max_per_category))
        print(f"Max samples per category: {max_per_category}")

    print()

    # Choose operation
    if args.extract_ids:
        print("Mode: Extract sample IDs")
        extract_sample_ids(categories, args.split, args.sample_output, max_per_category)
    else:
        print("Mode: Filter data")
        filter_data(categories, args.split, args.output, max_per_category)


if __name__ == "__main__":
    main()
