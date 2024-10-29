# CIS6930 Fall 2024 -- Project 1

Name: Pratham Rao

# Project Description
This project is focused on developing a comprehensive text redaction tool that can identify and censor sensitive information from text files. The tool is designed to handle various types of sensitive data, including names, dates, phone numbers, addresses, and specific concepts. The primary goal is to ensure that any personal or sensitive information is effectively redacted to protect privacy and confidentiality.

The tool leverages natural language processing (NLP) techniques and libraries such as Spacy to accurately detect and redact the specified types of information. Users can specify the types of data they want to redact through command-line arguments, making the tool flexible and customizable for different use cases.

Key features of the project include:

- Name Redaction: Identifies and censors personal names from the text.
- Date Redaction: Detects and redacts dates in various formats.
- Phone Number Redaction: Recognizes and censors phone numbers, including international formats.
- Address Redaction: Identifies and redacts physical addresses.
- Concept Redaction: Allows users to specify a concept (e.g., "house") and censors related terms and synonyms.

The tool also provides options for outputting the redacted text to a specified directory and generating statistics about the redaction process, which can be directed to either stderr or stdout.

Overall, this project aims to create a robust and efficient text redaction solution that can be easily integrated into various workflows to enhance data privacy and security.

# How to install
1. Clone the Repository: First, clone the repository to your local machine using the following command:
```bash
# Clone the repository
git clone https://github.com/prathamrao021/cis6930fa24-project1
# Change Directory to the folder
cd cis6930fa24-project1
```

2. Install Pipenv: Ensure you have Pipenv installed. If not, you can install it using:
```bash
# Install pipenv
pip install pipenv
```

3. Install Dependencies: Navigate to the project directory and install the dependencies listed in the `Pipfile`:
```bash
pip install
```

4. Download Spacy Model: Download the required Spacy model:
```bash
# This will download the model
pipenv run python -m spacy download en_core_web_trf
```

# How to run
1. `--input`:

- Description: Specifies the directory containing the input text files to be redacted.
- Usage: `--input 'path/to/input/files'`
- Example: `--input 'demo_files/concept_redact'`

2. `--names`:

- Description: A flag to enable the redaction of personal names from the text.
- Usage: `--names`
- Example: `--names`

3.  `--dates`:

- Description: A flag to enable the redaction of dates in various formats from the text.
- Usage: `--dates`
- Example: `--dates`

4. `--phones`:

- Description: A flag to enable the redaction of phone numbers, including international formats, from the text.
- Usage: `--phones`
- Example: `--phones`

5. `--address`:

- Description: A flag to enable the redaction of physical addresses from the text.
- Usage: `--address`
- Example: `--address`

6. `--concept`:

- Description: Specifies a concept (e.g., "house") and enables the redaction of related terms and synonyms from the text.
- Usage: `--concept 'kids'`
- Example: `--concept 'house'`

7. `--output`:

- Description: Specifies the directory where the redacted text files will be saved.
- Usage: `--output 'path/to/output/directory'`
- Example: `--output 'output/'`

8. `--stats`:

- Description: Specifies where to output the redaction statistics. Can be either `stderr` or `stdout` or a file.
- Usage: `--stats 'stderr'`
- Example: `--stats 'stderr'`

Run the Redactor: You can now run the redactor script with the desired options. For example:
```bash
pipenv run python redactor.py --input 'path/to/input/files' --names --dates --phones --address --concept 'house' --output 'path/to/output/files/' --stats stderr
```
![video](video)


# Functions

`get_file_vector`
- Description: Retrieves a list of files matching the specified input pattern.
- Parameters:
    - `input` (str): The input pattern to match files (e.g., `'path/to/files/*.txt'`).
- Returns: A list of matching file paths.

`get_data`
- Description: Reads the content of a specified file.
- Parameters:
    - `input` (str): The path to the input file.
- Returns: The content of the file as a string.

`redact_names`
- Description: Redacts personal names from the text.
- Parameters:
    - `data` (str): The input text data.
    - `nlp` (spacy.Language): The Spacy NLP model.
    - `stats` (str): The output stream for statistics (`stderr` or `stdout` or any file).
    - `filename` (str): The name of the file being processed.
- Returns: The redacted text with names replaced by block characters.

`redact_dates`
- Description: Redacts dates in various formats from the text.
- Parameters:
    - `data` (str): The input text data.
    - `nlp` (spacy.Language): The Spacy NLP model.
    - `stats` (str): The output stream for statistics (`stderr` or `stdout` or any file).
    - `filename` (str): The name of the file being processed.
- Returns: The redacted text with dates replaced by block characters.

`redact_phones`
- Description: Redacts phone numbers, including international formats, from the text.
- Parameters:
    - `data` (str): The input text data.
    - `stats` (str): The output stream for statistics (`stderr` or `stdout` or any file).
    - `filename` (str): The name of the file being processed.
- Returns: The redacted text with phone numbers replaced by block characters.

`redact_addresses`
- Description: Redacts physical addresses from the text.
- Parameters:
    - `data` (str): The input text data.
    - `stats` (str): The output stream for statistics (`stderr` or `stdout` or any file).
    - `filename` (str): The name of the file being processed.
- Returns: The redacted text with addresses replaced by block characters.

`get_similar_words`
- Description: Finds words similar to the given concept in the provided text using Spacy's word vectors.
- Parameters:
    - `nlp` (spacy.Language): The Spacy NLP model.
    - `data` (str): The input text data.
    - `concept` (str): The concept word to find similar words for.
    - `topn` (int): The number of top similar words to return (default is 10).
- Returns: A list of words similar to the given concept.

`redact_concepts`
- Description: Redacts words similar to the given concept from the text.
- Parameters:
    - `nlp` (spacy.Language): The Spacy NLP model.
    - `data` (str): The input text data.
    - `concept` (str): The concept word to find similar words for.
    - `stats` (str): The output stream for statistics (`stderr` or `stdout` or any file).
    - `filename` (str): The name of the file being processed.
- Returns: The redacted text with concept-related words replaced by block characters.


# Bugs and Assumptions

### Bugs

1. Phone Number Redaction:
- Issue: The phone number redaction may incorrectly redact numeric IDs that resemble phone numbers.
- Example: Numeric IDs such as "1234567890" might be redacted as phone numbers even if they are not actual phone numbers.

2. Concept Redaction:
- Issue: The concept redaction might not capture all synonyms or related terms due to limitations in the word vector model.
- Example: Some contextually similar words might not be redacted if they are not recognized as similar by the model.

3. Address Redaction:
- Issue: The address redaction only redacts addresses that match the defined format as per the `pyap` library. Addresses that do not conform to this format might not be redacted.
- Example: Unconventional address formats or text that resembles an address might not be redacted correctly.

4. Date Redaction:
- Issue: The date redaction might miss some date formats or incorrectly redact non-date text.
- Example: Dates written in non-standard formats or text that resembles a date might not be redacted correctly.

5. Performance:
- Issue: The redaction process might be slow for large text files due to the complexity of NLP operations and use of `en_core_web_trf` model is affecting the performance.
- Example: Processing large documents with multiple redaction types enabled might take a significant amount of time.

6. Name Redaction:
- Issue: The name redaction may not detect all names due to limitations in the Spacy model.
- Example: Some names might not be recognized and redacted by the model.

### Assumptions


1. Spacy Model:
- Assumption: The Spacy model `en_core_web_trf` is sufficient for named entity recognition and word vector operations.
- Example: The tool uses the `en_core_web_trf` model for all NLP tasks, assuming it provides adequate performance and accuracy.

2. Redaction Characters:
- Assumption: The block character `(U+2588)` is used for redaction.
- Example: All redacted text is replaced with block characters to indicate redaction.

3. Statistics Output:
- Assumption: The statistics output can be directed to `stderr`, `stdout`, or a specified file.
- Example: The tool assumes that the user will specify where to output the redaction statistics.

4. Concept Similarity:
- Assumption: The word vector model accurately captures the similarity between words for concept redaction.
- Example: The tool relies on the word vector model to find and redact words similar to the specified concept.

5. File Encoding:
- Assumption: The input and output files are encoded in UTF-8.
- Example: The tool reads and writes files assuming they are UTF-8 encoded.
