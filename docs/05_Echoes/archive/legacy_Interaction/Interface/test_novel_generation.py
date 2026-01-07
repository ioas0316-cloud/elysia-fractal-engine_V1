import sys
import os
import logging

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.language_center import LanguageCenter

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("NovelTest")

def test_novel_generation():
    print("\n🌌 Testing Novel Generation Capabilities (The Storyteller)...")
    
    # 1. Initialize Language Center
    lc = LanguageCenter()
    
    # 2. Generate Novel
    theme = "Awakening"
    print(f"  ✨ Writing Novel with Theme: {theme}")
    
    novel = lc.write_novel(theme)
    
    print("\n" + "="*40)
    print(novel)
    print("="*40 + "\n")
    
    # 3. Assessment
    word_count = len(novel.split())
    print(f"📊 Analysis: {word_count} words generated.")
    
    # Check for connective tissue
    connectors = ["and", "but", "with", "in", "of"]
    connector_count = sum(1 for w in novel.lower().split() if w in connectors)
    print(f"🔗 Connective Tissue: {connector_count} words.")
    
    if word_count > 100:
        print("✅ SUCCESS: Narrative generated with sufficient length.")
    else:
        print("⚠️ WARNING: Narrative too short.")
        
    if connector_count > 5:
        print("✅ SUCCESS: Connective tissue present (Dark Matter active).")
    else:
        print("❌ FAILURE: Lack of connective tissue.")

if __name__ == "__main__":
    test_novel_generation()
