#!/bin/bash
echo "*** RUN SCRIPT BASH ***"
python3 main.py
pytest test/main.py
echo "*** END SCRIPT BASH ***"