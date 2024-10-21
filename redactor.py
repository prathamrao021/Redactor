import argparse
import sys
import spacy
import re
import pyap
from spacy.matcher import Matcher
import os
import glob

def get_file_vector(input):
    matching_files = glob.glob(input)
    return matching_files

def handling_multiple_files(nlp, files, name_flag, date_flag, phones_flag, address_flag, concept, output_dir, stats):
    
    for f in files:
        data = get_data(f)
        if name_flag:
            output_data = redact_names(nlp, data, stats, f)
        if date_flag:
            output_data = redact_dates(nlp, output_data, stats, f)
        if phones_flag:
            output_data = redact_phones(output_data, stats, f)
        if address_flag:
            output_data = redact_addresses(nlp, output_data, stats, f) 
        # if concept:
        #     output_data = redact_concept(nlp, output_data, concept, stats, f)
        if os.path.exists(output_dir) == False:
            os.makedirs(output_dir)
        fileName = f"{output_dir}{f.split('/')[-1]}.censored"
        with open(fileName, "w") as file:
            file.write(output_data)
        
               
  
  
def get_data(input):
    data = ''
    with open(f"{input}", "r") as f:
        data = f.read()
    return data




def redact_names(nlp, data, stats, filename):
    redacted_char = '\u2588'
    
    doc = nlp(data)
    
    mails = list(re.finditer(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", data))
    
    redacted_data = data
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            redacted_data = redacted_data.replace(ent.text, redacted_char*len(ent.text))
            if stats == 'stderr':
                print(f"{filename}|PERSON|{ent.text}|{ent.start_char}|{ent.end_char}", file=sys.stderr)
            elif stats == 'stdout':
                print(f"{filename}|PERSON|{ent.text}|{ent.start_char}|{ent.end_char}", file=sys.stdout)
    
    for mail in mails:
        redacted_data = redacted_data.replace(mail.group(), redacted_char*len(mail.group()))
        if stats == 'stderr':
            print(f"{filename}|EMAIL|{mail.group()}|{mail.start()}|{mail.end()}", file=sys.stderr)
        elif stats == 'stdout':
            print(f"{filename}|EMAIL|{mail.group()}|{mail.start()}|{mail.end()}")
    return redacted_data




def redact_dates(nlp, data, stats, filename):
    redacted_char = '\u2588'
    
    doc = nlp(data)
    
    redacted_data = data
    for ent in doc.ents:
        if ent.label_ == "DATE":
            redacted_data = redacted_data.replace(ent.text, redacted_char*len(ent.text))
            if stats == 'stderr':
                print(f"{filename}|DATE|{ent.text}|{ent.start_char}|{ent.end_char}", file=sys.stderr)
            elif stats == 'stdout':
                print(f"{filename}|DATE|{ent.text}|{ent.start_char}|{ent.end_char}")
    return redacted_data





def redact_phones(data, stats, filename):
    redacted_char = '\u2588'
    phones = list(re.finditer(r'\b(?:\+?(\d{1,3})?[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\b', data))
    redacted_data = data
    for phone in phones:
        redacted_data = redacted_data.replace(phone.group(), redacted_char*len(phone.group()))
        if stats == 'stderr':
            print(f"{filename}|PHONE|{phone.group()}|{phone.start()}|{phone.end()}", file=sys.stderr)
        elif stats == 'stdout':
            print(f"{filename}|PHONE|{phone.group()}|{phone.start()}|{phone.end()}")
    return redacted_data





def redact_addresses(nlp, data, stats, filename):
    redacted_char = '\u2588'
    addresses = pyap.parse(data, country='US')
    redacted_data = data

    for address in addresses:
        redacted_data = redacted_data.replace(address.full_address, redacted_char*len(address.full_address))
        if stats == 'stderr':
            print(f"{filename}|ADDRESS|{address.full_address}|{address.start()}|{address.end()}", file=sys.stderr)
        elif stats == 'stdout':
            print(f"{filename}|ADDRESS|{address.full_address}|{address.start()}|{address.end()}")
            
    
    doc = nlp(data)
    
    for ent in doc.ents:
        if ent.label_ == "LOC" or ent.label_ == "GPE" or ent.label_ == "FAC":
            redacted_data = redacted_data.replace(ent.text, redacted_char*len(ent.text))
            if stats == 'stderr':
                print(f"{filename}|ADDRESS|{ent.text}|{ent.start_char}|{ent.end_char}", file=sys.stderr)
            elif stats == 'stdout':
                print(f"{filename}|ADDRESS|{ent.text}|{ent.start_char}|{ent.end_char}")

    
    # matcher = Matcher(nlp.vocab)
    
    # pattern = [
    # {"LIKE_NUM": True},
    # {"IS_ALPHA": True, "OP": "+"},
    # {"LOWER": {"IN": ["street", "st", "avenue", "ave", "boulevard", "blvd", "road", "rd", "lane", "ln", "drive", "dr", "court", "ct", "parkway", "pkwy", "place", "pl"]}},
    # {"IS_PUNCT": True, "OP": "?"},
    # {"IS_ALPHA": True, "OP": "+"},
    # {"IS_ALPHA": True},
    # ]
    
    # matcher.add("ADDRESS_PATTERN", [pattern])
    
    # doc = nlp(data)
    
    # matches = matcher(doc)
    
    # for match_id, start, end in matches:
    #     redacted_data = redacted_data.replace(doc[start:end].text, redacted_char*len(doc[start:end].text))
    #     if stats == 'stderr':
    #         print(f"{filename}|ADDRESS|{doc[start:end].text}|{start}|{end}", file=sys.stderr)
    #     elif stats == 'stdout':
    #         print(f"{filename}|ADDRESS|{doc[start:end].text}|{start}|{end}")
    
    # address_pattern = re.finditer(
    # r'\d{1,5}\s\w+\s(?:Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Lane|Ln|Drive|Dr|Court|Ct|Parkway|Pkwy|Place|Pl)\,?\s[A-Za-z\s]+\,?\s[A-Za-z\s]+\,?\s(?:[A-Za-z]{2,})?', data)
    return redacted_data





def redact_concept(nlp, data, concept, stats, filename):
    pass




if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--input", type=str, help="Input file")
    
    parser.add_argument("--names", action="store_true", help="Redact names")
    parser.add_argument("--dates", action="store_true", help="Redact dates")
    parser.add_argument("--phones", action="store_true", help="Redact phone numbers")
    parser.add_argument("--addresses", action="store_true", help="Redact addresses")
    
    parser.add_argument("--concept",type=str, help="Redact a specific concept")
    
    parser.add_argument("--output", type=str, help="Output file")
    
    parser.add_argument("--stats", choices=['stderr','stdout'], help="Print statistics")
    args = parser.parse_args()
    
    #calling spacy model
    nlp = spacy.load("en_core_web_trf")
    
    #get all the files in a vector
    all_files = get_file_vector(args.input)
    
    #call functions
    handling_multiple_files(nlp, all_files, args.names, args.dates, args.phones, args.addresses, args.concept, args.output, args.stats)
    