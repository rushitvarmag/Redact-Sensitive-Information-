import spacy
import en_core_web_md
import re
import os
import argparse
import glob
import tarfile
import requests
import sys
from spacy.tokens import Doc

class Redactor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.stats = {
            "names": 0,
            "dates": 0,
            "phones": 0,
            "addresses": 0,
            "concepts": 0
        }

    def redact_names(self, doc):
        redacted = doc.text
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                redacted = redacted.replace(ent.text, '█' * len(ent.text))
                self.stats["names"] += 1
        return self.nlp(redacted)

    def redact_dates(self, doc):
        redacted = doc.text
        for ent in doc.ents:
            if ent.label_ in ['DATE', 'TIME']:
                redacted = redacted.replace(ent.text, '█' * len(ent.text))
                self.stats["dates"] += 1
        return self.nlp(redacted)

    def redact_phones(self, doc):
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        redacted = re.sub(phone_pattern, lambda m: '█' * len(m.group()), doc.text)
        self.stats["phones"] += len(re.findall(phone_pattern, doc.text))
        return self.nlp(redacted)

    def redact_address(self, doc):
        redacted = doc.text
        for ent in doc.ents:
            if ent.label_ == 'GPE':
                redacted = redacted.replace(ent.text, '█' * len(ent.text))
                self.stats["addresses"] += 1
        return self.nlp(redacted)

    def redact_concepts(self, doc, concepts):
        redacted = doc.text
        for sent in doc.sents:
            if any(concept.lower() in sent.text.lower() for concept in concepts):
                redacted = redacted.replace(sent.text, '█' * len(sent.text))
                self.stats["concepts"] += 1
        return self.nlp(redacted)

    def process_file(self, input_path, output_dir, args):
        try:
            with open(input_path, 'r', encoding="utf-8", errors="ignore") as f:
                text = f.read()
            doc = self.nlp(text)

            # Apply redactions
            if args.names:
                doc = self.redact_names(doc)
            if args.dates:
                doc = self.redact_dates(doc)
            if args.phones:
                doc = self.redact_phones(doc)
            if args.address:
                doc = self.redact_address(doc)
            if args.concept:
                doc = self.redact_concepts(doc, args.concept)

            # Write censored output
            output_path = os.path.join(output_dir, os.path.basename(input_path) + ".censored")
            with open(output_path, 'w') as f:
                f.write(doc.text)
                print("done")
        except Exception as e:
            print(f"Error processing file {input_path}: {e}")

    def write_stats(self, stats_output):
        output = "Redaction Statistics:\n"
        for key, count in self.stats.items():
            output += f"{key.capitalize()}: {count}\n"

        output += "\nDetailed Redaction Count:\n"
        for key, count in self.stats.items():
            output += f"{key.capitalize()} Count: {count}\n"

        if stats_output.lower() == "stderr":
            sys.stderr.write(output)
        elif stats_output.lower() == "stdout":
            sys.stdout.write(output)
        else:
            with open(stats_output, "w") as f:
                f.write(output)

def get_arguments():
    parser = argparse.ArgumentParser(description="Redacts sensitive information from text files.")
    parser.add_argument('--input', nargs='+', help='Input files as glob pattern', required=True)
    parser.add_argument('--output', help='Directory to store censored files', required=True)
    parser.add_argument('--names', action='store_true', help='Redact names')
    parser.add_argument('--dates', action='store_true', help='Redact dates')
    parser.add_argument('--phones', action='store_true', help='Redact phone numbers')
    parser.add_argument('--address', action='store_true', help='Redact addresses')
    parser.add_argument('--concept', action='append', help='Concepts to redact')
    parser.add_argument('--stats', help='File or location for stats (stderr, stdout)')
    return parser.parse_args()

def main():
    args = get_arguments()
    os.makedirs(args.output, exist_ok=True)

    redactor = Redactor()

    for input_pattern in args.input:
        for input_path in glob.glob(input_pattern):  
            print(f"Processing file: {input_path}") 
            redactor.process_file(input_path, args.output, args)

    if args.stats:
        redactor.write_stats(args.stats)


if __name__ == '__main__':
    main()