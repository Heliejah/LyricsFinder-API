# Test file to verify imports
import os
import sys

print("Current working directory:", os.getcwd())
print("Python path:", sys.path)

try:
    import flask
    print("Flask imported successfully")
except ImportError as e:
    print("Flask import error:", e)
