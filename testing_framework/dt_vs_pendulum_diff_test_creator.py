import os
import re
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

from . import utils
from .templates.dt_vs_dt import DATETIME_DIFF_TEMPLATE
from .templates.dt_vs_pd import DATETIME_DIFF_TEMPLATE_PENDULUM
from .utils import (
    Computation,
    generator_mapping,
    generator_mapping_pd,
    type_mapping,
    type_mapping_pd,
)


class DiffTestCreator_DT_vs_PD:
    def __init__(self, language, extension):
        self.language = language
        self.extension = extension

    def extract_computation_dt(self, solution_src):
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
                    raise ValueError(f"Invalid argument type signature: {arg_type}.")

        # Step 3: Process return type
        try:
            return_type_signature = type_mapping[return_type]
        except KeyError:
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

    def extract_computation_pd(self, solution_src):
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
        signature_pattern = r"# Entry point:\s*(\w+)\((.*?)\)\s*->\s*([^\s]+)"
        match = re.search(signature_pattern, solution_code)

        if not match:
            raise ValueError("Entry point signature not found.")

        entry_point_name = match.group(1)
        args = match.group(2).strip()
        return_type = match.group(3)

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
                    argument_types.append(type_mapping_pd[arg_type])
                except KeyError:
                    raise ValueError(f"Invalid argument type signature: {arg_type}.")

        # Step 3: Process return type
        try:
            return_type_signature = type_mapping_pd[return_type]
        except KeyError:
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

    def create_diff_test_dt(self, computation: Computation, kwargs=None):
        generators = []
        for arg_type in computation.argument_types:
            generators.append(generator_mapping[arg_type])
            # Should not error here since we are checking the type in the extract_computation method
        generators = ", ".join(generators)

        args = [i for i in computation.argument_names]
        args = ", ".join(args)

        test_dt = DATETIME_DIFF_TEMPLATE.format(
            function_name=computation.entry_point_name,
            function_source=computation.imports + computation.code,
            generators=generators,
            args=args,
            max_examples=config.MAX_EXAMPLES,
            file_name=kwargs[0],
            test_a_or_b=kwargs[1],
            DIFF_TEST_LOGS_DIR=os.path.join(
                config.LOGS_DIR, config.DT_VS_PENDULUM_DIFF_TEST_LOGS_DIRNAME
            ),
            seed=config.SEED,
        )

        return test_dt

    def create_diff_test_pd(self, computation: Computation, kwargs=None):
        generators = []
        for arg_type in computation.argument_types:
            generators.append(generator_mapping_pd[arg_type])
            # Should not error here since we are checking the type in the extract_computation method
        generators = ", ".join(generators)

        args = [i for i in computation.argument_names]
        args = ", ".join(args)

        test_pd = DATETIME_DIFF_TEMPLATE_PENDULUM.format(
            function_name=computation.entry_point_name,
            function_source=computation.imports + computation.code,
            generators=generators,
            args=args,
            max_examples=config.MAX_EXAMPLES,
            file_name=kwargs[0],
            DIFF_TEST_LOGS_DIR=os.path.join(
                config.LOGS_DIR, config.DT_VS_PENDULUM_DIFF_TEST_LOGS_DIRNAME
            ),
            seed=config.SEED,
        )

        return test_pd

    def process_solution(
        self, solution_src_dt: str, solution_src_pd: str, working_dir: str
    ):
        print("\n\n#####\nCreating Diff Tests\n#####\n")
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)

        for sampled_computation in os.listdir(solution_src_dt):
            if os.path.isfile(os.path.join(solution_src_pd, sampled_computation)):
                try:
                    # Extract file name without extension
                    file_name = os.path.splitext(sampled_computation)[0]

                    postprocessed_computation_dt = self.extract_computation_dt(
                        os.path.join(solution_src_dt, sampled_computation)
                    )

                    test_dt = self.create_diff_test_dt(
                        postprocessed_computation_dt,
                        kwargs=[file_name, "dt"],
                    )

                    postprocessed_computation_pd = self.extract_computation_pd(
                        os.path.join(solution_src_pd, sampled_computation)
                    )

                    test_pd = self.create_diff_test_pd(
                        postprocessed_computation_pd,
                        kwargs=[file_name],
                    )

                    dst_dt = os.path.join(
                        working_dir,
                        f"{file_name}_dt{self.extension}",
                    )
                    with open(dst_dt, "w") as dst_file:
                        dst_file.write(test_dt)

                    dst_pd = os.path.join(
                        working_dir,
                        f"{file_name}_pd{self.extension}",
                    )
                    with open(dst_pd, "w") as dst_file:
                        dst_file.write(test_pd)

                    print(f"  \\_Created diff test for {sampled_computation}")
                except Exception as e:
                    print(f"  \\_**Error processing {sampled_computation}: {e}**")

        # copy important files to the working directory
        print()
        script_dir = os.path.dirname(os.path.abspath(__file__))

        src = os.path.join(script_dir, "misc", "pytest.ini")
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

        src = os.path.join(script_dir, "generators", "pendulum_generators.py")
        dst = os.path.join(working_dir, "pendulum_generators.py")
        if os.path.exists(src):
            if os.path.exists(dst):
                os.remove(dst)
            os.system(f"cp {src} {dst}")
            print(f"  \\_Copied pendulum_generators.py from {src} to {dst}")
        else:
            print(f"  \\_**Warning: pendulum_generators.py not found at {src}**")


def create_dt_vs_pendulum_diff_tests(programming_lang, extension, path):
    if not os.path.exists(path):
        raise ValueError(f"The path {path} does not exist.")

    diff_tests_dir = os.path.join(path, config.DT_VS_PENDULUM_DIFF_TESTS_DIR)

    print("\n" + "=" * 50)
    print(f"Creating diff tests for {programming_lang} with extension {extension}")
    print(f"Source path:      {path}")
    print(f"Destination path: {diff_tests_dir}")
    print("=" * 50 + "\n")

    code_set_dt = os.path.join(path, config.OUTPUT_DIR_DT_A)  # datetime solutions
    code_set_pd = os.path.join(path, config.OUTPUT_DIR_PENDULUM)  # pendulum solutions

    creator = DiffTestCreator_DT_vs_PD(programming_lang, extension)
    creator.process_solution(code_set_dt, code_set_pd, diff_tests_dir)
