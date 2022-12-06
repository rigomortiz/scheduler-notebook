# content of myinvoke.py
import pytest
import sys


if __name__ == "__main__":
    args = sys.argv[1:]
    print(args)
    if len(args) == 2 and args[0] == '--tests':
        # Print with the name in args[1]
        sys.exit(pytest.main(["-x", args[1]]))