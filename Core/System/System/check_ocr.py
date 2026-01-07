"""
Check OCR Availability
======================

Checks if Tesseract OCR is installed and usable.
"""

import sys
import os

try:
    import pytesseract
    from PIL import Image, ImageDraw
    
    print("✅ pytesseract module found.")
    
    # Common Windows paths for Tesseract
    paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe"
    ]
    
    tesseract_cmd = None
    for p in paths:
        if os.path.exists(p):
            tesseract_cmd = p
            break
            
    if tesseract_cmd:
        print(f"✅ Tesseract binary found at: {tesseract_cmd}")
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        
        # Test OCR
        img = Image.new('RGB', (100, 30), color = 'white')
        d = ImageDraw.Draw(img)
        d.text((10,10), "TEST", fill='black')
        
        try:
            text = pytesseract.image_to_string(img)
            print(f"✅ OCR Test Successful. Result: '{text.strip()}'")
        except Exception as e:
            print(f"❌ OCR Test Failed: {e}")
            
    else:
        print("❌ Tesseract binary NOT found in common paths.")
        print("   Please install Tesseract-OCR or set the path manually.")

except ImportError:
    print("❌ pytesseract module NOT installed.")
