from redactor import redact_dates
import argparse
import sys
import spacy
import re
import pyap
import os
import glob


def test_redact_dates():
    data = "John Doe was born on 12/12/1990."
    
    nlp = spacy.load("en_core_web_trf")
    
    redacted_result = redact_dates(nlp, data, 'stderr', 'Given Input')

    doc = nlp(data)
    
    assert redacted_result == "John Doe was born on ██████████."
    
    