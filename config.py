"""
Configuration file for DateTime GenAI Testing Framework.

This file contains all configurable parameters used across the datetime testing
framework for generating AI-powered datetime computations and running differential tests.
"""

import os

from genai.utils import Languages

# =============================================================================
# AI Model Parameters
# =============================================================================

# Temperature for LLM sampling (0.0 = deterministic, 1.0 = very random)
SAMPLING_TEMPERATURE = 0.5

# Maximum number of tokens for LLM responses
MAX_TOKENS = 32896

# Number of interesting datetime computation ideas to generate
IDEAS = 100

# =============================================================================
# File Paths and Directory Structure
# =============================================================================

# Base directory for all output files
OUTPUT_DIR_PATH = "./results/"

# Timestamped output directory (formatted with timestamp at runtime)
OUTPUT_DIR = "./results/run_{timestamp}/"

# Subdirectories for generated code sets A and B (for differential testing)
OUTPUT_DIR_A = "raw_results/A/"
OUTPUT_DIR_B = "raw_results/B/"

# Template for ideas file naming (formatted with model name)
IDEAS_PATH = "ideas_{model}.txt"

# Template for computation file naming (formatted with model name and index)
COMPUTATION_PATH = "computation_{model}_{i}.txt"

# Path to demonstration file used for few-shot prompting
GENERATION_DEMONSTRATION = "./genai/demonstrations/generate_computation.txt"

# =============================================================================
# Testing Framework Parameters
# =============================================================================

# Programming language for generated code
LANGUAGE = Languages.Python.value

# File extension for generated test files
EXTENSION = ".py"

# Directory name for differential test files
DIFF_TESTS_DIR = "diff_tests/"

# Maximum number of test examples to generate per test case
MAX_EXAMPLES = 10000

# Timeout duration (in seconds) for test execution
TIMEOUT_DURATION = 60

# Random seed for reproducible test generation
SEED = 27

# =============================================================================
# Logging Configuration
# =============================================================================

# Main logs directory
LOGS_DIR = ".logs"

# Directory for differential test logs
DIFF_TEST_LOGS_DIR = os.path.join(LOGS_DIR, "diff_test_logs")

# =============================================================================
# Test Analysis Parameters
# =============================================================================

# Threshold percentage for considering a test as differentiating
# (tests with <= THRESHOLD% differing lines are flagged for attention)
THRESHOLD = 99


# =============================================================================
# Analysis Parameters
# =============================================================================

# Directory for analysis results
ANALYSIS_OUTPUT_DIR = "./analysis/"

# Directory containing demonstration files for analysis prompts
DEMO_DIR = "./analyze/demonstration/"
