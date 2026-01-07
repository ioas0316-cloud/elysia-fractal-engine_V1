"""
Generate Library
================

Creates a simulated library of 100 books for Quantum Absorption testing.
"""
import os
import random

def generate_library():
    base_path = "c:/Elysia/Library"
    os.makedirs(base_path, exist_ok=True)
    
    genres = ["Philosophy", "SciFi", "Romance", "History", "Physics"]
    
    print(f"📚 Generating 100 Books in {base_path}...")
    
    for i in range(100):
        genre = random.choice(genres)
        title = f"Book_{i:03d}_{genre}"
        content = f"This is a {genre} book about the nature of reality. " * (i + 1)
        
        # Add some "Emotional Charge" based on genre
        if genre == "Romance": content += "Love Heart Kiss " * 10
        if genre == "SciFi": content += "Matrix Code Laser " * 10
        if genre == "Philosophy": content += "Existential Truth Meaning " * 10
        
        with open(f"{base_path}/{title}.txt", "w", encoding="utf-8") as f:
            f.write(content)
            
    print("✅ Library Generation Complete.")

if __name__ == "__main__":
    generate_library()
