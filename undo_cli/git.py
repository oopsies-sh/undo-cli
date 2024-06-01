from utils import run_cmd
import os


def main():
    log = run_cmd(["git", "log"])

    if log:
        print(log)


if __name__ == "__main__":
    main()
