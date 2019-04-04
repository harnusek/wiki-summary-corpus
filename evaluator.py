"""
Requires running server and database
"""

import requests
import json
import psycopg2

DATA_DIR = 'data'
DB_NAME = 'summaries_sk_wikipedia'

database = [['Koľko je hodín?', 'Aký je čas?', 'Mám rád čokoládu!'],
            ['Kde chodia vlaky?', 'Ako sa dostanem na stanicu?', 'Mám rád čokoládu!'],
            ['Som chladný', 'Dal by som si obed', 'Mám rád čokoládu!']
            ]

def all_config_testing():
    for method in ['knowledgeSim','corpusSim']:
        for use_lem in [True, False]:
            for use_pos in [True, False]:
                for use_stop in [True, False]:
                    triplet_testing(method, use_lem, use_pos, use_stop)

def triplet_testing(method, use_lem, use_pos, use_stop):
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
    for sent, sent_POS, sent_NEG in triplets():
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
        # print(sent[:10], method, use_lem, use_pos, use_stop, sim_POS, 1 - sim_NEG)
    POS = round(sum_POS/count,4)
    NEG = round(sum_NEG/count,4)
    print('AVG', method,'\tlem:', use_lem,'pos:', use_pos,'stop:', use_stop, POS, NEG, POS-NEG)

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
    # for _ in range(count):
    #     yield database[_]

def triplets(count=3):
    sent = select_sentences(2*count, 'movies')
    sent_POS = sent[count:]
    sent_NEG = select_sentences(2*count, 'cities_sk')
    for i in range(count):
        # print([sent[i], sent_POS[i], sent_NEG[i]])
        yield [sent[i], sent_POS[i], sent_NEG[i]]

if __name__ == '__main__':
    all_config_testing()
