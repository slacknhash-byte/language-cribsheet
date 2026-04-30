# Created 29/04/2026
# The original idea for Flubb's Reference Sheets was that
# there would be a range one could print or purchase.
# In addition to the table there would be a title graphic, and
# relevant information in the header and footer of the document
# to assist with identification and filing.
from utils.headers import get_language

def document_title(lang, word_type):

    return f"Flubb's Reference Sheets: {get_language(lang)} {word_type.capitalize()}s"

def build_codename(lang, word_type):
    # Created 30/04/2026. Each reference sheet should have an identifying
    # codename at the bottom for ease of filing.
    lexical_elements = {
        'noun': 'NOUN',
        'verb': 'VERB',
        'adjective': 'ADJ',
        'adverb': 'ADV',
        'preposition': 'PREP',
        'determiner': 'DET'
        }

    return f"{lang.upper()}-{lexical_elements[word_type].upper()}"
