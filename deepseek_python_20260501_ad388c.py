import argparse
from rtt.doctor import run_doctor

def main():
    parser = argparse.ArgumentParser(prog="rtt")
    subparsers = parser.add_subparsers(dest="command")

    # doctor
    subparsers.add_parser("doctor", help="Check platform capabilities")

    args = parser.parse_args()
    if args.command == "doctor":
        run_doctor()
    else:
        parser.print_help()