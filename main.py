"""Entry point for verifying the active Python interpreter."""

import sys


def main(age: int) -> None:

    print(age)
    print(sys.executable)


if __name__ == "__main__":
    main(25)
