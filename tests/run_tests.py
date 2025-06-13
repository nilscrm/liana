import subprocess
import os

known_results = {
  "25fv47": 5.5018458883E+03,
  "30fv47": 5.5018458883E+03,
  "40fv47": 5.5018458883E+03,
  "50fv47": 5.5018458883E+03,
  "60fv47": 5.5018458883E+03,
  "70fv47": 5.5018458883E+03,
  "80fv47": 5.5018458883E+03,
  "80bau3b": 9.8723216072E+05,
  "adlittle": 2.2549496316E+05,
  "afiro": -4.6475314286E+02,
  "agg": -3.5991767287E+07,
  "agg2": -2.0239252356E+07,
  "agg3": 1.0312115935E+07,
  "bandm": -1.5862801845E+02,
  "beaconfd": 3.3592485807E+04,
  "blend": -3.0812149846E+01,
  "bnl1": 1.9776292856E+03,
  "bnl2": 1.8112365404E+03,
  "boeing1": -3.3521356751E+02,
  "boeing2": -3.1501872802E+02,
  "bore3d": 1.3730803942E+03,
  "brandy": 1.5185098965E+03,
  "capri": 2.6900129138E+03,
  "cycle": -5.2263930249E+00,
  "czprob": 2.1851966989E+06,
  "d2q06c": 1.2278423615E+05,
  "d6cube": 3.1549166667E+02,
  "degen2": -1.4351780000E+03,
  "degen3": -9.8729400000E+02,
  "dfl001": 1.12664E+07,
  "e226": -1.8751929066E+01,
  "etamacro": -7.5571521774E+02,
  "fffff800": 5.5567961165E+05,
  "finnis": 1.7279096547E+05,
  "fit1d": -9.1463780924E+03,
  "fit1p": 9.1463780924E+03,
  "fit2d": -6.8464293294E+04,
  "fit2p": 6.8464293232E+04,
  "forplan": -6.6421873953E+02,
  "ganges": -1.0958636356E+05,
  "gfrd-pnc": 6.9022359995E+06,
  "greenbea": -7.2462405908E+07,
  "greenbeb": -4.3021476065E+06,
  "grow15": -1.0687094129E+08,
  "grow22": -1.6083433648E+08,
  "grow7": -4.7787811815E+07,
  "israel": -8.9664482186E+05,
  "kb2": -1.7499001299E+03,
  "lotfi": -2.5264706062E+01,
  "maros": -5.8063743701E+04,
  "maros-r7": 1.4971851665E+06,
  "modszk1": 3.2061972906E+02,
  "nesm": 1.4076073035E+07,
  "perold": -9.3807580773E+03,
  "pilot": -5.5740430007E+02,
  "pilot.we": -2.7201027439E+06,
  "pilot4": -2.5811392641E+03,
  "pilot87": 3.0171072827E+02,
  "pilotnov": -4.4972761882E+03,
  "qap8": 2.0350000000E+02,
  "qap12": 5.2289435056E+02,
  "qap15": 1.0409940410E+03,
  "recipe": -2.6661600000E+02,
  "sc105": -5.2202061212E+01,
  "sc205": -5.2202061212E+01,
  "sc50a": -6.4575077059E+01,
  "sc50b": -7.0000000000E+01,
  "scagr25": -1.4753433061E+07,
  "scagr7": -2.3313892548E+06,
  "scfxm1": 1.8416759028E+04,
  "scfxm2": 3.6660261565E+04,
  "scfxm3": 5.4901254550E+04,
  "scorpion": 1.8781248227E+03,
  "scrs8": 9.0429998619E+02,
  "scsd1": 8.6666666743E+00,
  "scsd6": 5.0500000078E+01,
  "scsd8": 9.0499999993E+02,
  "sctap1": 1.4122500000E+03,
  "sctap2": 1.7248071429E+03,
  "sctap3": 1.4240000000E+03,
  "seba": 1.5711600000E+04,
  "share1b": -7.6589318579E+04,
  "share2b": -4.1573224074E+02,
  "shell": 1.2088253460E+09,
  "ship04l": 1.7933245380E+06,
  "ship04s": 1.7987147004E+06,
  "ship08l": 1.9090552114E+06,
  "ship08s": 1.9200982105E+06,
  "sierra": 1.5394362184E+07,
  "stair": -2.5126695119E+02,
  "standata": 1.2576995000E+03,
  "standmps": 1.4060175000E+03,
  "stocfor1": -4.1131976219E+04,
  "stocfor2": -3.9024408538E+04,
  "stocfor3": -3.9976661576E+04,
  "truss": 4.5881584719E+05,
  "tuff": 2.9214776509E-01,
  "vtp.base": 1.2983146246E+05,
  "wood1p": 1.4429024116E+00,
  "woodw": 1.3044763331E+00,
}

num_tests = 0
num_passed = 0

def run_test(name: str, vine_file_path: str, expected_output_path: str, stdin: str | None):
    global num_tests, num_passed
    print(f"  Running test {name}: ", end="")
    num_tests += 1
    try:
        command = ["vine", "run", "--no-stats", vine_file_path]
        result = subprocess.run(command, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout = result.stdout
        if name in known_results:
            stdout = f"Expected optimal value: {known_results[name]}\n{stdout}"
        try:
            with open(expected_output_path, "r") as f:
                expected_output = f.read()
                if result.returncode == 0 and stdout == expected_output:
                    print("PASSED")
                    num_passed += 1
                else:
                    print("FAILED")
                    print(f"Expected: {expected_output}")
                    print(f"Got: {stdout}")
                    print(result.stderr)
        except FileNotFoundError:
            print("FAILED")
            with open(expected_output_path, "w") as f:
                f.write(stdout)
            print("Created new output file")
    except Exception as e:
        print("FAILED")
        print(e)
        print(result.stderr)


def run_vi_tests(test_dir_name: str):
    print(f"Running {test_dir_name} tests")
    os.makedirs(f"tests/outputs/{test_dir_name}", exist_ok=True)
    for file in os.listdir(f"tests/{test_dir_name}"):
        file_stem = file.split(".")[0]
        run_test(file_stem, f"tests/{test_dir_name}/{file}", f"tests/outputs/{test_dir_name}/{file_stem}.out", stdin=None)


def run_mps_tests(test_dir_name: str):
    print(f"Running {test_dir_name} tests")
    os.makedirs(f"tests/outputs/{test_dir_name}", exist_ok=True)
    for file in os.listdir(f"tests/{test_dir_name}"):
        with open(f"tests/{test_dir_name}/{file}", "r") as test_input_file:
            run_test(file, f"tests/test_mps.vi", f"tests/outputs/{test_dir_name}/{file}.out", stdin=test_input_file)

if __name__ == "__main__":
    run_vi_tests("linear_programs")
    run_mps_tests("netlib/small")

    print(f"Passed {num_passed}/{num_tests} tests")
    if num_passed == num_tests:
        exit(0)
    else:
        exit(1)
