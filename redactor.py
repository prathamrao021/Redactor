import argparse
import sys
import spacy
import re
import pyap
import os
import glob
import requests
from names_dataset import NameDataset
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex
from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt_tab')

def get_file_vector(input):
    matching_files = glob.glob(input)
    return matching_files

def custom_tokenizer(nlp):
    infix_re = compile_infix_regex(nlp.Defaults.infixes + [r'[_@:.]'])
    return Tokenizer(nlp.vocab, infix_finditer=infix_re.finditer)

def get_data(input):
    data = ''
    with open(f"{input}", "r") as f:
        data = f.read()
    return data


def handling_multiple_files(nlp, files, name_flag, date_flag, phones_flag, address_flag, concept, output_dir, stats):
    if stats != 'stderr' and stats != 'stdout':
        if os.path.exists(stats):
                os.remove(stats)
    for f in files:
        output_data=get_data(f)
        data = get_data(f)
        if name_flag:
            output_data = redact_names(nlp, data, stats, f)
        if date_flag:
            output_data = redact_dates(nlp, output_data, stats, f)
        if phones_flag:
            output_data = redact_phones(output_data, stats, f)
        if address_flag:
            output_data = redact_addresses(nlp, output_data, stats, f) 
        if concept:
            concept_words = get_similar_words(concept)
            output_data = redact_concepts(nlp, output_data, concept_words, concept, stats, f)
        if os.path.exists(output_dir) == False:
            os.makedirs(output_dir)
        
        fileName = f"{output_dir}{f.split('/')[-1]}.censored"
        with open(fileName, "w") as file:
            file.write(output_data)
            


def redact_names(nlp, data, stats, filename):
    redacted_char = '\u2588'
    
    doc = nlp(data)
    
    # mails = list(re.finditer(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data))
    # name_mail =[]
    
    # for mail in mails:
    #     name_mail.append([mail.group().split('@')[0],mail.start(),mail.end()])
    
    emails = list(re.finditer(r'\b([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b', data))
    
    
    redacted_data = data
    nd = NameDataset()
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            redacted_data = redacted_data.replace(ent.text, redacted_char*len(ent.text))
            
            stats_data = f"{filename}|PERSON|{ent.text}|{ent.start_char}|{ent.end_char}"
            
            if stats == 'stderr':
                print(stats_data, file=sys.stderr)
            elif stats == 'stdout':
                print(stats_data)
            else:
                with open(stats, "a") as f:
                    f.write(stats_data)
                    f.write("\n")
    
    for ent in doc.ents:
        search = nd.search(ent.text)
        if search['first_name'] is None and search['last_name'] is None:
            continue
        if search['first_name'] is not None:
            for probs in search["first_name"]["country"].values():
                if probs > 0.3:
                    redacted_data = redacted_data.replace(ent.text, redacted_char*len(ent.text))
            
                    stats_data = f"{filename}|PERSON|{ent.text}|{ent.start_char}|{ent.end_char}"
                    
                    if stats == 'stderr':
                        print(stats_data, file=sys.stderr)
                    elif stats == 'stdout':
                        print(stats_data)
                    else:
                        with open(stats, "a") as f:
                            f.write(stats_data)
                            f.write("\n")
        if search['last_name'] is not None:
            for probs in search["last_name"]["country"].values():
                if probs > 0.3:
                    redacted_data = redacted_data.replace(ent.text, redacted_char*len(ent.text))
                    
                    stats_data = f"{filename}|PERSON|{ent.text}|{ent.start_char}|{ent.end_char}"
                    
                    if stats == 'stderr':
                        print(stats_data, file=sys.stderr)
                    elif stats == 'stdout':
                        print(stats_data)
                    else:
                        with open(stats, "a") as f:
                            f.write(stats_data)
                            f.write("\n")
    
    for email in emails:
        username, domain = email.groups()
        start, end = email.span(1)
        
        redacted_data = redacted_data[:start] + (redacted_char * len(username)) + redacted_data[end:]
        
        stats_data = f"{filename}|EMAIL_USERNAME|{username}|{start}|{end}"
        
        if stats == 'stderr':
            print(stats_data, file=sys.stderr)
        elif stats == 'stdout':
            print(stats_data)
        else:
            with open(stats, "a") as f:
                f.write(stats_data)
                f.write("\n")    
    return redacted_data


def redact_dates(nlp, data, stats, filename):
    redacted_char = '\u2588'

    doc = nlp(data)

    redacted_data = list(data)
    for ent in reversed(doc.ents):
        if ent.label_ == "DATE":
            start, end = ent.start_char, ent.end_char
            redacted_data[start:end] = redacted_char * (end - start)
            
            stats_data = f"{filename}|DATE|{ent.text}|{start}|{end}"
            
            if stats == 'stderr':
                print(stats_data, file=sys.stderr)
            elif stats == 'stdout':
                print(stats_data)
            else:
                with open(stats, "a") as f:
                    f.write(stats_data)
                    f.write("\n")
                    

    return ''.join(redacted_data)


def redact_phones(data, stats, filename):
    redacted_char = '\u2588'
    old_pattern = r'\b(?:\+?(\d{1,3})?[-.\s]?)?\(?(\d{2,3})\)?[-.\s]?(\d{3,4})[-.\s]?(\d{4})\b'

    phones = list(re.finditer(old_pattern, data))
    redacted_data = data
    for phone in phones:
        
        redacted_data = redacted_data.replace(phone.group(), redacted_char*len(phone.group()))
        
        stats_data = f"{filename}|PHONE|{phone.group()}|{phone.start()}|{phone.end()}"
        
        if stats == 'stderr':
            print(stats_data, file=sys.stderr)
        elif stats == 'stdout':
            print(stats_data)
        else:
            with open(stats, "a") as f:
                f.write(stats_data)
                f.write("\n")

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

            stats_data = f"{filename}|ADDRESS|{address.full_address}|{start}|{end}"
            
            if stats == 'stderr':
                print(stats_data, file=sys.stderr)
            elif stats == 'stdout':
                print(stats_data)
            else:
                with open(stats, "a") as f:
                    f.write(stats_data)
                    f.write("\n")
                    
    redacted_data = ''.join(redacted_data)
    doc = nlp(data)
    
    for ent in doc.ents:
        if ent.label_ == "LOC" or ent.label_ == "GPE" or ent.label_ == "FAC":
            
            redacted_data = redacted_data.replace(ent.text, redacted_char*len(ent.text))
            
            stats_data = f"{filename}|ADDRESS|{ent.text}|{ent.start_char}|{ent.end_char}"
            
            if stats == 'stderr':
                print(stats_data, file=sys.stderr)
            elif stats == 'stdout':
                print(stats_data)
            else:
                with open(stats, "a") as f:
                    f.write(stats_data)
                    f.write("\n")
                    
    return redacted_data


def get_similar_words(concept):
    synonyms = []
    for con in concept:
        response = requests.get(f"https://api.datamuse.com/words?rel_syn={con}")
        for doc in response.json():
            synonyms.append(doc['word'])
        synonyms.append(con)
    return synonyms


def redact_concepts(nlp, data, concept_words, concept, stats, filename):
    redacted_char = '\u2588'
    
    doc = nlp(data)
    redacted_data = data
    print(doc)
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in concept_words:
                redacted_data = redacted_data.replace(sent.text, redacted_char*len(sent.text))
                
                stats_data = f"{filename}|CONCEPT|{sent.text}|{sent.start_char}|{sent.end_char}"
                if stats == 'stderr':
                    print(stats_data, file=sys.stderr)
                elif stats == 'stdout':
                    print(stats_data)
                else:
                    with open(stats, "a") as f:
                        f.write(stats_data)
                        f.write("\n")
    
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    redacted_text = []
    
    for sent in sent_tokenize(data):
        
        result = classifier(sent, candidate_labels=concept)
        if any(result['labels'][i] in concept and result['scores'][i] > 0.33 for i in range(len(result['labels']))):
            redacted_text.append("█" * len(sent))
            start_char = data.find(sent)
            end_char = start_char + len(sent)
            stats_data = f"{filename}|CONCEPT|{sent}|{start_char}|{end_char}"
            if stats == 'stderr':
                print(stats_data, file=sys.stderr)
            elif stats == 'stdout':
                print(stats_data)
            else:
                with open(stats, "a") as f:
                    f.write(stats_data)
                    f.write("\n")
        else:
            redacted_text.append(sent)
    redacted_data = " ".join(redacted_text)
    
    return redacted_data

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--input", type=str, help="Input file")
    
    parser.add_argument("--names", action="store_true", help="Redact names")
    parser.add_argument("--dates", action="store_true", help="Redact dates")
    parser.add_argument("--phones", action="store_true", help="Redact phone numbers")
    parser.add_argument("--addresses", action="store_true", help="Redact addresses")
    
    parser.add_argument("--concept",type=str, nargs='+', help="Redact a specific concept")
    
    parser.add_argument("--output", type=str, help="Output file")
    
    parser.add_argument("--stats", type=str, help="Print statistics")
    args = parser.parse_args()
    
    nlp = spacy.load("en_core_web_trf")
    nlp.tokenizer = custom_tokenizer(nlp)
    
    all_files = get_file_vector(args.input)
    
    handling_multiple_files(nlp, all_files, args.names, args.dates, args.phones, args.addresses, args.concept, args.output, args.stats)