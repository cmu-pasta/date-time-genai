import os
import shutil
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

from .check_results import *
from .utils import *

pytest_command = ["pytest"]

# dt_vs_dt
dt_vs_dt_result_log = os.path.join(config.LOGS_DIR, "dt_vs_dt_result_log.txt")
dt_vs_dt_error_log = os.path.join(config.LOGS_DIR, "dt_vs_dt_error_log.txt")

# dt_vs_pd
# dt_vs_pd_result_log = os.path.join(config.LOGS_DIR, "dt_vs_pd_result_log.txt")
# dt_vs_pd_error_log = os.path.join(config.LOGS_DIR, "dt_vs_pd_error_log.txt")

# # dt_vs_arrow
# dt_vs_arrow_result_log = os.path.join(config.LOGS_DIR, "dt_vs_arrow_result_log.txt")
# dt_vs_arrow_error_log = os.path.join(config.LOGS_DIR, "dt_vs_arrow_error_log.txt")


def init():
    if os.path.exists(config.LOGS_DIR):
        shutil.rmtree(config.LOGS_DIR)

    if os.path.exists(".coverage"):
        os.remove(".coverage")

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
        with open(error_log, "a") as log_file:
            log_file.write(error_message)
        print(f"Error encountered in {file_name}. Check {error_log} for details.")
    except subprocess.TimeoutExpired as e:
        status = Status.TIMEOUT
        error_message = f"Error in file {file_name}:\n" f"Timeout\n" f"{'=' * 40}\n"
        with open(error_log, "a") as log_file:
            log_file.write(error_message)
        print(f"Error encountered in {file_name}. Check {error_log} for details.")

    return status


def run_diff_tests_dt_vs_dt():
    print("\n\n#####\nRunning datetime vs datetime differential tests...\n#####\n")

    most_recent_subdir = find_most_recent_subdirectory(config.OUTPUT_DIR_PATH)
    diff_tests_path = os.path.join(most_recent_subdir, config.DIFF_TESTS_DIR)

    for file_name in sorted(os.listdir(diff_tests_path)):

        if file_name.endswith("_a.py"):
            print(f"Running test {file_name}...")
            status = run_command(
                diff_tests_path, file_name, pytest_command, dt_vs_dt_error_log
            )

            if status != Status.PASSED:
                print(f"  \\_**Error: test {file_name} failed.**")
                if status == Status.ERROR:
                    status = DiffTestStatus.PROGRAM_ERROR
                elif status == Status.TIMEOUT:
                    status = DiffTestStatus.TIMEOUT

        elif file_name.endswith("_b.py"):
            print(f"Running test {file_name}...")
            status = run_command(
                diff_tests_path, file_name, pytest_command, dt_vs_dt_error_log
            )

            if status != Status.PASSED:
                print(f"  \\_**Error: test {file_name} failed.**")
                if status == Status.ERROR:
                    status = DiffTestStatus.PROGRAM_ERROR
                elif status == Status.TIMEOUT:
                    status = DiffTestStatus.TIMEOUT

    # Compare the results of test_a and test_b
    print("\nComparing the results...")
    for file_name in sorted(os.listdir(diff_tests_path)):
        if file_name.endswith("_a.py"):
            file_name = file_name.split(".")[0][:-2]

            test_log_file_a = os.path.join(
                config.DIFF_TEST_LOGS_DIR, f"log_{file_name}_a.txt"
            )
            test_log_file_b = os.path.join(
                config.DIFF_TEST_LOGS_DIR, f"log_{file_name}_b.txt"
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


# def run_diff_tests_dt_vs_pd(run_path, directory):
#     if not os.path.exists(os.path.join(sanity_check_result_log)):
#         run_sanity_checks(os.path.join(run_path, "sanity_checks"))

#     print("\n\n#####\nRunning datetime vs pendulum differential tests...\n#####\n")

#     status_results = ""
#     with open(sanity_check_result_log, "r") as log_file:
#         status_results = log_file.read()
#         print("\nStatus results:\n", status_results)

#     for file_name in sorted(os.listdir(directory)):
#         print()
#         # Check if the test is valid
#         cmp_str = f"{file_name.split(".")[0][:-3]}.py: {SanityCheckStatus.PASSED}"
#         if cmp_str not in status_results:
#             print(
#                 f"**Error: {cmp_str} not found for {file_name}. Skipping this test...**"
#             )
#             continue

#         if file_name.endswith("_dt.py"):
#             print(f"Running datetime test {file_name}...")
#             status = run_command(
#                 directory, file_name, pytest_command, dt_vs_pd_error_log
#             )

#             if status != Status.PASSED:
#                 print(f"  \\_**Error: datetime test {file_name} failed.**")

#         elif file_name.endswith("_pd.py"):
#             print(f"Running pendulum test {file_name}...")
#             status = run_command(
#                 directory, file_name, pytest_command, dt_vs_pd_error_log
#             )

#             if status != Status.PASSED:
#                 print(f"  \\_**Error: pendulum test {file_name} failed.**")

#     # Compare the results of test_a and test_b
#     print("\nComparing the results...")
#     for file_name in sorted(os.listdir(directory)):
#         if file_name.endswith("_dt.py"):
#             print()
#             file_name = file_name.split(".")[0][:-3]

#             test_log_file_dt = os.path.join(
#                 DIFF_TEST_LOGS_DIR_DT_VS_PD, f"log_{file_name}_dt.txt"
#             )
#             test_log_file_pd = os.path.join(
#                 DIFF_TEST_LOGS_DIR_DT_VS_PD, f"log_{file_name}_pd.txt"
#             )

#             if os.path.exists(test_log_file_dt) and os.path.exists(test_log_file_pd):
#                 status, differing_percentage = compare_diff_test_results(
#                     test_log_file_dt, test_log_file_pd, file_name
#                 )
#                 with open(dt_vs_pd_result_log, "a") as log_file:
#                     log_file.write(f"{file_name}: {status} ({differing_percentage}%)\n")
#             else:
#                 print(f"  \\_Skipping {file_name}.")


# def run_diff_tests_dt_vs_arrow(run_path, directory):
#     if not os.path.exists(os.path.join(sanity_check_result_log)):
#         run_sanity_checks(os.path.join(run_path, "sanity_checks"))

#     print("\n\n#####\nRunning datetime vs arrow differential tests...\n#####\n")

#     status_results = ""
#     with open(sanity_check_result_log, "r") as log_file:
#         status_results = log_file.read()
#         print("\nStatus results:\n", status_results)

#     for file_name in sorted(os.listdir(directory)):
#         print()
#         # Check if the test is valid
#         cmp_str_dt = f"{file_name.split(".")[0][:-3]}.py: {SanityCheckStatus.PASSED}"
#         cmp_str_arrow = f"{file_name.split(".")[0][:-6]}.py: {SanityCheckStatus.PASSED}"
#         if cmp_str_dt not in status_results and cmp_str_arrow not in status_results:
#             print(
#                 f"**Error: {cmp_str_dt} not found for {file_name}. Skipping this test...**"
#             )
#             continue

#         if file_name.endswith("_dt.py"):
#             print(f"Running datetime test {file_name}...")
#             status = run_command(
#                 directory, file_name, pytest_command, dt_vs_arrow_error_log
#             )

#             if status != Status.PASSED:
#                 print(f"  \\_**Error: datetime test {file_name} failed.**")

#         elif file_name.endswith("_arrow.py"):
#             print(f"Running arrow test {file_name}...")
#             status = run_command(
#                 directory, file_name, pytest_command, dt_vs_arrow_error_log
#             )

#             if status != Status.PASSED:
#                 print(f"  \\_**Error: arrow test {file_name} failed.**")

#     # Compare the results of test_a and test_b
#     print("\nComparing the results...")
#     for file_name in sorted(os.listdir(directory)):
#         if file_name.endswith("_dt.py"):
#             print()
#             file_name = file_name.split(".")[0][:-3]

#             test_log_file_dt = os.path.join(
#                 DIFF_TEST_LOGS_DIR_DT_VS_ARROW, f"log_{file_name}_dt.txt"
#             )
#             test_log_file_arrow = os.path.join(
#                 DIFF_TEST_LOGS_DIR_DT_VS_ARROW, f"log_{file_name}_arrow.txt"
#             )

#             if os.path.exists(test_log_file_dt) and os.path.exists(test_log_file_arrow):
#                 status, differing_percentage = compare_diff_test_results(
#                     test_log_file_dt, test_log_file_arrow, file_name
#                 )
#                 with open(dt_vs_arrow_result_log, "a") as log_file:
#                     log_file.write(f"{file_name}: {status} ({differing_percentage}%)\n")
#             else:
#                 print(f"  \\_Skipping {file_name}.")
