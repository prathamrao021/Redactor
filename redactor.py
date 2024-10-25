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
        # if name_flag:
        #     output_data = redact_names(nlp, data, stats, f)
        # if date_flag:
        #     output_data = redact_dates(nlp, data, stats, f)
        # if phones_flag:
        #     output_data = redact_phones(data, stats, f)
        # if address_flag:
        #     output_data = redact_addresses(nlp, data, stats, f) 
        if concept:
            concept_words = get_similar_words(concept)
            # print(concept_words)
            output_data = redact_concepts(nlp, data, concept_words, stats, f)
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
    name_mail =[]
    
    for mail in mails:
        name_mail.append([mail.group().split('@')[0],mail.start(),mail.end()])
    redacted_data = data
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            redacted_data = redacted_data.replace(ent.text, redacted_char*len(ent.text))
            if stats == 'stderr':
                print(f"{filename}|PERSON|{ent.text}|{ent.start_char}|{ent.end_char}", file=sys.stderr)
            elif stats == 'stdout':
                print(f"{filename}|PERSON|{ent.text}|{ent.start_char}|{ent.end_char}", file=sys.stdout)

    for mail in name_mail:
        redacted_data = redacted_data.replace(mail[0], redacted_char*len(mail))
        if stats == 'stderr':
            print(f"{filename}|PERSON|{mail[0]}|{mail[1]}|{mail[2]}", file=sys.stderr)
        elif stats == 'stdout':
            print(f"{filename}|PERSON|{mail[0]}|{mail[1]}|{mail[2]}")
    return redacted_data



def redact_dates(nlp, data, stats, filename):
    redacted_char = '\u2588'
    
    doc = nlp(data)
    
    redacted_data = list(data)  # Convert to list for mutable operations
    for ent in reversed(doc.ents):
        if ent.label_ == "DATE":
            start, end = ent.start_char, ent.end_char
            redacted_data[start:end] = redacted_char * (end - start)
            if stats == 'stderr':
                print(f"{filename}|DATE|{ent.text}|{start}|{end}", file=sys.stderr)
            elif stats == 'stdout':
                print(f"{filename}|DATE|{ent.text}|{start}|{end}")

    return ''.join(redacted_data)  # Convert back to string





def redact_phones(data, stats, filename):
    redacted_char = '\u2588'

    phones = list(re.finditer(r'\b(?:\+?(\d{1,3})?[-.\s]?)?\(?(\d{2,3})\)?[-.\s]?(\d{3,4})[-.\s]?(\d{4})\b', data))
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
    redacted_data = list(data)

    for address in addresses:
        pattern = re.escape(address.full_address)
        for match in re.finditer(pattern, data):
            start, end = match.start(), match.end()
            redacted_data[start:end] = redacted_char * (end - start)
            if stats == 'stderr':
                print(f"{filename}|ADDRESS|{address.full_address}|{start}|{end}", file=sys.stderr)
            elif stats == 'stdout':
                print(f"{filename}|ADDRESS|{address.full_address}|{start}|{end}")
            
    redacted_data = ''.join(redacted_data)
    doc = nlp(data)
    
    for ent in doc.ents:
        if ent.label_ == "LOC" or ent.label_ == "GPE" or ent.label_ == "FAC":
            redacted_data = redacted_data.replace(ent.text, redacted_char*len(ent.text))
            if stats == 'stderr':
                print(f"{filename}|ADDRESS|{ent.text}|{ent.start_char}|{ent.end_char}", file=sys.stderr)
            elif stats == 'stdout':
                print(f"{filename}|ADDRESS|{ent.text}|{ent.start_char}|{ent.end_char}")
    
    return redacted_data


def get_similar_words(concept):
    doc = nlp(concept)
    
    similar_words = set([concept])  
    
    for word in nlp.vocab:  
        if word.has_vector and word.is_lower and word.is_alpha:  
            similarity = doc.similarity(nlp(word.text))
            if similarity > 0.5:  
                similar_words.add(word.text)
    
    return similar_words

def redact_concepts(nlp, data, concept_words, stats, filename):
    redacted_char = '\u2588'
    
    doc = nlp(data)
    redacted_data = data
    
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in concept_words:
                redacted_data = redacted_data.replace(sent.text, redacted_char*len(sent.text))
                
                if stats == 'stderr':
                    print(f"{filename}|CONCEPT|{sent.text}|{sent.start_char}|{sent.end_char}", file=sys.stderr)
                elif stats == 'stdout':
                    print(f"{filename}|CONCEPT|{sent.text}|{sent.start_char}|{sent.end_char}")
    
    return redacted_data




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
    