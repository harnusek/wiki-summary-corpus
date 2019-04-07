"""
Requires running server and database
"""

import requests
import json
import psycopg2
import time
import os

domains = ['bands', 'battles', 'birds', 'cars', 'castles_sk', 'cities_sk', 'constellations', 'countries', 'dinosaurs',
           'dogs', 'elements', 'mammals', 'movies', 'myth_figures', 'peaks_sk', 'plants_sk', 'regions_sk', 'rivers_sk',
           'rocks', 'sports']

DATA_DIR = 'data'
DB_NAME = 'summaries_sk_wikipedia'
NUMBER_OF_TRIPLETS = 1
DOMAIN_P = 'cities_sk'
DOMAIN_N = 'peaks_sk'

def all_config_testing():
    for method in ['corpusSim']:
        for use_lem in [True, False]:
            for use_pos in [True, False]:
                for use_stop in [True, False]:
                    triplet_testing(method, use_lem, use_pos, use_stop)

def triplet_testing(method, use_lem, use_pos, use_stop):
    print(fname)
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
    file.write('AVG '+method+'\tlem:'+str(use_lem)+'\tpos:'+str(use_pos)+'\tstop:'+str(use_stop)+'\t'+str(POS)+'\t'+str(NEG)+'\t'+str(DIFF)+'\n')
    print('AVG', method,'\tlem:', use_lem,'pos:', use_pos,'stop:', use_stop, POS, NEG, DIFF)

def select_sentences(count, domain):
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

def triplets():
    sent = select_sentences(2*NUMBER_OF_TRIPLETS, DOMAIN_P)
    sent_POS = sent[NUMBER_OF_TRIPLETS:]
    sent_NEG = select_sentences(2*NUMBER_OF_TRIPLETS, DOMAIN_N)
    for i in range(NUMBER_OF_TRIPLETS):
        # print([sent[i], sent_POS[i], sent_NEG[i]])
        yield [sent[i], sent_POS[i], sent_NEG[i]]

def triplets_all_domains():
    pocet = 1
    database = [select_sentences(2*pocet,domain) for domain in domains]
    for index in range(len(database)):
        sent = database[index][:pocet]
        sent_POS = database[index][pocet:]
        sent_NEG = database[index-1][pocet:]
        # print(sent,sent_POS,sent_NEG)
        for i in range(pocet):
            yield [sent[i], sent_POS[i], sent_NEG[i]]

if __name__ == '__main__':
    fname = time.strftime("reports/%Y-%m-%d-%H-%M") + "(1x20).txt" #str(NUMBER_OF_TRIPLETS) + ").txt"
    file =  open(fname, "a")
    # file.write('['+ DOMAIN_P + ', ' + DOMAIN_N + '] ')
    file.write('[all domains] ')
    file.write('pos tagset basic rivalF\n\n') # <------------POPIS SEM
    all_config_testing()
    file.close()
