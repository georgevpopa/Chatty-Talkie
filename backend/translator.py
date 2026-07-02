"""
Chatty Talkie - Translation Engine
Uses Meta's NLLB-200 distilled 600M model for RO/ES/EN translations.
"""

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch


# NLLB language codes
LANGUAGE_CODES = {
    "en": "eng_Latn",
    "ro": "ron_Latn",
    "es": "spa_Latn",
}

LANGUAGE_NAMES = {
    "en": "English",
    "ro": "Romanian",
    "es": "Spanish",
}

MODEL_NAME = "facebook/nllb-200-distilled-600M"


class Translator:
    """Handles loading the NLLB model and performing translations."""

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._loaded = False

    def load_model(self):
        """Load the NLLB model and tokenizer. Call once at startup."""
        if self._loaded:
            return

        print(f"Loading NLLB model on {self.device}...")
        print("First run will download ~1.2GB model. Please wait...")

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        self.model.to(self.device)
        self.model.eval()

        self._loaded = True
        print("Model loaded successfully!")

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text from source language to target language.

        Args:
            text: The text to translate.
            source_lang: Source language code ('en', 'ro', 'es').
            target_lang: Target language code ('en', 'ro', 'es').

        Returns:
            Translated text string.
        """
        if not self._loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        if source_lang not in LANGUAGE_CODES:
            raise ValueError(f"Unsupported source language: {source_lang}")
        if target_lang not in LANGUAGE_CODES:
            raise ValueError(f"Unsupported target language: {target_lang}")
        if source_lang == target_lang:
            return text

        src_code = LANGUAGE_CODES[source_lang]
        tgt_code = LANGUAGE_CODES[target_lang]

        # Set source language for tokenizer
        self.tokenizer.src_lang = src_code

        # Tokenize input
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512,
        ).to(self.device)

        # Generate translation
        with torch.no_grad():
            generated_tokens = self.model.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(tgt_code),
                max_new_tokens=512,
                num_beams=5,
                early_stopping=True,
            )

        # Decode output
        result = self.tokenizer.batch_decode(
            generated_tokens, skip_special_tokens=True
        )

        return result[0]

    def get_supported_languages(self) -> dict:
        """Return dictionary of supported language codes and names."""
        return LANGUAGE_NAMES.copy()

    def is_loaded(self) -> bool:
        """Check if the model is loaded and ready."""
        return self._loaded
