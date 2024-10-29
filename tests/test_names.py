from redactor import redact_names
import argparse
import sys
import spacy
import re
import pyap
import os
import glob


def test_redact_names():
    data = "John Doe is a person. His email is john.doe@gmail.com."
    
    nlp = spacy.load("en_core_web_trf")
    
    redacted_result = redact_names(nlp, data, 'stderr', 'Given Input')
    print(redacted_result)
    doc = nlp(data)
    
    assert doc.ents[0].text == 'John Doe'
    assert doc.ents[0].label_ == 'PERSON'
    assert redacted_result == "████████ is a person. His email is ████████@gmail.com."
    
    