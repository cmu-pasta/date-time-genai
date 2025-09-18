"""
Configuration file for DateTime GenAI Testing Framework.

This file contains all configurable parameters used across the datetime testing
framework for generating AI-powered datetime computations and running differential tests.
"""

import os
from enum import Enum

# =============================================================================
# ENUMS for configuration (placed here to avoid circular imports)
# =============================================================================


class Languages(Enum):
    """Supported Languages"""

    Python = "python"


class PythonDatetimeLibraries(Enum):
    """Supported Libraries"""

    Datetime = "datetime"
    Pendulum = "pendulum"


# =============================================================================
# AI Model Parameters
# =============================================================================

# Temperature for LLM sampling (0.0 = deterministic, 1.0 = very random)
SAMPLING_TEMPERATURE = 1.0

# Maximum number of tokens for LLM responses
MAX_TOKENS = 32896

# Number of interesting datetime computation ideas to generate
IDEAS = 10

# Maximum number of retries for LLM sampling
MAX_RETRIES = 3

# =============================================================================
# File Paths and Directory Structure
# =============================================================================

# Base directory for all output files
OUTPUT_DIR_PATH = "./results/"

# Timestamped output directory (formatted with ai_model at runtime)
OUTPUT_DIR = "./results/run_{ai_model}/"

# Subdirectories for generated code sets A and B (for differential testing)
OUTPUT_DIR_DT_A = "raw_results/DT_A/"
OUTPUT_DIR_DT_B = "raw_results/DT_B/"
OUTPUT_DIR_PENDULUM = "raw_results/PENDULUM/"


# Path to ideas file for caching generated ideas
IDEAS_PATH = "results/ideas/ideas.txt"

# Template for computation file naming (formatted with ai_model and index)
COMPUTATION_PATH = "computation_{model}_{i}.txt"

# Path to demonstration file used for few-shot prompting
DT_GENERATION_DEMONSTRATION = "./sample_llm/demonstrations/dt_generate_computation.txt"
PENDULUM_GENERATION_DEMONSTRATION = (
    "./sample_llm/demonstrations/pendulum_generate_computation.txt"
)

# =============================================================================
# Testing Framework Parameters
# =============================================================================

# Programming language for generated code
LANGUAGE = Languages.Python.value

# File extension for generated test files
EXTENSION = ".py"

# Directory name for differential test files
DT_VS_DT_DIFF_TESTS_DIR = "dt_vs_dt_diff_tests/"
DT_VS_PENDULUM_DIFF_TESTS_DIR = "dt_vs_pendulum_diff_tests/"

# Maximum number of test examples to generate per test case
MAX_EXAMPLES = 10000

# Timeout duration (in seconds) for test execution
TIMEOUT_DURATION = 60

# Random seed for reproducible test generation
SEED = 27

# =============================================================================
# Logging Configuration
# =============================================================================

# Logs directory
LOGS_DIR = "./results/run_{ai_model}/.logs/"

# Directory names for differential test logs (to be joined with LOGS_DIR dynamically)
DT_VS_DT_DIFF_TEST_LOGS_DIRNAME = "dt_vs_dt_diff_test_logs"
DT_VS_PENDULUM_DIFF_TEST_LOGS_DIRNAME = "dt_vs_pendulum_diff_test_logs"

# =============================================================================
# Test Analysis Parameters
# =============================================================================

# Threshold percentage for considering a test as differentiating
# (tests with <= THRESHOLD% differing lines are flagged for attention)
THRESHOLD = 101


# =============================================================================
# Analysis Parameters
# =============================================================================

# Directory for analysis results
ANALYSIS_OUTPUT_DIR = "./analysis/"

# Directory containing demonstration files for analysis prompts
DEMO_DIR = "./analyze/demonstration/"
