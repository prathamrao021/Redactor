from redactor import redact_phones
import argparse
import sys
import spacy
import re
import pyap
import os
import glob


def test_redact_phones():
    data = "John Doe has a phone number of 123-456-7890."
    
    nlp = spacy.load("en_core_web_trf")
    
    redacted_result = redact_phones(data, 'stderr', 'Given Input')

    doc = nlp(data)
    
    assert redacted_result == "John Doe has a phone number of█████████████."
    