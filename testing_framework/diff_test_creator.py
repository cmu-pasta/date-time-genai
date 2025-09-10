import os
import re
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

from . import utils
from .templates.dt_vs_dt import DATETIME_DIFF_TEMPLATE
from .utils import Computation, generator_mapping, type_mapping


class DiffTestCreator:
    def __init__(self, language, extension):
        self.language = language
        self.extension = extension

    def extract_computation(self, solution_src):
        with open(solution_src, "r") as file:
            solution_code = file.read()

        match = re.search(
            rf"```{self.language.lower()}\n(.*?)\n```", solution_code, re.DOTALL
        )
        if match:
            code = match.group(1)
            lines = code.splitlines()

            imports = []
            main_code = []
            for line in lines:
                if line.startswith("import ") or line.startswith("from "):
                    imports.append(line)
                else:
                    main_code.append(line)

            imports = "\n".join(imports)
            solution_code = "\n".join(main_code)

        else:
            raise ValueError("No code block found in the solution.")

        # Step 1: Extract the function signature from the comment
        # signature_pattern = r"# Entry point:\s*(\w+)\((.*?)\)\s*->\s*(\w+)"
        signature_pattern = r"# Entry point:\s*(\w+)\((.*?)\)\s*->\s*([^\s]+)"
        match = re.search(signature_pattern, solution_code)

        if not match:
            raise ValueError("Entry point signature not found.")

        entry_point_name = match.group(1).strip()
        args = match.group(2).strip()
        return_type = match.group(3).strip()

        # Step 2: Process argument types
        argument_names = []
        argument_types = []
        if args:  # Check if there are any arguments
            arg_list = args.split(",")
            for arg in arg_list:
                arg_name = arg.strip().split(":")[0].strip()
                arg_type = arg.strip().split(":")[1].strip()
                try:
                    argument_names.append(arg_name)
                    argument_types.append(type_mapping[arg_type])
                except KeyError:
                    # print(solution_src, arg_type)
                    raise ValueError(f"Invalid argument type signature: {arg_type}.")

        # Step 3: Process return type
        try:
            return_type_signature = type_mapping[return_type]
        except KeyError:
            # print(solution_src, return_type)
            raise ValueError(f"Invalid return type signature: {return_type}.")

        # Create an EntryPoint object and return it
        arguments_count = len(argument_types)
        return Computation(
            entry_point_name,
            arguments_count,
            argument_names,
            argument_types,
            return_type_signature,
            solution_code,
            imports=imports,
        )

    def create_diff_test(self, computation: Computation, kwargs=None):
        generators = []
        for arg_type in computation.argument_types:
            generators.append(generator_mapping[arg_type])
            # Should not error here since we are checking the type in the extract_computation method
        generators = ", ".join(generators)

        args = [i for i in computation.argument_names]
        args = ", ".join(args)

        test = DATETIME_DIFF_TEMPLATE.format(
            function_name=computation.entry_point_name,
            function_source=computation.imports + computation.code,
            generators=generators,
            args=args,
            max_examples=config.MAX_EXAMPLES,
            file_name=kwargs[0],
            test_a_or_b=kwargs[1],
            DIFF_TEST_LOGS_DIR=config.DIFF_TEST_LOGS_DIR,
            seed=config.SEED,
        )

        return test

    def process_solution(self, code_set_a: str, code_set_b: str, working_dir: str):
        print("\n\n#####\nCreating Diff Tests\n#####\n")
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)

        for sampled_computation in os.listdir(code_set_a):
            if os.path.isfile(os.path.join(code_set_b, sampled_computation)):
                try:
                    # remove "." from file names to avoid issues with pytest
                    file_name = sampled_computation.replace(".", "")

                    postprocessed_computation_a = self.extract_computation(
                        os.path.join(code_set_a, sampled_computation)
                    )

                    test_a = self.create_diff_test(
                        postprocessed_computation_a,
                        kwargs=[file_name, "a"],
                    )

                    postprocessed_computation_b = self.extract_computation(
                        os.path.join(code_set_b, sampled_computation)
                    )
                    test_b = self.create_diff_test(
                        postprocessed_computation_b,
                        kwargs=[file_name, "b"],
                    )

                    dst_a = os.path.join(
                        working_dir,
                        f"{file_name}_a{self.extension}",
                    )
                    with open(dst_a, "w") as dst_file:
                        dst_file.write(test_a)

                    dst_b = os.path.join(
                        working_dir,
                        f"{file_name}_b{self.extension}",
                    )
                    with open(dst_b, "w") as dst_file:
                        dst_file.write(test_b)

                    print(f"  \\_Created diff test for {sampled_computation}")
                except Exception as e:
                    print(f"  \\_**Error processing {sampled_computation}: {e}**")

        # copy important files to the working directory
        print()
        script_dir = os.path.dirname(os.path.abspath(__file__))

        src = os.path.join(script_dir, "pytest.ini")
        dst = os.path.join(working_dir, "pytest.ini")
        if os.path.exists(src):
            if os.path.exists(dst):
                os.remove(dst)
            os.system(f"cp {src} {dst}")
            print(f"  \\_Copied pytest.ini from {src} to {dst}")
        else:
            print(f"  \\_**Warning: pytest.ini not found at {src}**")

        src = os.path.join(script_dir, "generators", "datetime_generators.py")
        dst = os.path.join(working_dir, "datetime_generators.py")
        if os.path.exists(src):
            if os.path.exists(dst):
                os.remove(dst)
            os.system(f"cp {src} {dst}")
            print(f"  \\_Copied datetime_generators.py from {src} to {dst}")
        else:
            print(f"  \\_**Warning: datetime_generators.py not found at {src}**")


def create_diff_tests(programming_lang, extension):
    most_recent_subdir = utils.find_most_recent_subdirectory(config.OUTPUT_DIR_PATH)
    if not most_recent_subdir:
        raise ValueError("No subdirectories found in the source files path.")

    diff_tests_dir = os.path.join(most_recent_subdir, config.DIFF_TESTS_DIR)

    print("\n" + "=" * 50)
    print(f"Creating diff tests for {programming_lang} with extension {extension}")
    print(f"Source path:      {most_recent_subdir}")
    print(f"Destination path: {diff_tests_dir}")
    print("=" * 50 + "\n")

    code_set_a = os.path.join(most_recent_subdir, config.OUTPUT_DIR_A)
    code_set_b = os.path.join(most_recent_subdir, config.OUTPUT_DIR_B)

    creator = DiffTestCreator(programming_lang, extension)
    creator.process_solution(code_set_a, code_set_b, diff_tests_dir)
