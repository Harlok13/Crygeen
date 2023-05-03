#!/bin/bash

if [[ "$OSTYPE" == "darwin"* || "$OSTYPE" == "linux-gnu"* ]]; then
  # Mac OS X or Linux
  python3 -m venv env && source env/bin/activate && python3 -m pip install -U pip
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  # Windows/Cygwin or Windows/MinGW or Windows/PowerShell
  python -m venv env && source env/Scripts/activate && python -m pip install -U pip
else
  echo "Unsupported OS: $OSTYPE"
fi
  
pip install -r requirements.txt
