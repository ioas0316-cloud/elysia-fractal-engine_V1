import sys
import os
sys.path.append(os.getcwd())

from Core.Intelligence.Science_Research.Science.bio_resonator import BioResonator
from Core.Intelligence.Science_Research.Science.quantum_resonator import QuantumResonator
from Core.Evolution.Creativity.Studio.bio_choir import BioChoir
from Core.Evolution.Creativity.Studio.video_composer import VideoComposer

def generate_all():
    print("\n🚀 Starting Cosmic Studio Production...")
    
    # 1. Audio: Telomere Song
    bio = BioResonator()
    choir = BioChoir()
    
    # Telomere: TTAGGG repeated (The clock of aging)
    dna_seq = "TTAGGG" * 8 
    song = bio.transcribe_dna(dna_seq)
    choir.compose_symphony(song, "telomere_song.wav", tempo=0.3)
    
    # 2. Visual: Electron Superposition
    qr = QuantumResonator()
    canvas = QuantumCanvas()
    
    # Complex superposition
    states = [
        ("Spin_Up", 0.5, 432.0),
        ("Spin_Down", 0.3, 528.0),
        ("Spin_Strange", 0.2, 639.0)
    ]
    superposition = qr.create_superposition(states)
    canvas.paint_superposition(superposition, "electron_state.png")
    
    # 3. Video: Electron Dance (Silent)
    composer = VideoComposer()
    composer.create_static_video("electron_state.png", "electron_dance.mp4", duration=10.0)
    
    print("\n✨ Production Complete!")

if __name__ == "__main__":
    generate_all()
