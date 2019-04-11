#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from nltk.tokenize import sent_tokenize

DATA_DIR = 'data'
DB_NAME = 'summaries_sk_wikipedia'

def print_info():
    domain_id, summary_id = None, None
    for directory in os.listdir(DATA_DIR):
        # print directory + '\t' + str(len(os.listdir(os.path.join(DATA_DIR, directory))))
        for f_name in os.listdir(os.path.join(DATA_DIR, directory)):
            with open(os.path.join(DATA_DIR, directory,f_name), 'r', encoding="utf8") as f:
                pageid = f.readline().rstrip()
                title = f.readline().rstrip()
                url = f.readline().rstrip()
                all_sent = sent_tokenize(f.read())
            print(title + '\t' + url)
            print(all_sent)
            break

def number_sumaries_by_domain():
    domain_id, summary_id = None, None
    for directory in os.listdir(DATA_DIR):
        print(directory + '\t' + str(len(os.listdir(os.path.join(DATA_DIR, directory)))))

if __name__ == "__main__":
    # number_sumaries_by_domain()
    print_info()
