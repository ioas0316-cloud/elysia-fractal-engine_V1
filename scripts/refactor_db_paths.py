import os
from pathlib import Path

TARGET_FILES = [
    r"c:\Elysia\Core\Intelligence\Memory\find_dream_concepts.py",
    r"c:\Elysia\Core\Intelligence\Memory\memory_initializer.py",
    r"c:\Elysia\Core\Intelligence\Memory\vacuum_db.py",
    r"c:\Elysia\Core\Intelligence\Memory\analyze_전체시스템.py",
    r"c:\Elysia\Core\Intelligence\Memory\analyze_db_size.py",
    r"c:\Elysia\Core\Intelligence\Memory\analyze_db_patterns.py",
    r"c:\Elysia\Core\Intelligence\Intelligence\analyze_concept_isolation.py",
    r"c:\Elysia\Core\Intelligence\Intelligence\check_memory_db.py",
    r"c:\Elysia\Core\Intelligence\Intelligence\system_self_awareness.py",
    r"c:\Elysia\Core\Foundation\attractor.py",
    r"c:\Elysia\Core\Foundation\Autonomy\autonomous_evolution.py",
    r"c:\Elysia\Core\Foundation\Autonomy\self_diagnosis.py",
    r"c:\Elysia\Core\Foundation\fractal_vocabulary_expansion.py",
    r"c:\Elysia\Core\Foundation\Memory\vocabulary_migrator.py",
    r"c:\Elysia\Core\Foundation\reorganize_memory_universe.py",
    r"c:\Elysia\Core\Foundation\Memory\Graph\hippocampus.py",
    r"c:\Elysia\Core\Foundation\Memory\migrate_legacy_concepts.py",
    r"c:\Elysia\Core\Foundation\Memory\migrate_seeds_to_db.py",
    r"c:\Elysia\Core\Foundation\Memory\reorganize_memory_universe.py"
]

def fix_paths():
    count = 0
    for file_path in TARGET_FILES:
        path = Path(file_path)
        if not path.exists():
            print(f"Skipping {path} (Not found)")
            continue
            
        try:
            content = path.read_text(encoding='utf-8')
            new_content = content
            
            # Replace variations of memory.db path
            replacements = {
                '"memory.db"': '"data/Memory/memory.db"',
                "'memory.db'": "'data/Memory/memory.db'",
                '"c:/Elysia/memory.db"': '"data/Memory/memory.db"',
                '"C:/Elysia/memory.db"': '"data/Memory/memory.db"',
                '"data/core_state/memory.db"': '"data/Memory/memory.db"',
                '"Data/memory.db"': '"data/Memory/memory.db"'
            }
            
            for old, new in replacements.items():
                new_content = new_content.replace(old, new)
            
            if content != new_content:
                path.write_text(new_content, encoding='utf-8')
                print(f"Fixed: {path.name}")
                count += 1
        except Exception as e:
            print(f"Error processing {path}: {e}")
            
    print(f"Total files fixed: {count}")

if __name__ == "__main__":
    fix_paths()
