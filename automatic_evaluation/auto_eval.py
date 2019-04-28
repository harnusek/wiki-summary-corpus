#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates automatic evaluation of semantic-similarity-tool with every configuration
Requires running server and database
"""

import requests
import json
import psycopg2
import time

DOMAINS = ['bands', 'battles', 'birds', 'cars', 'castles_sk', 'cities_sk', 'constellations', 'countries', 'dinosaurs',
           'dogs', 'elements', 'mammals', 'movies', 'myth_figures', 'peaks_sk', 'plants_sk', 'regions_sk', 'rivers_sk',
           'rocks', 'sports']
DATA_DIR = 'data'
DB_NAME = 'summaries_sk_wikipedia'

def all_config_testing():
    """
    Start evaluation with every configuration
    """
    for method in ['corpusSim','knowledgeSim']:
        for use_lem in [True, False]:
            for use_pos in [True, False]:
                for use_stop in [True, False]:
                    triplet_testing(method, use_lem, use_pos, use_stop)

def triplet_testing(method, use_lem, use_pos, use_stop):
    """
    Start evaluation with params
    :param method:
    :param use_lem:
    :param use_pos:
    :param use_stop:
    """
    headers = {'content-type': 'application/json'}
    url = 'http://localhost:5000/api/' + method
    data = {
        "sent_1": None,
        "sent_2": None,
        "use_lem": use_lem,
        "use_pos": use_pos,
        "use_stop": use_stop
    }
    sum_POS  = 0
    sum_NEG  = 0
    count  = 0
    for sent, sent_POS, sent_NEG in triplets_all_domains():
        data["sent_1"] = sent
        data["sent_2"] = sent_POS
        response = requests.post(url, data=json.dumps(data), headers=headers)
        sim_POS = float(response.content)
        sum_POS = sum_POS+sim_POS
        data["sent_1"] = sent
        data["sent_2"] = sent_NEG
        response = requests.post(url, data=json.dumps(data), headers=headers)
        sim_NEG = float(response.content)
        sum_NEG = sum_NEG+sim_NEG
        count=count+1
    POS = round(sum_POS/count,4)
    NEG = round(sum_NEG/count,4)
    DIFF = round(POS-NEG,4)
    file.write(method+'\t'+str(use_lem)+'\t'+str(use_pos)+'\t'+str(use_stop)+'\t'+str(POS)+'\t'+str(NEG)+'\t'+str(DIFF)+'\n')
    print(method+'\t'+str(use_lem)+'\t'+str(use_pos)+'\t'+str(use_stop)+'\t'+str(POS)+'\t'+str(NEG)+'\t'+str(DIFF))

def select_sentences(count, domain):
    """
    :param count:
    :param domain:
    :return: Sentences from database
    """
    sql = """select sentence.text
            from sentence
            join summary on summary_id = summary.id
            join domain on domain_id = domain.id
            where sentence.rank = 0 and domain.label = '""" + domain + """'
            order by summary_id
            limit """ + str(count)
    triplets = None
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_NAME, password=DB_NAME)
        cur = conn.cursor()
        cur.execute(sql)
        triplets = [x[0] for x in cur.fetchall()]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            cur.close()
    return triplets

def triplets_all_domains():
    """
    :return: List of 10 triplets from every domain
    """
    count = 10
    database = [select_sentences(2*count,domain) for domain in DOMAINS]
    for index in range(len(database)):
        sent = database[index][:count]
        sent_POS = database[index][count:]
        sent_NEG = database[index-1][count:]
        for i in range(count):
            yield [sent[i], sent_POS[i], sent_NEG[i]]

if __name__ == '__main__':
    fname = "reports/auto-eval-report-10x20.txt"
    file =  open(fname, "w")
    file.write('method\t\tuse_lem\tuse_pos\tuse_stop\tpos\nneg\ndiff\n')
    print('method\t\tuse_lem\tuse_pos\tuse_stop\tpos\nneg\ndiff\n')
    all_config_testing()
    file.close()
