import re
import spacy
import logging

logger = logging.getLogger(__name__)

# Try loading the spacy model, fallback if not available (e.g., during tests without model)
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    logger.warning(f"Failed to load spacy model 'en_core_web_sm': {e}. PII redaction might be limited.")
    nlp = None

def redact_pii(text: str) -> str:
    """
    Detects and redacts Personally Identifiable Information (PII) from the given text.
    Uses spaCy for NER (Named Entity Recognition) and Regex for standard patterns (Emails, Phones).
    """
    if not text:
        return text

    # Regex patterns for Email and basic Phone Numbers
    email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    # A simple regex for phone numbers (e.g., +1-800-555-0199, (800) 555-0199, 800-555-0199)
    phone_pattern = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
    # Basic SSN pattern for US
    ssn_pattern = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')

    # Apply regex redaction first
    redacted_text = email_pattern.sub('[EMAIL REDACTED]', text)
    redacted_text = phone_pattern.sub('[PHONE REDACTED]', redacted_text)
    redacted_text = ssn_pattern.sub('[SSN REDACTED]', redacted_text)

    # Apply spaCy NER redaction if the model was successfully loaded
    if nlp:
        doc = nlp(redacted_text)
        # We need to replace from the end to the beginning to not mess up character indices
        ents = sorted(doc.ents, key=lambda e: e.start_char, reverse=True)
        
        # Entities we want to redact
        target_labels = {'PERSON', 'ORG', 'GPE'}
        
        for ent in ents:
            if ent.label_ in target_labels:
                start = ent.start_char
                end = ent.end_char
                redacted_text = redacted_text[:start] + f'[{ent.label_} REDACTED]' + redacted_text[end:]

    return redacted_text
