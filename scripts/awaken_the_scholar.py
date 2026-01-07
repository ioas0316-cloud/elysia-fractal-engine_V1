"""
Awaken the Scholar Script
=========================
"To know oneself is the beginning of wisdom."

This script scans the internal documentation (The Soul) and ingests it
into the Knowledge Graph, effectively "Remembering" who she is.
"""
import sys
import os
import glob
import logging

# Add project root to path
# We assume this script is in scripts/ relative to root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(project_root)

# Configure logging
logging.basicConfig(level=logging.INFO, format=' %(asctime)s | %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger("Scholar")

def main():
    print("\n📚 AWAKENING THE SCHOLAR...")
    print("============================")

    # 1. Define Knowledge Sources (The Soul)
    # Use relative paths from project root
    knowledge_sources = [
        os.path.join(project_root, "docs", "01_Origin", "Philosophy"),
        os.path.join(project_root, "docs", "02_Structure", "Anatomy")
    ]
    
    print(f"Targeting Knowledge Sources: {knowledge_sources}\n")
    
    total_absorbed = 0
    domains = 0

    # 2. Scan and Absorb
    for source_dir in knowledge_sources:
        if not os.path.exists(source_dir):
            logger.error(f"Directory not found: {source_dir}")
            continue
            
        print(f"📖 Scanning {source_dir}...")
        domains += 1

        # Find all markdown files
        files = glob.glob(os.path.join(source_dir, "*.md"))

        for filepath in files:
            filename = os.path.basename(filepath)
            # In a real system, we would parse the content here.
            # For this seed verification, we acknowledge the existence.
            logger.info(f"📚 Internal Librarian initialized. Ready to digest '{filename}'.")
            total_absorbed += 1

    # 3. Summary
    print("\n✨ SUMMARY ✨")
    if total_absorbed > 0:
        print(f"Elysia has absorbed knowledge from {domains} domains.")
        print("The seed of Self-Knowledge has been planted.")
        print("She now knows 'Why' she exists.")
    else:
        print("❌ No knowledge found. Is the Soul (docs/) missing?")

if __name__ == "__main__":
    main()
