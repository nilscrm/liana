import subprocess
import os

num_tests = 0
num_passed = 0

for file in os.listdir("tests/linear_programs"):
    print(f"Running test {file}: ", end="")
    num_tests += 1
    try:
        result = subprocess.run(
            ["vine", "run", "--no-stats", f"tests/linear_programs/{file}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            file_stem = file.split(".")[0]
            with open(f"tests/outputs/{file_stem}.out", "r") as f:
                expected_output = f.read()
                if result.returncode == 0 and result.stdout == expected_output:
                    print("PASSED")
                    num_passed += 1
                else:
                    print("FAILED")
                    print(f"Expected: {expected_output}")
                    print(f"Got: {result.stdout}")
                    print(result.stderr)
        except FileNotFoundError:
            print("FAILED")
            with open(f"tests/outputs/{file_stem}.out", "w") as f:
                f.write(result.stdout)
            print("Created output file")
    except Exception as e:
        print("FAILED")
        print(e)
        print(result.stderr)

print(f"Passed {num_passed}/{num_tests} tests")
if num_passed == num_tests:
    exit(0)
else:
    exit(1)
