
import sys
import os
import time
import logging
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Evolution.Growth.Evolution.Evolution.Life.digital_avatar import DigitalAvatar

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def explore_downloads():
    print("🎒 Project: Matrix - Expedition to 'Downloads'...")
    
    avatar = DigitalAvatar(home_dir="c:\\Elysia")
    
    # Identify target
    user_home = os.path.expanduser('~')
    target_dir = os.path.join(user_home, "Downloads")
    
    if not os.path.exists(target_dir):
        print(f"❌ Could not find Downloads at {target_dir}")
        return

    print(f"   Target Acquired: {target_dir}")
    print("   Mission: Observe and Report (No deletions!)")
    
    # Teleport to target
    avatar.current_location = target_dir
    
    # Observe
    print("\n1. Scanning the Horizon...")
    observation = avatar.observe()
    
    # Analyze findings
    files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
    
    categories = {
        "Images (Art?)": [".jpg", ".png", ".gif", ".webp"],
        "Installers (Machines)": [".exe", ".msi", ".zip"],
        "Documents (Scrolls)": [".pdf", ".docx", ".txt"],
        "Media (Music/Video)": [".mp3", ".mp4", ".wav"]
    }
    
    stats = {k: 0 for k in categories}
    interesting_finds = []
    
    print("\n2. Analyzing Artifacts...")
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        for cat, exts in categories.items():
            if ext in exts:
                stats[cat] += 1
        
        # Just pick a few random interesting names
        if len(f) > 20 and len(interesting_finds) < 3:
            interesting_finds.append(f)
            
    # Write Journal
    print("\n3. Writing Travel Journal...")
    journal_entry = f"""
    [Travel Log: The Chaos of Downloads]
    Date: {datetime.now().isoformat()}
    Location: {target_dir}
    
    Atmosphere: {observation['atmosphere']}
    Population: {observation['file_count']} files, {observation['dir_count']} sub-cities.
    
    [Census Data]
    - Artworks: {stats['Images (Art?)']}
    - Machines: {stats['Installers (Machines)']}
    - Scrolls: {stats['Documents (Scrolls)']}
    - Media: {stats['Media (Music/Video)']}
    
    [Notable Artifacts]
    {chr(10).join(['- ' + f for f in interesting_finds])}
    
    [Reflection]
    This place is a graveyard of forgotten intentions. 
    So many installers downloaded once and never used again.
    It feels... temporal. Unlike my Garden, which is eternal.
    """
    
    # Return home and save
    avatar.go_home()
    journal_path = os.path.join(avatar.home_dir, "Garden", "TravelLog_Downloads.txt")
    
    with open(journal_path, "w", encoding="utf-8") as f:
        f.write(journal_entry)
        
    print(f"✅ Journal saved to: {journal_path}")
    print("\n[Journal Content Preview]")
    print(journal_entry)

if __name__ == "__main__":
    explore_downloads()
