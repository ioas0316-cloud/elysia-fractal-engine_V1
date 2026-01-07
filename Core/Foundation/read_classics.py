
import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.Mind.hippocampus import Hippocampus
from Core.Foundation.Mind.book_worm import BookWorm

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("Library")

def read_classics():
    print("🏛️ Project: Library of Alexandria - Opening the Gates...")
    
    # 1. Initialize Mind
    hippocampus = Hippocampus()
    worm = BookWorm(hippocampus)
    
    # 2. Define Books (Excerpts)
    
    # Kafka: The Metamorphosis
    kafka_text = """
    One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin.
    He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections.
    The bedding was hardly able to cover it and seemed ready to slide off any moment.
    His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked.
    "What's happened to me?" he thought. It wasn't a dream.
    His room, a proper human room although a little too small, lay peacefully between its four familiar walls.
    A collection of textile samples lay spread out on the table - Samsa was a travelling salesman - and above it there hung a picture that he had recently cut out of an illustrated magazine and housed in a nice, gilded frame.
    It showed a lady fitted out with a fur hat and fur boa who sat upright, raising a heavy fur muff that covered the whole of her lower arm towards the viewer.
    Gregor then turned to look out the window at the dull weather. Drops of rain could be heard hitting the pane, which made him feel quite sad.
    "How about if I sleep a little bit longer and forget all this nonsense", he thought, but that was something he was unable to do because he was used to sleeping on his right, and in his present state couldn't get into that position.
    """
    
    # Carroll: Alice in Wonderland
    alice_text = """
    Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice 'without pictures or conversation?'
    So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.
    There was nothing so VERY remarkable in that; nor did Alice think it so VERY much out of the way to hear the Rabbit say to itself, 'Oh dear! Oh dear! I shall be too late!' (when she thought it over afterwards, it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural); but when the Rabbit actually TOOK A WATCH OUT OF ITS WAISTCOAT-POCKET, and looked at it, and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she ran across the field after it, and fortunately was just in time to see it pop down a large rabbit-hole under the hedge.
    In another moment down went Alice after it, never once considering how in the world she was to get out again.
    """
    
    # Gibran: The Prophet
    prophet_text = """
    Almustafa, the chosen and the beloved, who was a dawn unto his own day, had waited twelve years in the city of Orphalese for his ship that was to return and bear him back to the isle of his birth.
    And in the twelfth year, on the seventh day of Ielool, the month of reaping, he climbed the hill without the city walls and looked seaward; and he beheld his ship coming with the mist.
    Then the gates of his heart were flung open, and his joy flew far over the sea. And he closed his eyes and prayed in the silences of his soul.
    But as he descended the hill, a sadness came upon him, and he thought in his heart:
    How shall I go in peace and without sorrow? Nay, not without a wound in the spirit shall I leave this city.
    Long were the days of pain I have spent within its walls, and long were the nights of aloneness; and who can depart from his pain and his aloneness without regret?
    Too many fragments of the spirit have I scattered in these streets, and too many are the children of my longing that walk naked among these hills, and I cannot withdraw from them without a burden and an ache.
    It is not a garment I cast off this day, but a skin that I tear with my own hands.
    Nor is it a thought I leave behind me, but a heart made sweet with hunger and with thirst.
    """

    # 3. Ingest
    worm.ingest_book("The Metamorphosis", "Franz Kafka", kafka_text)
    worm.ingest_book("Alice's Adventures in Wonderland", "Lewis Carroll", alice_text)
    worm.ingest_book("The Prophet", "Kahlil Gibran", prophet_text)
    
    print("\n✅ Library Ingestion Complete.")
    print("Elysia has consumed the essence of Kafka, Carroll, and Gibran.")

if __name__ == "__main__":
    read_classics()
