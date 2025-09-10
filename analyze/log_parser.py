import os
import re

# Add the parent directory to the path so we can import from config
from collections import Counter
from typing import Any, Dict, Optional


def parse_log_file(filepath) -> Dict[str, Any]:
    """Parse the log file and extract test results with statistics.

    Args:
        filepath: Path to the log file to parse

    Returns:
        Dictionary containing parsed results, statistics, and metadata

    Raises:
        FileNotFoundError: If the log file doesn't exist
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Log file not found: {filepath}")

    # Updated pattern to match log entries with percentage values
    pattern = r"computations_([a-zA-Z0-9-]+)_(\d+)_(\d+): DiffTestStatus\.(\w+)(?: \((\d+(?:\.\d+)?)%\))?"

    results = []
    computation_ids = set()

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            match = re.match(pattern, line)
            if match:
                model, comp_id, variant, status, percentage = match.groups()
                result_entry = {
                    "model": model,
                    "computation_id": comp_id + "_" + variant,
                    "status": status,
                    "percentage": percentage,
                }

                results.append(result_entry)
                computation_ids.add(int(comp_id))

    # Calculate statistics
    status_counts = Counter([r["status"] for r in results])

    return {
        "raw_results": results,
        "total_tests": len(results),
        "unique_computations": sorted(list(computation_ids)),
        "status_counts": dict(status_counts),
    }


def generate_summary_report(
    results: Dict[str, Any], output_file: Optional[str] = None
) -> str:
    """Generate a markdown summary report from parsed results.

    Args:
        results: Parsed results dictionary from parse_log_file
        output_file: Optional path to save the report to

    Returns:
        The generated report as a string
    """
    report = []
    report.append("# Differential Testing Results Summary")
    report.append(f"\nTotal tests: {results['total_tests']}")
    report.append(f"Number of computations: {len(results['unique_computations'])}")

    report.append("\n## Status Counts")
    for status, count in results["status_counts"].items():
        report.append(f"- {status}: {count} ({count/results['total_tests']*100:.1f}%)")

    report_text = "\n".join(report)

    if output_file:
        with open(output_file, "w") as f:
            f.write(report_text)

    return report_text
