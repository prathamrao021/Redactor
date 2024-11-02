from redactor import redact_addresses
import argparse
import sys
import spacy
import re
import pyap
import os
import glob


def test_redact_addresses():
    data = """John Smith was excited to move into his new home at 123 Maple Street, Springfield, IL 62704. He had spent months searching for the perfect place and finally found it. His friend, Jane Doe, lived nearby at 456 Oak Avenue, Springfield, IL 62705, and they planned to meet up often. John's office was located at 789 Pine Road, Suite 101, Springfield, IL 62706, just a short drive from his new house."""
    
    nlp = spacy.load("en_core_web_trf")
    
    redacted_result = redact_addresses(nlp, data, 'stderr', 'Given Input')

    doc = nlp(data)
    
    assert redacted_result == """John Smith was excited to move into his new home at ███████████████████████████████████████. He had spent months searching for the perfect place and finally found it. His friend, Jane Doe, lived nearby at █████████████████████████████████████, and they planned to meet up often. John's office was located at ███████████████████████████████████████████████, just a short drive from his new house."""