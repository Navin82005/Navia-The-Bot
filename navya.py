#!/usr/bin/env python

import argparse
import subprocess

def init():
    subprocess.run(["python", "setup.py"])

def main():
    parser = argparse.ArgumentParser(prog="navya", description="Navya AI CLI")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("init", help="Run setup wizard")
    args = parser.parse_args()

    if args.command == "init":
        init()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
