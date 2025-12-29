import subprocess
import os

known_results = {
    "25fv47": 5.5018458883e03,
    "30fv47": 5.5018458883e03,
    "40fv47": 5.5018458883e03,
    "50fv47": 5.5018458883e03,
    "60fv47": 5.5018458883e03,
    "70fv47": 5.5018458883e03,
    "80fv47": 5.5018458883e03,
    "80bau3b": 9.8723216072e05,
    "adlittle": 2.2549496316e05,
    "afiro": -4.6475314286e02,
    "agg": -3.5991767287e07,
    "agg2": -2.0239252356e07,
    "agg3": 1.0312115935e07,
    "bandm": -1.5862801845e02,
    "beaconfd": 3.3592485807e04,
    "blend": -3.0812149846e01,
    "bnl1": 1.9776292856e03,
    "bnl2": 1.8112365404e03,
    "boeing1": -3.3521356751e02,
    "boeing2": -3.1501872802e02,
    "bore3d": 1.3730803942e03,
    "brandy": 1.5185098965e03,
    "capri": 2.6900129138e03,
    "cycle": -5.2263930249e00,
    "czprob": 2.1851966989e06,
    "d2q06c": 1.2278423615e05,
    "d6cube": 3.1549166667e02,
    "degen2": -1.4351780000e03,
    "degen3": -9.8729400000e02,
    "dfl001": 1.12664e07,
    "e226": -1.8751929066e01,
    "etamacro": -7.5571521774e02,
    "fffff800": 5.5567961165e05,
    "finnis": 1.7279096547e05,
    "fit1d": -9.1463780924e03,
    "fit1p": 9.1463780924e03,
    "fit2d": -6.8464293294e04,
    "fit2p": 6.8464293232e04,
    "forplan": -6.6421873953e02,
    "ganges": -1.0958636356e05,
    "gfrd-pnc": 6.9022359995e06,
    "greenbea": -7.2462405908e07,
    "greenbeb": -4.3021476065e06,
    "grow15": -1.0687094129e08,
    "grow22": -1.6083433648e08,
    "grow7": -4.7787811815e07,
    "israel": -8.9664482186e05,
    "kb2": -1.7499001299e03,
    "lotfi": -2.5264706062e01,
    "maros": -5.8063743701e04,
    "maros-r7": 1.4971851665e06,
    "modszk1": 3.2061972906e02,
    "nesm": 1.4076073035e07,
    "perold": -9.3807580773e03,
    "pilot": -5.5740430007e02,
    "pilot.we": -2.7201027439e06,
    "pilot4": -2.5811392641e03,
    "pilot87": 3.0171072827e02,
    "pilotnov": -4.4972761882e03,
    "qap8": 2.0350000000e02,
    "qap12": 5.2289435056e02,
    "qap15": 1.0409940410e03,
    "recipe": -2.6661600000e02,
    "sc105": -5.2202061212e01,
    "sc205": -5.2202061212e01,
    "sc50a": -6.4575077059e01,
    "sc50b": -7.0000000000e01,
    "scagr25": -1.4753433061e07,
    "scagr7": -2.3313892548e06,
    "scfxm1": 1.8416759028e04,
    "scfxm2": 3.6660261565e04,
    "scfxm3": 5.4901254550e04,
    "scorpion": 1.8781248227e03,
    "scrs8": 9.0429998619e02,
    "scsd1": 8.6666666743e00,
    "scsd6": 5.0500000078e01,
    "scsd8": 9.0499999993e02,
    "sctap1": 1.4122500000e03,
    "sctap2": 1.7248071429e03,
    "sctap3": 1.4240000000e03,
    "seba": 1.5711600000e04,
    "share1b": -7.6589318579e04,
    "share2b": -4.1573224074e02,
    "shell": 1.2088253460e09,
    "ship04l": 1.7933245380e06,
    "ship04s": 1.7987147004e06,
    "ship08l": 1.9090552114e06,
    "ship08s": 1.9200982105e06,
    "sierra": 1.5394362184e07,
    "stair": -2.5126695119e02,
    "standata": 1.2576995000e03,
    "standmps": 1.4060175000e03,
    "stocfor1": -4.1131976219e04,
    "stocfor2": -3.9024408538e04,
    "stocfor3": -3.9976661576e04,
    "truss": 4.5881584719e05,
    "tuff": 2.9214776509e-01,
    "vtp.base": 1.2983146246e05,
    "wood1p": 1.4429024116e00,
    "woodw": 1.3044763331e00,
}

num_tests = 0
num_passed = 0


def run_test(
    name: str, vine_file_path: str, expected_output_path: str, stdin: str | None
):
    global num_tests, num_passed
    print(f"  Running test {name}: ", end="")
    num_tests += 1
    try:
        command = [
            "vine",
            "run",
            "--no-stats",
            vine_file_path,
            "--lib",
            "liana/liana.vi",
        ]
        result = subprocess.run(
            command,
            stdin=stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout = result.stdout
        if name in known_results:
            stdout = f"Expected optimal value: {known_results[name]}\n{stdout}"
        try:
            with open(expected_output_path, "r") as f:
                expected_output = f.read()
        except FileNotFoundError:
            expected_output = None

        # Compare with old expected output
        if result.returncode == 0 and stdout == expected_output:
            print("PASSED")
            num_passed += 1
        else:
            print("FAILED")
            if result.stderr:
                print(f"'{result.stderr}'")

        # Always write the new output
        with open(expected_output_path, "w") as f:
            f.write(stdout)

    except Exception:
        print("FAILED")
        if result.stderr:
            print(f"'{result.stderr}'")


def run_vi_tests(test_dir_name: str):
    print(f"Running {test_dir_name} tests")
    os.makedirs(f"tests/outputs/{test_dir_name}", exist_ok=True)
    for file in os.listdir(f"tests/{test_dir_name}"):
        file_stem = file.split(".")[0]
        run_test(
            file_stem,
            f"tests/{test_dir_name}/{file}",
            f"tests/outputs/{test_dir_name}/{file_stem}.out",
            stdin=None,
        )


def run_mps_tests(test_dir_name: str):
    print(f"Running {test_dir_name} tests")
    os.makedirs(f"tests/outputs/{test_dir_name}", exist_ok=True)
    for file in os.listdir(f"tests/{test_dir_name}"):
        with open(f"tests/{test_dir_name}/{file}", "r") as test_input_file:
            run_test(
                file,
                "tests/test_mps.vi",
                f"tests/outputs/{test_dir_name}/{file}.out",
                stdin=test_input_file,
            )


if __name__ == "__main__":
    run_vi_tests("linear_programs")
    run_mps_tests("netlib/small")

    print(f"Passed {num_passed}/{num_tests} tests")
    if num_passed == num_tests:
        exit(0)
    else:
        exit(1)
