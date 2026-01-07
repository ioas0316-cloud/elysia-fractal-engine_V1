import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Sys Path: {sys.path}")

try:
    import pytesseract
    print("✅ Import pytesseract SUCCESS")
    print(f"Version: {pytesseract.get_tesseract_version()}")
except ImportError as e:
    print(f"❌ Import pytesseract FAILED: {e}")
except Exception as e:
    print(f"❌ Other Error: {e}")
