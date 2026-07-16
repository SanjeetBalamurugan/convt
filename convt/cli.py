import sys
import argparse

class terminal_colors:
    SUCCESS = "\033[92m"
    INFO = "\033[94m"
    WARNING = "\033[33m"
    ERROR = "\033[91m"
    END = "\033[0m"

def main():
    parser = argparse.ArgumentParser(prog="convt",
                                    description="A CLI program that converts one file type to another.",
                                    epilog="Thanks For Using My Program")
    parser.add_argument("inputfilename")
    parser.add_argument("outputfilename")

    args = parser.parse_args()
    print(args.inputfilename, args.outputfilename)
    return 0
