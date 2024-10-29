# import requests

# def find_synonyms(word):
#     response = requests.get(f"https://api.datamuse.com/words?rel_syn={word}")
#     synonyms = [doc['word'] for doc in response.json()]
#     return synonyms

# text = "Your text here..."

# # split the text into words
# words = text.split()


# synonyms = find_synonyms("house")
# print(f"The synonyms for 'house' are: {synonyms}")


# ----------------------

# import spacy

# def find_similarity(text, concept='house'):
#     # Load the spaCy language model, assuming you'd like to use a transformer-based model for improved accuracy
#     model = spacy.load('en_core_web_trf')

#     # Process the full text with the model
#     doc = model(text)

#     # Process the concept word with the model to get its vector
#     concept_token = model(concept)

#     redacted_text = []
    
#     # Iterate over sentences in the document
#     for sent in doc.sents:
#         # Check similarity (this should compare vector of concept to the average vector of the sentence)
#         if concept_token.similarity(sent) > 0.5:  # Adjust threshold accordingly
#             print("Redacting")
#             redacted_text.append("[REDACTED]")
#         else:
#             redacted_text.append(sent.text)
    
#     return " ".join(redacted_text)

# # Example usage of the function
# text = """Jack pursued his journey. He walked on till after sunset, when to his great joy, he espied a large mansion. A plain-looking woman was at the door: he accosted her, begging she would give him a morsel of bread and a night’s lodging. She expressed the greatest surprise, and said it was quite uncommon to see a human being near their house; for it was well known that her husband was a powerful giant, who would never eat anything but human flesh, if he could possibly get it; that he would walk fifty miles to procure it, usually being out the whole day for that purpose.
# This account greatly terrified Jack, but still he hoped to elude the giant, and therefore he again entreated the woman to take him in for one night only, and hide him where she thought proper. She at last suffered herself to be persuaded, for she was of a compassionate and generous disposition, and took him into the house. First, they entered a fine large hall, magnificently furnished; they then passed through several spacious rooms, in the same style of grandeur; but all appeared forsaken and desolate.
# A long gallery came next; it was very dark – just light enough to show that, instead of a wall on one side, there was a grating of iron which parted off a dismal dungeon, from whence issued the groans of those victims whom the cruel giant reserved in confinement for his own voracious appetite.
# Poor Jack was half dead with fear, and would have given the world to have been with his mother again, for he now began to doubt if he should ever see her more; he even mistrusted the good woman, and thought she had let him into the house for no other purpose than to lock him up among the unfortunate people in the dungeon.
# However, she bade Jack sit down, and gave him plenty to eat and drink; and he, not seeing anything to make him uncomfortable, soon forgot his fear and was just beginning to enjoy himself, when he was startled by a loud knocking at the outer door, which made the whole house shake."""
# redacted = find_similarity(text)
# print(redacted)
# --------------------------------



# import spacy
# from spacy.tokens import Doc, Span, Token
# from spacy.language import Language

# Token.set_extension('is_redacted', default=False, force=True)

# @Language.component('redact_names')
# def redact_names(doc):
#     redacted_char = '█'
#     redacted_data = doc.text
#     for ent in doc.ents:
#         if ent.label_ == "PERSON":
#             redacted_data = redacted_data.replace(ent.text, redacted_char*len(ent.text))
#             # for token in ent:
#             #     token._.is_redacted = True
#     return doc

# @Language.component('redact_dates')
# def redact_dates(doc):
#     redacted_char = '█'
#     for ent in doc.ents:
#         if ent.label_ == "DATE":
#             for token in ent:
#                 token._.is_redacted = True
#     return doc

# def construct_redacted_text(doc):
#     return ''.join([token._.is_redacted * len(token.text) * '█' if token._.is_redacted else token.text_with_ws for token in doc])

# nlp = spacy.load('en_core_web_trf')

# nlp.add_pipe('redact_names', after='ner')
# nlp.add_pipe('redact_dates', after='redact_names')


# text = "John Doe was born on January 1, 1990. He met Emily in Paris on March 23, 2020."


# doc = nlp(text)


# redacted_text = construct_redacted_text(doc)
# print(redacted_text)


#------------------------------
# import spacy
# from gensim import corpora, models

# # Load the spaCy model
# nlp = spacy.load('en_core_web_trf')

# # Example text data
# text = """Jack pursued his journey. He walked on till after sunset, when to his great joy, he espied a large mansion. A plain-looking woman was at the door: he accosted her, begging she would give him a morsel of bread and a night’s lodging. She expressed the greatest surprise, and said it was quite uncommon to see a human being near their house; for it was well known that her husband was a powerful giant, who would never eat anything but human flesh, if he could possibly get it; that he would walk fifty miles to procure it, usually being out the whole day for that purpose.
# This account greatly terrified Jack, but still he hoped to elude the giant, and therefore he again entreated the woman to take him in for one night only, and hide him where she thought proper. She at last suffered herself to be persuaded, for she was of a compassionate and generous disposition, and took him into the house. First, they entered a fine large hall, magnificently furnished; they then passed through several spacious rooms, in the same style of grandeur; but all appeared forsaken and desolate.
# A long gallery came next; it was very dark – just light enough to show that, instead of a wall on one side, there was a grating of iron which parted off a dismal dungeon, from whence issued the groans of those victims whom the cruel giant reserved in confinement for his own voracious appetite.
# Poor Jack was half dead with fear, and would have given the world to have been with his mother again, for he now began to doubt if he should ever see her more; he even mistrusted the good woman, and thought she had let him into the house for no other purpose than to lock him up among the unfortunate people in the dungeon.
# However, she bade Jack sit down, and gave him plenty to eat and drink; and he, not seeing anything to make him uncomfortable, soon forgot his fear and was just beginning to enjoy himself, when he was startled by a loud knocking at the outer door, which made the whole house shake."""

# # Process the text with spaCy
# doc = nlp(text)

# # Tokenize and remove stopwords and punctuation
# tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

# # Create a dictionary and corpus for topic modeling
# dictionary = corpora.Dictionary([tokens])
# corpus = [dictionary.doc2bow(tokens)]

# # Perform LDA topic modeling
# lda_model = models.LdaModel(corpus, num_topics=2, id2word=dictionary, passes=15)

# # Print topics
# topics = lda_model.print_topics(num_topics=2, num_words=4)
# for topic in topics:
#     print(topic)

#-------------------------------------
# import spacy
# from gensim import corpora, models
# from gensim.models import CoherenceModel
# import numpy as np

# # Load spaCy model
# nlp = spacy.load('en_core_web_md')

# # Text data
# text = """Jack pursued his journey. He walked on till after sunset, when to his great joy, he espied a large mansion. A plain-looking woman was at the door: he accosted her, begging she would give him a morsel of bread and a night’s lodging. She expressed the greatest surprise, and said it was quite uncommon to see a human being near their house; for it was well known that her husband was a powerful giant, who would never eat anything but human flesh, if he could possibly get it; that he would walk fifty miles to procure it, usually being out the whole day for that purpose.
# This account greatly terrified Jack, but still he hoped to elude the giant, and therefore he again entreated the woman to take him in for one night only, and hide him where she thought proper. She at last suffered herself to be persuaded, for she was of a compassionate and generous disposition, and took him into the house. First, they entered a fine large hall, magnificently furnished; they then passed through several spacious rooms, in the same style of grandeur; but all appeared forsaken and desolate.
# A long gallery came next; it was very dark – just light enough to show that, instead of a wall on one side, there was a grating of iron which parted off a dismal dungeon, from whence issued the groans of those victims whom the cruel giant reserved in confinement for his own voracious appetite.
# Poor Jack was half dead with fear, and would have given the world to have been with his mother again, for he now began to doubt if he should ever see her more; he even mistrusted the good woman, and thought she had let him into the house for no other purpose than to lock him up among the unfortunate people in the dungeon.
# However, she bade Jack sit down, and gave him plenty to eat and drink; and he, not seeing anything to make him uncomfortable, soon forgot his fear and was just beginning to enjoy himself, when he was startled by a loud knocking at the outer door, which made the whole house shake."""

# # Process the document with spaCy
# doc = nlp(text)

# # Keywords related to concept "house"
# keywords = ["house", "mansion", "home", "residence", "abode"]

# # Collect sentences that have a high semantic similarity to the house keywords
# candidate_sentences = []
# for sent in doc.sents:
#     if any(token.text.lower() in keywords for token in sent):
#         candidate_sentences.append(sent.text)
#     else:
#         # Calculate sentence similarity with each keyword and consider it if it's above a threshold
#         sent_vector = sent.vector
#         for keyword in keywords:
#             keyword_vector = nlp(keyword).vector
#             similarity = np.dot(sent_vector, keyword_vector) / (np.linalg.norm(sent_vector) * np.linalg.norm(keyword_vector))
#             if similarity > 0.5:  # Threshold, can be adjusted
#                 candidate_sentences.append(sent.text)
#                 break

# # Tokenize and prepare for LDA
# texts = [[token.lemma_ for token in nlp(sent) if not token.is_stop and not token.is_punct] for sent in candidate_sentences]
# dictionary = corpora.Dictionary(texts)
# corpus = [dictionary.doc2bow(text) for text in texts]

# # Apply LDA model
# lda_model = models.LdaModel(corpus, num_topics=2, id2word=dictionary, passes=15)

# # Display topics
# topics = lda_model.print_topics(num_topics=2, num_words=5)
# for topic in topics:
#     print(topic)

#--------------------------------
from redactor import redact_concepts, get_similar_words, redact_addresses
import argparse
import sys
import spacy
import re
import pyap
import os
import glob

# def test_redact_dates():
#     data = """John Smith was excited to move into his new home at 123 Maple Street, Springfield, IL 62704. He had spent months searching for the perfect place and finally found it. His friend, Jane Doe, lived nearby at 456 Oak Avenue, Springfield, IL 62705, and they planned to meet up often. John's office was located at 789 Pine Road, Suite 101, Springfield, IL 62706, just a short drive from his new house.

#     On weekends, John liked to visit his favorite coffee shop, Brewed Awakenings, at 321 Elm Street, Springfield, IL 62707. He often met his colleague, Michael Johnson, there. Michael's address was 654 Birch Lane, Springfield, IL 62708, and they carpooled to work together. John's gym, Fit for Life, was at 987 Cedar Boulevard, Springfield, IL 62709, where he worked out every morning.

#     John's parents lived in a nearby town at 111 Maple Street, Rivertown, IL 62001. He visited them every Sunday for dinner. His sister, Emily Davis, lived at 222 Oak Avenue, Rivertown, IL 62002, and they often met up at their parents' house. John's best friend, Robert Brown, had recently moved to 333 Pine Road, Rivertown, IL 62003, and they planned to catch up soon.

#     For his medical needs, John visited Dr. Lisa White at the Springfield Medical Center, located at 444 Elm Street, Springfield, IL 62710. His dentist, Dr. David Green, had an office at 555 Birch Lane, Springfield, IL 62711. John also had regular appointments with his chiropractor, Dr. James Gray, whose clinic was at 666 Cedar Boulevard, Springfield, IL 62712.

#     John's favorite restaurant, The Gourmet Kitchen, was at 777 Maple Street, Springfield, IL 62713. He often dined there with his girlfriend, Rachel Yellow, who lived at 888 Oak Avenue, Springfield, IL 62714. They enjoyed trying new dishes and spending time together.

#     John's plumber, Mike Purple, had his office at 999 Pine Road, Springfield, IL 62715. Whenever John had plumbing issues, he knew he could rely on Mike to fix them promptly. His electrician, Tom Pink, was based at 1010 Elm Street, Springfield, IL 62716, and had helped John with several electrical projects in his new home.

#     As John settled into his new life in Springfield, he felt grateful for the support of his friends and family. He looked forward to creating many happy memories in his new home at 123 Maple Street, Springfield, IL 62704."""
    
#     nlp = spacy.load("en_core_web_trf")
    
    
#     output_data=redact_addresses(nlp, data, "stderr", "Given Input")
#     print(output_data)
# test_redact_dates()

# def test_redact_concepts():
#     data = """Jack pursued his journey. He walked on till after sunset, when to his great joy, he espied a large mansion. A plain-looking woman was at the door: he accosted her, begging she would give him a morsel of bread and a night’s lodging. She expressed the greatest surprise, and said it was quite uncommon to see a human being near their house; for it was well known that her husband was a powerful giant, who would never eat anything but human flesh, if he could possibly get it; that he would walk fifty miles to procure it, usually being out the whole day for that purpose.
#     This account greatly terrified Jack, but still he hoped to elude the giant, and therefore he again entreated the woman to take him in for one night only, and hide him where she thought proper. She at last suffered herself to be persuaded, for she was of a compassionate and generous disposition, and took him into the house. First, they entered a fine large hall, magnificently furnished; they then passed through several spacious rooms, in the same style of grandeur; but all appeared forsaken and desolate.
#     A long gallery came next; it was very dark – just light enough to show that, instead of a wall on one side, there was a grating of iron which parted off a dismal dungeon, from whence issued the groans of those victims whom the cruel giant reserved in confinement for his own voracious appetite.
#     Poor Jack was half dead with fear, and would have given the world to have been with his mother again, for he now began to doubt if he should ever see her more; he even mistrusted the good woman, and thought she had let him into the house for no other purpose than to lock him up among the unfortunate people in the dungeon.
#     However, she bade Jack sit down, and gave him plenty to eat and drink; and he, not seeing anything to make him uncomfortable, soon forgot his fear and was just beginning to enjoy himself, when he was startled by a loud knocking at the outer door, which made the whole house shake."""
#     concept=['house']
    
#     nlp = spacy.load("en_core_web_trf")
    
#     concept_words = get_similar_words(concept)
#     output_data = redact_concepts(nlp, data, concept_words, 'stderr', 'Given Input')
    
#     print(output_data)
    
#     with open("output.txt", "w") as f:
#         f.write(output_data)
# test_redact_concepts()