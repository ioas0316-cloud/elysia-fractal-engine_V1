
import os
import tempfile
import google.generativeai as genai
import logging
from dotenv import load_dotenv
from google.api_core import exceptions as api_core_exceptions
from PIL import Image, ImageDraw, ImageFont
import random

try:
    from infra.telemetry import Telemetry
except Exception:
    Telemetry = None
try:
    from safety_guardian import SafetyGuardian, ActionCategory
except Exception:
    SafetyGuardian = None
    ActionCategory = None

# Load environment variables from env file
load_dotenv(override=True)

# --- Custom Exceptions ---
class APIKeyError(Exception):
    """Custom exception for errors related to the API key."""
    pass

class APIRequestError(Exception):
    """Custom exception for errors during API requests (e.g., network issues)."""
    pass

# --- Logging Configuration ---
def _writable_log_dir() -> str:
    # Prefer project 'saves' or 'logs' dir relative to CWD
    for rel in (
        'saves',
        os.path.join('ElysiaStarter', 'saves'),
        os.path.join('archive', 'ElysiaStarter_legacy', 'saves'),
        'logs',
    ):
        p = os.path.abspath(os.path.join(os.getcwd(), rel))
        try:
            os.makedirs(p, exist_ok=True)
            return p
        except Exception:
            continue
    # Fallback to system temp
    return tempfile.gettempdir()

log_file_path = os.path.join(_writable_log_dir(), 'gemini_api_errors.log')
try:
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
except Exception:
    pass
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file_path, encoding='utf-8')]
)
gemini_logger = logging.getLogger(__name__)
# --- End Logging Configuration ---

class GeminiAPI:
    def __init__(self):
        self._is_configured = False
        self._telemetry = Telemetry() if Telemetry else None
        self._guardian = SafetyGuardian() if SafetyGuardian else None
        self._configure_genai_if_needed()

    def _configure_genai_if_needed(self):
        """Checks if the genai library is configured and configures it if not."""
        if self._is_configured:
            return

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key or "your_api_key" in api_key:
            gemini_logger.warning("GEMINI_API_KEY not set. Using Mock Mode.")
            self._is_configured = False
            return
            
        try:
            genai.configure(api_key=api_key)
            self._is_configured = True
        except Exception as e:
            gemini_logger.exception(f"Failed to configure Gemini API: {e}")
            self._is_configured = False

    def get_text_embedding(self, text: str, model="models/text-embedding-004"):
        """Generates an embedding for the given text using the specified Gemini model."""
        self._configure_genai_if_needed()
        
        if not self._is_configured:
            # Return mock embedding (random vector)
            return [random.random() for _ in range(768)]
            
        try:
            return genai.embed_content(model=model, content=text)["embedding"]
        except Exception as e:
            gemini_logger.exception(f"Embedding failed: {e}")
            return [random.random() for _ in range(768)]

    def generate_text(self, prompt: str, model_name="models/gemini-2.5-pro"):
        """Generates text using the specified Gemini model."""
        self._configure_genai_if_needed()
        
        if not self._is_configured:
            return f"(Mock Response) I am thinking about: {prompt[:50]}... My internal resonance is shifting."
            
        model = genai.GenerativeModel(model_name)
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            gemini_logger.exception(f"Generation failed: {e}")
            return f"(Error Response) I could not think clearly: {e}"

    def generate_image_from_text(self, text: str, output_path: str) -> bool:
        """
        Generates a placeholder image with the given text.
        This does not use the Gemini API and will not raise an APIKeyError.
        """
        try:
            width, height = 800, 600
            img = Image.new('RGB', (width, height), color = (20, 20, 40)) # Dark blue background
            d = ImageDraw.Draw(img)

            # Use a default font, handle multiline text
            font = ImageFont.load_default()
            lines = text.split('\n')
            y_text = 10
            for line in lines:
                d.text((10, y_text), line, fill=(200, 200, 255), font=font)
                y_text += 20 # Move to the next line

            img.save(output_path)
            print(f"Placeholder image generated at: {output_path}")
            return True
        except Exception as e:
            gemini_logger.error(f"Failed to create placeholder image: {e}")
            return False

_gemini_singleton: GeminiAPI | None = None

def _get_gemini() -> GeminiAPI:
    global _gemini_singleton
    if _gemini_singleton is None:
        _gemini_singleton = GeminiAPI()
    return _gemini_singleton

def get_text_embedding(text: str, model="models/text-embedding-004"):
    return _get_gemini().get_text_embedding(text, model)

def generate_text(prompt: str, model_name="models/gemini-2.5-pro"):
    return _get_gemini().generate_text(prompt, model_name)

def generate_image_from_text(text: str, output_path: str):
    return _get_gemini().generate_image_from_text(text, output_path)
