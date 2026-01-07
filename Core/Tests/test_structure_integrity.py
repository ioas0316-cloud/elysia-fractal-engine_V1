import os
import pytest

# Define the root directory of the project
PROJECT_ROOT = "c:\\Elysia"

def test_root_directory_trinity():
    """
    Enforce the 'Trinity Rule': Root should only contain Core, Docs, Data, Archive, and minimal config.
    """
    allowed_roots = {
        "core", "docs", "data", "archive",  # The Trinity + History (Lowercase for comparison)
        ".git", ".github", ".vscode", ".venv", ".agent", ".jules", # Configs
        "readme.md", "license", "agents.md", # Essential Docs
        "monitor_elysia.bat", "run_system.bat", "start_elysia.bat", # Bootloaders
        "wake_up_elysia.py", "visualizer.pid", # Runtime
        "dashboard_debug.log", "test_output.txt", "final_boot_check.log", "final_boot_check_v2.log" # Logs
    }
    
    # Tolerated for now but should be moved eventually
    tolerated_legacy = {".pre-commit-config.yaml", ".gitignore", ".env", ".env.example", ".gitattributes", ".editorconfig", ".dockerignore", ".pytest_cache"}

    current_items = os.listdir(PROJECT_ROOT)
    
    for item in current_items:
        # Case-insensitive check
        if item.lower() in allowed_roots or item.lower() in tolerated_legacy:
            continue
        
        # Fail if an unknown item is found in root
        full_path = os.path.join(PROJECT_ROOT, item)
        # Check if it's a directory or file that shouldn't be there
        if os.path.isdir(full_path) or item not in allowed_roots:
             pytest.fail(f"FORBIDDEN ROOT ITEM: '{item}'. Root must only contain Core, Docs, Data. Move this to one of them.")


def test_no_forbidden_directories_in_docs():
    """
    Enforce that specific legacy or duplicate directories do not exist in Docs/.
    """
    forbidden_dirs = [
        "Docs\\Philosophy",
        "Docs\\Roadmap",
        "Docs\\Analysis",
        "Docs\\Vision",
    ]
    
    for relative_path in forbidden_dirs:
        full_path = os.path.join(PROJECT_ROOT, relative_path)
        assert not os.path.exists(full_path), f"FORBIDDEN DIRECTORY FOUND: {full_path}. \nAction Required: Move contents to canonical location and delete this folder."

def test_canonical_directories_exist():
    """
    Ensure the canonical directories actually exist.
    """
    required_dirs = [
        "Docs\\01_Origin\\Philosophy",
        "Docs\\04_Evolution\\Roadmaps",
        "Docs\\05_Echoes\\Analysis",
        "Docs\\04_Evolution\\Vision",
        "Core\\Tests",
        "Core\\Scripts",
        "data\\Knowledge",
    ]

    for relative_path in required_dirs:
        full_path = os.path.join(PROJECT_ROOT, relative_path)
        assert os.path.isdir(full_path), f"MISSING CANONICAL DIRECTORY: {full_path}. \nAction Required: Create this mandatory directory."

if __name__ == "__main__":
    pytest.main([__file__])

