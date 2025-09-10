import argparse
from datetime import datetime

from dotenv import load_dotenv

import config
from analyze.log_parser import generate_summary_report, parse_log_file
from genai.models import OpenAIModel
from genai.sample_code import sample_interesting_computations
from genai.sample_ideas import sample_ideas
from genai.utils import Languages, PythonDatetimeLibraries, environment_variables_set
from testing_framework.diff_test_creator import create_diff_tests
from testing_framework.diff_test_runner import run_diff_tests_dt_vs_dt


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="DateTime GenAI Testing Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py gen          # Generate ideas and code snippets
  python run.py test         # Run diff tests only
  python run.py all          # Run complete pipeline (generate + test)
        """,
    )

    parser.add_argument(
        "mode",
        choices=["gen", "test", "all"],
        help="Operation mode: 'gen' to generate code, 'test' to run tests, 'all' for complete pipeline",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    load_dotenv()

    if not environment_variables_set():
        return

    # Sample outputs for Python
    programming_lang = Languages.Python.value
    model_gpt_41 = OpenAIModel("gpt-4.1")

    print(
        f"\n#####\nStarting experiment run for {programming_lang} (mode: {args.mode})\n#####\n"
    )

    config.OUTPUT_DIR = config.OUTPUT_DIR.format(
        timestamp=int(datetime.now().timestamp())
    )

    # Execute based on mode
    if args.mode in ["gen", "all"]:
        print("🚀 Generating ideas and code snippets...")

        # Generate ideas
        ideas_file = sample_ideas(model_gpt_41)

        # Generate code snippets
        sample_interesting_computations(
            model_gpt_41,
            programming_lang,
            PythonDatetimeLibraries.Datetime,
            PythonDatetimeLibraries.Datetime,
            ideas_file,
        )

        print("✅ Generation phase completed!")

    if args.mode in ["test", "all"]:
        print("🧪 Creating and running diff tests...")

        # Create diff tests
        create_diff_tests(config.LANGUAGE, config.EXTENSION)

        # Run diff tests
        run_diff_tests_dt_vs_dt()

        print("\n✅ Testing phase completed!")

    print(f"\n🎉 All operations for mode '{args.mode}' completed successfully!")

    # Analyze results at the end
    print("\n📊 Analyzing results...")
    try:
        # Generate summary report
        results = parse_log_file()
        report_file = f"{config.ANALYSIS_OUTPUT_DIR}/summary_report.md"
        generate_summary_report(results, report_file)
        print(f"Summary report saved to {report_file}")

    except FileNotFoundError as e:
        print(f"Warning: Could not analyze results - {e}")
    except Exception as e:
        print(f"Error during results analysis: {e}")

    print("✅ Results analysis completed!")


if __name__ == "__main__":
    main()
