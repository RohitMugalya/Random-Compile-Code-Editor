import subprocess
import os
import tempfile

def evaluate_code(code, language, question):
    """
    Evaluate the submitted code against the test cases for the given question.

    Args:
        code (str): The code submitted by the user.
        language (str): The programming language (e.g., 'python', 'c', 'cpp', 'java').
        question (Question): The question object containing test cases.

    Returns:
        tuple: A tuple containing the result message and the number of test cases passed.
    """
    # Create a temporary directory to store the code and output files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write the code to a file
        code_file = os.path.join(temp_dir, f'solution.{language}')
        with open(code_file, 'w') as f:
            f.write(code)

        # Compile and run the code based on the language
        if language == 'python':
            return run_python_code(code_file, question)
        elif language == 'c':
            return run_c_code(code_file, temp_dir, question)
        elif language == 'cpp':
            return run_cpp_code(code_file, temp_dir, question)
        elif language == 'java':
            return run_java_code(code_file, temp_dir, question)
        else:
            return "Unsupported language", 0

def run_python_code(code_file, question):
    """
    Run Python code and evaluate it against test cases.

    Args:
        code_file (str): Path to the Python code file.
        question (Question): The question object containing test cases.

    Returns:
        tuple: A tuple containing the result message and the number of test cases passed.
    """
    passed_test_cases = 0
    for test_case in question.test_cases:
        try:
            # Run the code with the test case input
            process = subprocess.run(
                ['python3', code_file],
                input=test_case.input.encode(),
                capture_output=True,
                timeout=5  # Timeout after 5 seconds
            )
            # Compare the output with the expected output
            output = process.stdout.decode().strip()
            if output == test_case.output.strip():
                passed_test_cases += 1
        except subprocess.TimeoutExpired:
            return "Time Limit Exceeded", passed_test_cases
        except Exception as e:
            return f"Runtime Error: {str(e)}", passed_test_cases

    return "Success", passed_test_cases

def run_c_code(code_file, temp_dir, question):
    """
    Compile and run C code and evaluate it against test cases.

    Args:
        code_file (str): Path to the C code file.
        temp_dir (str): Path to the temporary directory.
        question (Question): The question object containing test cases.

    Returns:
        tuple: A tuple containing the result message and the number of test cases passed.
    """
    # Compile the C code
    executable = os.path.join(temp_dir, 'solution')
    compile_process = subprocess.run(
        ['gcc', code_file, '-o', executable],
        capture_output=True
    )
    if compile_process.returncode != 0:
        return "Compilation Error", 0

    # Run the compiled code against test cases
    passed_test_cases = 0
    for test_case in question.test_cases:
        try:
            process = subprocess.run(
                [executable],
                input=test_case.input.encode(),
                capture_output=True,
                timeout=5  # Timeout after 5 seconds
            )
            output = process.stdout.decode().strip()
            if output == test_case.output.strip():
                passed_test_cases += 1
        except subprocess.TimeoutExpired:
            return "Time Limit Exceeded", passed_test_cases
        except Exception as e:
            return f"Runtime Error: {str(e)}", passed_test_cases

    return "Success", passed_test_cases

def run_cpp_code(code_file, temp_dir, question):
    """
    Compile and run C++ code and evaluate it against test cases.

    Args:
        code_file (str): Path to the C++ code file.
        temp_dir (str): Path to the temporary directory.
        question (Question): The question object containing test cases.

    Returns:
        tuple: A tuple containing the result message and the number of test cases passed.
    """
    # Compile the C++ code
    executable = os.path.join(temp_dir, 'solution')
    compile_process = subprocess.run(
        ['g++', code_file, '-o', executable],
        capture_output=True
    )
    if compile_process.returncode != 0:
        return "Compilation Error", 0

    # Run the compiled code against test cases
    passed_test_cases = 0
    for test_case in question.test_cases:
        try:
            process = subprocess.run(
                [executable],
                input=test_case.input.encode(),
                capture_output=True,
                timeout=5  # Timeout after 5 seconds
            )
            output = process.stdout.decode().strip()
            if output == test_case.output.strip():
                passed_test_cases += 1
        except subprocess.TimeoutExpired:
            return "Time Limit Exceeded", passed_test_cases
        except Exception as e:
            return f"Runtime Error: {str(e)}", passed_test_cases

    return "Success", passed_test_cases

def run_java_code(code_file, temp_dir, question):
    """
    Compile and run Java code and evaluate it against test cases.

    Args:
        code_file (str): Path to the Java code file.
        temp_dir (str): Path to the temporary directory.
        question (Question): The question object containing test cases.

    Returns:
        tuple: A tuple containing the result message and the number of test cases passed.
    """
    # Compile the Java code
    compile_process = subprocess.run(
        ['javac', code_file],
        capture_output=True
    )
    if compile_process.returncode != 0:
        return "Compilation Error", 0

    # Run the compiled code against test cases
    passed_test_cases = 0
    for test_case in question.test_cases:
        try:
            process = subprocess.run(
                ['java', '-cp', temp_dir, 'Solution'],
                input=test_case.input.encode(),
                capture_output=True,
                timeout=5  # Timeout after 5 seconds
            )
            output = process.stdout.decode().strip()
            if output == test_case.output.strip():
                passed_test_cases += 1
        except subprocess.TimeoutExpired:
            return "Time Limit Exceeded", passed_test_cases
        except Exception as e:
            return f"Runtime Error: {str(e)}", passed_test_cases

    return "Success", passed_test_cases