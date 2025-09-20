import os
import shutil
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

from .utils import *

pytest_command = ["pytest"]


def init():
    if os.path.exists(config.LOGS_DIR):
        shutil.rmtree(config.LOGS_DIR)

    os.makedirs(config.LOGS_DIR)


def run_command(directory, file_name, command, error_log) -> Status:
    status = Status.PASSED
    file_path = os.path.join(directory, file_name)
    print(f"Running command: {command}...")
    try:
        subprocess.run(
            command + [file_path],
            check=True,
            text=True,
            capture_output=True,
            timeout=config.TIMEOUT_DURATION,
        )
        print(f"{file_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        error_message = (
            f"Error in file {file_name}:\n"
            f"Return Code: {e.returncode}\n"
            f"Standard Output:\n{e.stdout}\n"
            f"Standard Error:\n{e.stderr}\n"
            f"{'=' * 50}\n"
        )
        status = Status.ERROR
        # Ensure the logs directory exists before writing
        os.makedirs(os.path.dirname(error_log), exist_ok=True)
        with open(error_log, "a") as log_file:
            log_file.write(error_message)
        print(f"Error encountered in {file_name}. Check {error_log} for details.")
    except subprocess.TimeoutExpired as e:
        status = Status.TIMEOUT
        error_message = f"Error in file {file_name}:\n" f"Timeout\n" f"{'=' * 40}\n"
        # Ensure the logs directory exists before writing
        os.makedirs(os.path.dirname(error_log), exist_ok=True)
        with open(error_log, "a") as log_file:
            log_file.write(error_message)
        print(f"Error encountered in {file_name}. Check {error_log} for details.")

    return status


def run_diff_tests_dt_vs_dt(path):
    if not os.path.exists(path):
        raise ValueError(f"The path {path} does not exist.")

    diff_tests_path = os.path.join(path, config.DT_VS_DT_DIFF_TESTS_DIR)

    if not os.path.exists(diff_tests_path):
        raise ValueError(f"The path {diff_tests_path} does not exist.")

    # Construct log paths dynamically to use properly formatted config.LOGS_DIR
    dt_vs_dt_result_log = os.path.join(config.LOGS_DIR, "dt_vs_dt_result_log.txt")
    dt_vs_dt_error_log = os.path.join(config.LOGS_DIR, "dt_vs_dt_error_log.txt")

    print("\n\n#####\nRunning datetime vs datetime differential tests...\n#####\n")

    for file_name in sorted(os.listdir(diff_tests_path)):

        if file_name.endswith("_a.py"):
            print(f"Running test {file_name}...")
            status = run_command(
                diff_tests_path, file_name, pytest_command, dt_vs_dt_error_log
            )

            if status != Status.PASSED:
                print(f"  \\_**Error: test {file_name} failed.**")

        elif file_name.endswith("_b.py"):
            print(f"Running test {file_name}...")
            status = run_command(
                diff_tests_path, file_name, pytest_command, dt_vs_dt_error_log
            )

            if status != Status.PASSED:
                print(f"  \\_**Error: test {file_name} failed.**")

    # Compare the results of test_a and test_b
    print("\nComparing the results...")
    for file_name in sorted(os.listdir(diff_tests_path)):
        if file_name.endswith("_a.py"):
            file_name = file_name.split(".")[0][:-2]

            dt_vs_dt_diff_test_logs_dir = os.path.join(
                config.LOGS_DIR, config.DT_VS_DT_DIFF_TEST_LOGS_DIRNAME
            )
            test_log_file_a = os.path.join(
                dt_vs_dt_diff_test_logs_dir, f"log_{file_name}_a.txt"
            )
            test_log_file_b = os.path.join(
                dt_vs_dt_diff_test_logs_dir, f"log_{file_name}_b.txt"
            )

            if os.path.exists(test_log_file_a) and os.path.exists(test_log_file_b):
                status, differing_percentage = compare_diff_test_results(
                    test_log_file_a, test_log_file_b, file_name
                )
                with open(dt_vs_dt_result_log, "a") as log_file:
                    log_file.write(
                        f"{file_name}: {status.value} ({differing_percentage}%)\n"
                    )
            else:
                print(f"  \\_Skipping {file_name}.")


def run_diff_tests_dt_vs_pendulum(path):
    if not os.path.exists(path):
        raise ValueError(f"The path {path} does not exist.")

    diff_tests_path = os.path.join(path, config.DT_VS_PENDULUM_DIFF_TESTS_DIR)

    if not os.path.exists(diff_tests_path):
        raise ValueError(f"The path {diff_tests_path} does not exist.")

    # Construct log paths dynamically to use properly formatted config.LOGS_DIR
    dt_vs_pendulum_result_log = os.path.join(
        config.LOGS_DIR, "dt_vs_pendulum_result_log.txt"
    )
    dt_vs_pendulum_error_log = os.path.join(
        config.LOGS_DIR, "dt_vs_pendulum_error_log.txt"
    )

    print("\n\n#####\nRunning datetime vs pendulum differential tests...\n#####\n")

    for file_name in sorted(os.listdir(diff_tests_path)):
        if file_name.endswith("_dt.py"):
            print(f"Running datetime test {file_name}...")
            status = run_command(
                diff_tests_path, file_name, pytest_command, dt_vs_pendulum_error_log
            )

            if status != Status.PASSED:
                print(f"  \\_**Error: datetime test {file_name} failed.**")

        elif file_name.endswith("_pd.py"):
            print(f"Running pendulum test {file_name}...")
            status = run_command(
                diff_tests_path, file_name, pytest_command, dt_vs_pendulum_error_log
            )

            if status != Status.PASSED:
                print(f"  \\_**Error: pendulum test {file_name} failed.**")

    # Compare the results of test_a and test_b
    print("\nComparing the results...")
    for file_name in sorted(os.listdir(diff_tests_path)):
        if file_name.endswith("_dt.py"):
            file_name = file_name.split(".")[0][:-3]

            dt_vs_pendulum_diff_test_logs_dir = os.path.join(
                config.LOGS_DIR, config.DT_VS_PENDULUM_DIFF_TEST_LOGS_DIRNAME
            )
            test_log_file_dt = os.path.join(
                dt_vs_pendulum_diff_test_logs_dir, f"log_{file_name}_dt.txt"
            )
            test_log_file_pd = os.path.join(
                dt_vs_pendulum_diff_test_logs_dir,
                f"log_{file_name}_pendulum.txt",
            )

            if os.path.exists(test_log_file_dt) and os.path.exists(test_log_file_pd):
                status, differing_percentage = compare_diff_test_results(
                    test_log_file_dt, test_log_file_pd, file_name
                )
                with open(dt_vs_pendulum_result_log, "a") as log_file:
                    log_file.write(
                        f"{file_name}: {status.value} ({differing_percentage}%)\n"
                    )
            else:
                print(f"  \\_Skipping {file_name}.")
