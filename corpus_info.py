#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from nltk.tokenize import sent_tokenize
import pandas as pd
import numpy as np
import matplotlib as plt
plt.interactive(False)

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

def man_eval_info():
    rows = []
    sent_1, sent_2, sim = None, None, None
    with open('manual_evaluation/selected_sentences.txt', 'r', encoding='utf8') as file_in:
        line = file_in.readline()
        cnt, id = 0, 1
        while line:
            if(cnt%3 == 0):
                sent_1 = line.strip()
            if(cnt%3 == 1):
                sent_2 = line.strip()
            if(cnt%3 == 2):
                sim = line.strip()
                # rows.append({"id":id, "sent_1":sent_1, "sent_2":sent_2, "sim":sim})
                rows.append(sent_1)
                rows.append(sent_2)
                id = id+1
            line = file_in.readline()
            cnt += 1
    lens = [len(r.split()) for r in rows]
    print(lens)
    # return rows

if __name__ == "__main__":
    # number_sumaries_by_domain()
    # print_info()
    man_eval_info()
