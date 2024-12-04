# cis6930fa24-project1
Name:Rushit Varma Gadiraju

# Project Description
This Python package accepts a glob pattern, output directory, and file flags to locate matching files, process each one by masking names, phone numbers, addresses, and dates, and generate document statistics in stderr, stdout, or a specified stats file. The censored content is then saved in a new file with a '.censored' extension.

PROJECT STRUCTURE

The project is organized with an initial redactor file that triggers the process, leveraging four modules—redact_dates, redact_phone, redact_address, redact_names, and redact_concepts—to carry out the specified actions. All these files are located in the root directory.

The downloaded files is saved into the directory path given in the --output flag. 

Command-Line Arguments The program accepts several command-line arguments to customize its behavior. Below is a list of the available arguments:

--input: Path(s) to input files or glob patterns (e.g., *.txt).
--output: Directory to save redacted files.
--names: Redact names (optional flag).
--dates: Redact dates (optional flag).
--phones: Redact phone numbers (optional flag).
--address: Redact addresses (optional flag).
--concept: Redact sentences containing specified concepts (can be used multiple times).
--stats: Output redaction statistics to stdout, stderr, or a file.


KEY LIBRARIES

spaCy: Detects entities such as names, dates, and geographical places.
re: Used for regex-based phone number redaction.
argparse: Handles command-line arguments.
glob: Facilitates pattern-based file searches.

Classes and Methods:

Redactor:
redact_names: Detects and redacts PERSON entities.
redact_dates: Detects and redacts DATE and TIME entities.
redact_phones: Matches phone number patterns and replaces them.
redact_address: Detects and redacts GPE (geo-political entities).
redact_concepts: Redacts sentences containing user-specified concepts.
File Handling:
process_file: Reads files, applies redactions, and saves results.
write_stats: Outputs redaction statistics.
Execution Flow:

Parse command-line arguments.
Process files using specified redaction options.
Save redacted files to the output directory.
Output redaction statistics.


TESTING
This project contains test files that test all the redactor modules along with the stats. each test case to test redactor modules is written in test_redactor.py.


# Installation
pipenv install

## Run the code
1-pipenv shell
2- pipenv install
3- pipenv run python redactor.py --input '*.txt' --names --dates --phones --address --output 'output/' --stats stderr



## Testing
pipenv run python3 -m pytest <test_file>



 
