import re
import os

def fix_json_conflicts(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    in_conflict = False
    keep_head = True # By default, keep the HEAD (local) version

    for line in lines:
        if line.startswith('<<<<<<<'):
            in_conflict = True
            continue
        if line.startswith('======='):
            keep_head = False
            continue
        if line.startswith('>>>>>>>'):
            in_conflict = False
            keep_head = True
            continue
        
        if in_conflict:
            if keep_head:
                new_lines.append(line)
        else:
            new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Fixed conflicts in {filepath}")

if __name__ == "__main__":
    fix_json_conflicts('C:/Elysia/data/memory/experience/memory_state.json')
