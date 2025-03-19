import subprocess
import os

num_tests = 0
num_passed = 0

expected_output = {
    "lp1.vi": (18, [2, 3]),
    "lp2.vi": (23, [2, 3]),
}

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

        sol_val, sol = result.stdout.split(",", maxsplit=1)
        sol_val = float(sol_val.strip())
        sol = list(float(x) for x in sol.strip().strip("[]").split(","))
        expected_sol_val, expected_sol = expected_output[file]
        if sol_val == expected_sol_val and sol == expected_sol:
            print("PASSED")
            num_passed += 1
        else:
            print("FAILED")
            print(f"Expected: {expected_sol_val}, {expected_sol}")
            print(f"Got: {sol_val}, {sol}")
            print(result.stderr)
    except Exception as e:
        print("FAILED")
        print(e)
        print(result.stderr)

print(f"Passed {num_passed}/{num_tests} tests")
if num_passed == num_tests:
    exit(0)
else:
    exit(1)
