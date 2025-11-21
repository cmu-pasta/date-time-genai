import argparse
import os
from datetime import datetime

from dotenv import load_dotenv

import config
from analyze.plot_diff_test_results import (
    plot_models_divergence,
    plot_models_reliability,
)
from analyze.print_diff_test_results import print_models_statistics
from genai.models import Model, ModelType
from genai.utils import sanitize_model_name_for_path
from manual_analysis.plot_merged_categories import plot_merged_categories
from sample_llm.sample_code import sample_dt_vs_dt_code_sets, sample_pendulum_code_sets
from sample_llm.sample_ideas import sample_ideas
from testing_framework.diff_test_runner import (
    init,
    run_diff_tests_dt_vs_dt,
    run_diff_tests_dt_vs_pendulum,
)
from testing_framework.dt_vs_dt_diff_test_creator import create_dt_vs_dt_diff_tests
from testing_framework.dt_vs_pendulum_diff_test_creator import (
    create_dt_vs_pendulum_diff_tests,
)


def environment_variables_set() -> bool:
    """Check if required API keys are set in environment variables.

    LiteLLM automatically detects and uses the appropriate API keys:
    - OPENAI_API_KEY for OpenAI models
    - ANTHROPIC_API_KEY for Anthropic models
    - GEMINI_API_KEY or GOOGLE_API_KEY for Google models
    """
    missing_keys = []

    if "OPENAI_API_KEY" not in os.environ:
        missing_keys.append("OPENAI_API_KEY")

    elif "ANTHROPIC_API_KEY" not in os.environ:
        missing_keys.append("ANTHROPIC_API_KEY")

    elif "GEMINI_API_KEY" not in os.environ and "GOOGLE_API_KEY" not in os.environ:
        missing_keys.append("GEMINI_API_KEY or GOOGLE_API_KEY")

    else:
        print("Missing environment variables:")
        for key in missing_keys:
            print(f"  - {key}")
        print("\nNote: Only set the API keys for the models you plan to use.")
        return False

    return True


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="DateTime GenAI Testing Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py --model openai --ideas                        # Generate ideas only
  python run.py --model gemini --dt-code                      # Generate datetime library code snippets only
  python run.py --model claude --pd-code                      # Generate pendulum library code snippets only
  python run.py --model openai --create-tests                 # Create diff tests only
  python run.py --model openai --run-tests                    # Run diff tests only
  python run.py --model openai --analyze                      # Analyze results only
  python run.py --model openai --ideas --dt-code              # Generate ideas and datetime code
  python run.py --model gemini --dt-code --pd-code            # Generate all code snippets
  python run.py --model claude --create-tests --run-tests     # Create and run tests
  python run.py --model openai --all                          # Run complete pipeline
        """,
    )

    parser.add_argument(
        "--ideas",
        action="store_true",
        help="Generate ideas for datetime computations",
    )

    parser.add_argument(
        "--dt-code",
        action="store_true",
        help="Generate datetime library code snippets based on ideas",
    )

    parser.add_argument(
        "--pd-code",
        action="store_true",
        help="Generate pendulum library code snippets based on ideas",
    )

    parser.add_argument(
        "--create-tests",
        action="store_true",
        help="Create diff tests from generated code",
    )

    parser.add_argument(
        "--run-tests",
        action="store_true",
        help="Run the diff tests",
    )

    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analyze test results and generate summary report",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Run complete pipeline (all steps)",
    )

    parser.add_argument(
        "--model",
        choices=["openai", "gemini", "claude"],
        required=True,
        help="AI model to use for generation (required)",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    load_dotenv()

    # Check if any arguments are provided, if not show help
    if not any(
        [
            args.ideas,
            args.dt_code,
            args.pd_code,
            args.create_tests,
            args.run_tests,
            args.analyze,
            args.all,
        ]
    ):
        print("Error: No operation specified. Use --help to see available options.")
        return

    if not environment_variables_set():
        return

    # Sample outputs for Python
    programming_lang = config.Languages.Python.value

    # Map user input to ModelType enum
    model_mapping = {
        "openai": ModelType.OPENAI,
        "gemini": ModelType.GEMINI,
        "claude": ModelType.CLAUDE,
    }
    ai_model = Model(model_mapping[args.model])

    # Determine which operations to run
    run_ideas = args.ideas or args.all
    run_dt_code = args.dt_code or args.all
    run_pd_code = args.pd_code or args.all
    run_create_tests = args.create_tests or args.all
    run_run_tests = args.run_tests or args.all
    run_analyze = args.analyze or args.all

    # Build operation list for display
    operations = []
    if run_ideas:
        operations.append("ideas")
    if run_dt_code:
        operations.append("dt-code")
    if run_pd_code:
        operations.append("pd-code")
    if run_create_tests:
        operations.append("create-tests")
    if run_run_tests:
        operations.append("run-tests")
    if run_analyze:
        operations.append("analyze")

    print(
        f"\n#####\nStarting experiment run for {programming_lang}\nOperations: {', '.join(operations)}\n#####\n"
    )

    config.OUTPUT_DIR = config.OUTPUT_DIR.format(
        ai_model=sanitize_model_name_for_path(ai_model.model_name)
    )
    config.LOGS_DIR = config.LOGS_DIR.format(
        ai_model=sanitize_model_name_for_path(ai_model.model_name)
    )

    ideas_file = None

    # Generate ideas
    if run_ideas:
        print("💡 Generating ideas...")
        ideas_file = sample_ideas(ai_model)
        print("✅ Ideas generation completed!\n")

    # Generate datetime code snippets
    if run_dt_code:
        print("🚀 Generating datetime library code snippets...")
        if ideas_file is None:
            # If we're only running code generation without ideas,
            # we need to find the existing ideas file from config
            ideas_file = config.IDEAS_PATH
            if not os.path.exists(ideas_file):
                print(f"Error: Ideas file not found at {ideas_file}")
                print(
                    "Please run with --ideas first to generate ideas, or run --all for the complete pipeline."
                )
                return

        sample_dt_vs_dt_code_sets(
            ai_model,
            programming_lang,
            ideas_file,
        )
        print("✅ Datetime code generation completed!\n")

    # Generate pendulum library code snippets
    if run_pd_code:
        print("🚀 Generating pendulum library code snippets...")
        if ideas_file is None:
            # If we're only running code generation without ideas,
            # we need to find the existing ideas file from config
            ideas_file = config.IDEAS_PATH
            if not os.path.exists(ideas_file):
                print(f"Error: Ideas file not found at {ideas_file}")
                print(
                    "Please run with --ideas first to generate ideas, or run --all for the complete pipeline."
                )
                return

        sample_pendulum_code_sets(
            ai_model,
            programming_lang,
            ideas_file,
        )

        print("✅ Pendulum code generation completed!\n")

    # Create diff tests
    if run_create_tests:
        print("🧪 Creating diff tests...")
        create_dt_vs_dt_diff_tests(config.LANGUAGE, config.EXTENSION, config.OUTPUT_DIR)
        create_dt_vs_pendulum_diff_tests(
            config.LANGUAGE, config.EXTENSION, config.OUTPUT_DIR
        )
        print("✅ Diff tests creation completed!\n")

    # Run diff tests
    if run_run_tests:
        print("🏃 Running diff tests...")
        # Initialize logs directory (clean up old logs and create fresh directory)
        init()
        run_diff_tests_dt_vs_dt(config.OUTPUT_DIR)
        run_diff_tests_dt_vs_pendulum(config.OUTPUT_DIR)
        print("✅ Diff tests execution completed!\n")

    # Analyze results
    if run_analyze:
        print("📊 Analyzing results...")
        try:
            print_models_statistics()
            plot_models_reliability()
            plot_models_divergence()
            plot_merged_categories()
        except Exception as e:
            print(f"Error during results analysis: {e}")
        print("✅ Results analysis completed!")

    print(f"\n🎉 All requested operations completed successfully!")


if __name__ == "__main__":
    main()
