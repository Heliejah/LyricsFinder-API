import sys
import os
import locale

print("=== Python Environment Diagnostics ===")
print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")
print(f"File System Encoding: {sys.getfilesystemencoding()}")
print(f"Default Encoding: {sys.getdefaultencoding()}")
print(f"Locale Encoding: {locale.getpreferredencoding()}")
print(f"Current Working Directory: {os.getcwd()}")

# Test file reading
try:
    with open('scripts/api.py', 'rb') as f:
        content = f.read()
        print("\nFirst 100 bytes of api.py:", content[:100])
        # Check for null bytes
        if b'\x00' in content:
            print("WARNING: Null bytes detected in api.py!")
except Exception as e:
    print(f"Error reading api.py: {e}")
