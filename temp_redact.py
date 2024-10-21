import argparse
import sys
import spacy
import re
import os

def get_data():
    if os.path.exists("stats.txt"):
        os.remove("stats.txt")
    with open("demo_files/2.", "r") as f:
        data = f.read()
    return data




def redact_names(nlp, data):
    redacted_char = '\u2588'
    
    doc = nlp(data)
    
    mails = list(re.finditer(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", data))
    
    redacted_data = data
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            redacted_data = redacted_data.replace(ent.text, redacted_char*len(ent.text))
            with open("stats.txt","a") as file:
                file.write(f"PERSON|{ent.text}|{ent.start_char}|{ent.end_char}\n")
    
    # for mail in mails:
    #     redacted_data = redacted_data.replace(mail.group(), redacted_char*len(mail.group()))
    #     with open("stats.txt","a") as file:
    #         file.write(f"EMAIL|{mail.group()}|{mail.start()}|{mail.end()}\n")
    return redacted_data




def redact_dates(nlp, data):
    redacted_char = '\u2588'
    
    doc = nlp(data)
    
    redacted_data = data
    for ent in doc.ents:
        if ent.label_ == "DATE":
            redacted_data = redacted_data.replace(ent.text, redacted_char*len(ent.text))
            with open("stats.txt","a") as file:
                file.write(f"DATE|{ent.text}|{ent.start_char}|{ent.end_char}\n")
    return redacted_data




def redact_phones(data):
    redacted_char = '\u2588'
    phones = list(re.finditer(r'\b(?:\+?(\d{1,3})?[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\b', data))
    redacted_data = data
    for phone in phones:
        redacted_data = redacted_data.replace(phone.group(), redacted_char*len(phone.group()))
        with open("stats.txt","a") as file:
            file.write(f"PHONE|{phone.group()}|{phone.start()}|{phone.end()}\n")
    return redacted_data




def redact_addresses(nlp, data):
    redacted_char = '\u2588'
    
    doc = nlp(data)
    
    redacted_data = data
    for ent in doc.ents:
        if ent.label_ == "LOC" or ent.label_ == "GPE" or ent.label_ == "FAC":
            redacted_data = redacted_data.replace(ent.text, redacted_char*len(ent.text))
            with open("stats.txt","a") as file:
                file.write(f"ADDRESS|{ent.text}|{ent.start_char}|{ent.end_char}\n")
    return redacted_data




def write_file(redacted_data):
    with open("output.txt", "w") as f:
        f.write(redacted_data)

if __name__ == "__main__":
    
    data = get_data()
    nlp = spacy.load("en_core_web_trf")
    
    redacted_name = redact_names(nlp,data)
    # redacted_dates = redact_dates(nlp,data)
    # redacted_phones = redact_phones(redacted_dates)
    # redacted_addresses = redact_addresses(nlp,redacted_phones)
    
    write_file(redacted_name)