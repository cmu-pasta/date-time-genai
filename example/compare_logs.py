#!/usr/bin/env python3
"""
Script to compare dt_log.txt and pd_log.txt and report percentage of non-matching lines.
"""

import os
from pathlib import Path


def compare_log_files(file1_path, file2_path):
    """
    Compare two log files line by line and return statistics.

    Args:
        file1_path (str): Path to first log file
        file2_path (str): Path to second log file

    Returns:
        dict: Statistics about the comparison
    """
    try:
        with open(file1_path, "r") as f1, open(file2_path, "r") as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        return None
    except Exception as e:
        print(f"Error reading files: {e}")
        return None

    # Get the minimum length to avoid index errors
    min_length = min(len(lines1), len(lines2))
    max_length = max(len(lines1), len(lines2))

    # Count matching and non-matching lines
    matching_lines = 0
    non_matching_lines = 0

    # Compare lines that exist in both files
    for i in range(min_length):
        line1 = lines1[i].strip()
        line2 = lines2[i].strip()

        if line1 == line2:
            matching_lines += 1
        else:
            non_matching_lines += 1

    # If files have different lengths, all extra lines are considered non-matching
    extra_lines = max_length - min_length
    non_matching_lines += extra_lines

    total_lines = max_length

    # Calculate percentages
    if total_lines > 0:
        matching_percentage = (matching_lines / total_lines) * 100
        non_matching_percentage = (non_matching_lines / total_lines) * 100
    else:
        matching_percentage = 0
        non_matching_percentage = 0

    return {
        "file1_lines": len(lines1),
        "file2_lines": len(lines2),
        "total_lines_compared": total_lines,
        "matching_lines": matching_lines,
        "non_matching_lines": non_matching_lines,
        "matching_percentage": matching_percentage,
        "non_matching_percentage": non_matching_percentage,
        "length_difference": abs(len(lines1) - len(lines2)),
    }


def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent

    # Define file paths
    dt_log_path = script_dir / "dt_log.txt"
    pd_log_path = script_dir / "pd_log.txt"

    print("Comparing log files...")
    print(f"File 1: {dt_log_path}")
    print(f"File 2: {pd_log_path}")
    print("-" * 50)

    # Compare the files
    results = compare_log_files(dt_log_path, pd_log_path)

    if results is None:
        return

    # Display results
    print(f"File 1 (dt_log.txt) lines: {results['file1_lines']:,}")
    print(f"File 2 (pd_log.txt) lines: {results['file2_lines']:,}")
    print(f"Total lines compared: {results['total_lines_compared']:,}")
    print()
    print(f"Matching lines: {results['matching_lines']:,}")
    print(f"Non-matching lines: {results['non_matching_lines']:,}")
    print()
    print(f"Matching percentage: {results['matching_percentage']:.2f}%")
    print(f"Non-matching percentage: {results['non_matching_percentage']:.2f}%")

    if results["length_difference"] > 0:
        print(
            f"\nNote: Files have different lengths (difference: {results['length_difference']} lines)"
        )

    # Show some examples of differences if there are any
    if results["non_matching_lines"] > 0:
        print("\nShowing first 5 differences:")
        show_differences(dt_log_path, pd_log_path, max_examples=5)


def show_differences(file1_path, file2_path, max_examples=5):
    """Show examples of differing lines between the two files."""
    try:
        with open(file1_path, "r") as f1, open(file2_path, "r") as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
    except Exception as e:
        print(f"Error reading files for examples: {e}")
        return

    min_length = min(len(lines1), len(lines2))
    examples_shown = 0

    for i in range(min_length):
        if examples_shown >= max_examples:
            break

        line1 = lines1[i].strip()
        line2 = lines2[i].strip()

        if line1 != line2:
            examples_shown += 1
            print(f"\nLine {i+1}:")
            print(f"  dt_log.txt: {line1}")
            print(f"  pd_log.txt: {line2}")

    # Show length differences if any
    if len(lines1) != len(lines2):
        print(f"\nFiles have different lengths:")
        print(f"  dt_log.txt: {len(lines1)} lines")
        print(f"  pd_log.txt: {len(lines2)} lines")


if __name__ == "__main__":
    main()
