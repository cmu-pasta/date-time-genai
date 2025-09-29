# Example: Differential Testing Demonstration

This folder contains an example code snippet to demonstrate how our differential testing works and everything that goes into making it work (test harnesses, generators, and logging).

## Overview

The example demonstrates differential testing between Python's standard `datetime` library and the `pendulum` library by implementing the same function (`calculate_days_difference`) in both libraries and comparing their outputs.

## Files

- `dt_code.py` - Implementation using Python's standard datetime library
- `pd_code.py` - Implementation using the Pendulum library  
- `datetime_generators.py` - Hypothesis generators for datetime objects
- `pendulum_generators.py` - Hypothesis generators for pendulum objects
- `compare_logs.py` - Script to compare the generated log files and analyze differences
- `pytest.ini` - Pytest configuration file

## How to Run

### Step 1: Run the code snippets by calling pytest

```bash
pytest dt_code.py
pytest pd_code.py
```

These commands will:
- Execute the test functions with 10,000 generated test cases each
- Generate `dt_log.txt` and `pd_log.txt` containing the results from each library
- Use the same random seed (1234) to ensure reproducible test cases

### Step 2: Run the compare logs script to get the results

```bash
python compare_logs.py
```

The comparison script will display:
- Number of lines in each log file
- Total matching and non-matching lines
- Percentage breakdown of results
- Examples of the first 5 differences (if any exist)

## What This Demonstrates

This example showcases:
1. **Test Harnesses**: How to structure tests for differential testing
2. **Generators**: Using Hypothesis to generate comprehensive test data
3. **Logging**: Capturing and formatting results for comparison
4. **Analysis**: Automated comparison and reporting of differences

The differential testing approach helps identify discrepancies between different AI-generated datetime code snippets that manifest as behavioral differences that might not be caught by developers.
