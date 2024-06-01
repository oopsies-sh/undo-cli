import subprocess


def run_cmd(args):
    try:
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout, stderr
    except Exception as e:
        return None, str(e)


if __name__ == "__main__":
    # Run the command
    stdout, stderr = run_cmd(["ls", "-l"])
    if stderr:
        print("Error: ", stderr)
    else:
        print("Output: ", stdout)
