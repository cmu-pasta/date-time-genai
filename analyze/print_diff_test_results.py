#!/usr/bin/env python3
"""
Print Diff Test Results for DateTime GenAI Testing Framework

This module provides functions to analyze and print statistics from log files
for all available model runs. It extracts key statistics:
- Number of non-differentiating computations
- Number of differentiating computations
- Among differentiating, how many have percentage < 75%
- Remaining computations (differentiating with >= 75%)

The module automatically discovers all available model runs and processes both
dt_vs_dt and dt_vs_pendulum log files. It can be used both as a standalone script
and imported from run.py.
"""

import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, NamedTuple, Tuple

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class ComputationStats(NamedTuple):
    """Statistics for a single model run"""

    non_differentiating: int
    differentiating_total: int
    differentiating_under_75: int
    differentiating_75_and_above: int
    other_statuses: int  # program-error, timeout, input-error, etc.


# Regex pattern to extract status and percentage from log lines
PATTERN = re.compile(r":\s*([a-z0-9_-]+)\s*\(\s*([\d.]+)\s*%\s*\)", re.IGNORECASE)


def get_available_model_runs(log_filename: str) -> List[Tuple[str, str]]:
    """
    Automatically discover available model runs and return their log file paths and labels.

    Args:
        log_filename: Name of the log file to look for (e.g., "dt_vs_dt_result_log.txt")

    Returns:
        List of tuples (file_path, label) for each available model run
    """
    results_dir = Path(config.OUTPUT_DIR_PATH)
    model_runs = []

    if not results_dir.exists():
        print(f"Warning: Results directory {results_dir} does not exist.")
        return model_runs

    # Look for run_* directories
    for run_dir in results_dir.glob("run_*"):
        if run_dir.is_dir():
            # Extract model name from directory name
            model_name = run_dir.name.replace("run_", "")

            # Construct log file path
            original_logs_dir_template = "./results/run_{ai_model}/.logs/"
            logs_dir_path = original_logs_dir_template.format(ai_model=model_name)
            logs_dir = Path(logs_dir_path)
            log_file = logs_dir / log_filename

            if log_file.exists():
                # Create a human-readable label from the model name
                label = format_model_label(model_name)
                model_runs.append((str(log_file), label))

    return sorted(model_runs, key=lambda x: x[1])  # Sort by label


def format_model_label(model_name: str) -> str:
    """
    Convert model name to a human-readable label.

    Args:
        model_name: Raw model name from directory (e.g., 'gpt-5', 'claude-sonnet-4-20250514')

    Returns:
        Formatted label for display
    """
    # Handle common model name patterns
    if model_name.startswith("gpt"):
        return model_name.upper().replace("-", "-")
    elif model_name.startswith("claude"):
        return "Claude Sonnet 4"
    elif model_name.startswith("gemini"):
        return "Gemini 2.5 Flash"
    else:
        # Generic formatting: capitalize and replace hyphens with spaces
        return model_name.replace("-", " ").title()


def analyze_log_file(log_path: str) -> ComputationStats:
    """
    Analyze a single log file and extract statistics.

    Args:
        log_path: Path to the log file to analyze

    Returns:
        ComputationStats object with extracted statistics
    """
    non_differentiating = 0
    differentiating_total = 0
    differentiating_under_75 = 0
    differentiating_75_and_above = 0
    other_statuses = 0

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Extract status and percentage using regex
                match = PATTERN.search(line.lower())
                if not match:
                    continue

                status, pct_str = match.groups()
                status = status.lower().strip()

                try:
                    percentage = float(pct_str)
                except ValueError:
                    continue

                if status == "non-differentiating":
                    non_differentiating += 1
                elif status == "differentiating":
                    differentiating_total += 1
                    if percentage < 75.0:
                        differentiating_under_75 += 1
                    else:
                        differentiating_75_and_above += 1
                else:
                    # Other statuses like program-error, timeout, input-error
                    other_statuses += 1

    except FileNotFoundError:
        print(f"Warning: Log file not found: {log_path}")
    except Exception as e:
        print(f"Error reading log file {log_path}: {e}")

    return ComputationStats(
        non_differentiating=non_differentiating,
        differentiating_total=differentiating_total,
        differentiating_under_75=differentiating_under_75,
        differentiating_75_and_above=differentiating_75_and_above,
        other_statuses=other_statuses,
    )


def print_statistics_table(results: Dict[str, Dict[str, ComputationStats]]):
    """
    Print a formatted table of statistics for all models and test types.

    Args:
        results: Dictionary with structure {model_name: {test_type: ComputationStats}}
    """
    print("\n" + "=" * 120)
    print("LOG STATISTICS ANALYSIS - DateTime GenAI Testing Framework")
    print("=" * 120)

    # Print header
    header = f"{'Model':<20} {'Test Type':<15} {'Non-Diff':<10} {'Diff Total':<12} {'Diff <75%':<12} {'Diff ≥75%':<12} {'Other':<8} {'Total':<8}"
    print(header)
    print("-" * 120)

    # Print data for each model
    for model_name in sorted(results.keys()):
        model_data = results[model_name]
        first_row = True

        for test_type in sorted(model_data.keys()):
            stats = model_data[test_type]
            total = (
                stats.non_differentiating
                + stats.differentiating_total
                + stats.other_statuses
            )

            # Print model name only on first row
            model_display = model_name if first_row else ""
            first_row = False

            print(
                f"{model_display:<20} {test_type:<15} {stats.non_differentiating:<10} "
                f"{stats.differentiating_total:<12} {stats.differentiating_under_75:<12} "
                f"{stats.differentiating_75_and_above:<12} {stats.other_statuses:<8} {total:<8}"
            )

        if model_data:  # Add separator between models
            print("-" * 120)

    print("\nLEGEND:")
    print("  Non-Diff:     Computations with no behavioral differences")
    print("  Diff Total:   Total computations with behavioral differences")
    print("  Diff <75%:    Differentiating computations with < 75% differing inputs")
    print("  Diff ≥75%:    Differentiating computations with ≥ 75% differing inputs")
    print("  Other:        Program errors, timeouts, input errors, etc.")
    print("  Total:        Total computations processed")


def print_summary_statistics(results: Dict[str, Dict[str, ComputationStats]]):
    """
    Print summary statistics across all models and test types.

    Args:
        results: Dictionary with structure {model_name: {test_type: ComputationStats}}
    """
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)

    # Aggregate statistics by test type
    test_type_totals = defaultdict(lambda: ComputationStats(0, 0, 0, 0, 0))

    for model_data in results.values():
        for test_type, stats in model_data.items():
            current = test_type_totals[test_type]
            test_type_totals[test_type] = ComputationStats(
                non_differentiating=current.non_differentiating
                + stats.non_differentiating,
                differentiating_total=current.differentiating_total
                + stats.differentiating_total,
                differentiating_under_75=current.differentiating_under_75
                + stats.differentiating_under_75,
                differentiating_75_and_above=current.differentiating_75_and_above
                + stats.differentiating_75_and_above,
                other_statuses=current.other_statuses + stats.other_statuses,
            )

    for test_type, stats in sorted(test_type_totals.items()):
        total = (
            stats.non_differentiating
            + stats.differentiating_total
            + stats.other_statuses
        )
        print(f"\n{test_type.upper()} (across all models):")
        print(f"  Non-differentiating computations:     {stats.non_differentiating:4d}")
        print(
            f"  Differentiating computations (total): {stats.differentiating_total:4d}"
        )
        print(
            f"    - With < 75% differing inputs:      {stats.differentiating_under_75:4d}"
        )
        print(
            f"    - With ≥ 75% differing inputs:      {stats.differentiating_75_and_above:4d}"
        )
        print(f"  Other statuses:                       {stats.other_statuses:4d}")
        print(f"  Total computations:                   {total:4d}")

        if stats.differentiating_total > 0:
            under_75_pct = (
                stats.differentiating_under_75 / stats.differentiating_total
            ) * 100
            over_75_pct = (
                stats.differentiating_75_and_above / stats.differentiating_total
            ) * 100
            print(
                f"  Differentiating breakdown:            {under_75_pct:.1f}% < 75%, {over_75_pct:.1f}% ≥ 75%"
            )


def print_models_statistics():
    """
    Automatically discover and print statistics for all available model runs.
    Uses both dt_vs_dt_result_log.txt and dt_vs_pendulum_result_log.txt files.
    This function can be called from run.py as part of the analysis pipeline.
    """
    print("DateTime GenAI Testing Framework - Statistics Analysis")
    print("Discovering available model runs...")

    # Dictionary to store results: {model_name: {test_type: ComputationStats}}
    results = defaultdict(dict)

    # Analyze both dt_vs_dt and dt_vs_pendulum logs
    log_types = [
        ("dt_vs_dt_result_log.txt", "reliability"),
        ("dt_vs_pendulum_result_log.txt", "divergence"),
    ]

    for log_filename, test_type in log_types:
        model_runs = get_available_model_runs(log_filename)

        if not model_runs:
            print(f"No {test_type} logs found for {log_filename}")
            continue

        print(f"\nAnalyzing {test_type} logs ({log_filename}):")

        for log_path, model_label in model_runs:
            print(f"  Processing {model_label}...")
            stats = analyze_log_file(log_path)
            results[model_label][test_type] = stats

    if not results:
        print("\nNo log files found to analyze. Please check:")
        print(f"1. Results directory exists: {config.OUTPUT_DIR_PATH}")
        print("2. Model run directories exist (format: run_<model_name>)")
        print("3. Log files exist in: <run_dir>/.logs/")
        return

    # Print detailed results table
    print_statistics_table(results)

    # Print summary statistics
    print_summary_statistics(results)

    print(f"\nStatistics analysis complete. Processed {len(results)} model(s).\n\n")
