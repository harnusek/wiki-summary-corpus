#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Requires running server and outputs from experiment
"""

import requests
import json
import io

EXPERIMENT_NAME = 'ondrej'

def all_config_testing():
    for method in ['corpusSim','knowledgeSim']:
        for use_lem in [True, False]:
            for use_pos in [True, False]:
                for use_stop in [True, False]:
                    compare_method(method, use_lem, use_pos, use_stop)

def compare_method(method, use_lem, use_pos, use_stop):
    agg_difference = 0
    number_experiments = len(experiment["rows"])
    for row in experiment["rows"]:
        sent_1 = row["sent_1"]
        sent_2 = row["sent_2"]
        man_sim = row["sim"]

        computed_sim = get_similarity(sent_1,sent_2,method, use_lem, use_pos, use_stop)
        agg_difference = agg_difference + abs(man_sim - computed_sim)
        # print(man_sim, computed_sim, method + str(use_lem) + str(use_pos) + str(use_stop) + ' ' + sent_1 + ' ' + sent_2)

    avg_diff = round(agg_difference/number_experiments, 4)
    file.write('AVG '+method+'\tlem:'+str(use_lem)+'\tpos:'+str(use_pos)+'\tstop:'+str(use_stop)+'\t'+str(avg_diff)+'\t=1 - '+str(1-avg_diff)+'\n')

def get_similarity(sent_1, sent_2, method, use_lem, use_pos, use_stop):
    headers = {'content-type': 'application/json'}
    url = 'http://localhost:5000/api/' + method
    data = {
        "sent_1": sent_1,
        "sent_2": sent_2,
        "use_lem": use_lem,
        "use_pos": use_pos,
        "use_stop": use_stop
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return float(response.content)

def load_experiment():
    with open('experiments/'+EXPERIMENT_NAME+'.json', 'r', encoding="utf8") as json_file:
        json_str = json_file.read()
        return json.loads(json_str)

def just_temporary():
    rows = []
    sent_1, sent_2, sim = None, None, None
    with open('select-sentences.txt', 'r', encoding="utf8") as fp:
        line = fp.readline()
        cnt = 0
        while line:
            if(cnt%3 == 0):
                sent_1 = line.strip()
            if(cnt%3 == 1):
                sent_2 = line.strip()
            if(cnt%3 == 2):
                sim = line.strip()
                rows.append({"sent_1":sent_1, "sent_2":sent_2, "sim":sim})
            line = fp.readline()
            cnt += 1

    dictionary = {"rows":rows}
    with io.open('output.json', 'w', encoding='utf8') as json_file:
        json.dump(dictionary, json_file, ensure_ascii=False)

if __name__ == '__main__':
    just_temporary()
    # experiment = load_experiment()
    # fname = "reports/" + EXPERIMENT_NAME + "-comparation.txt"
    # file = open(fname, "w")
    # file.write('pos tagset basic\n\n')
    # all_config_testing()
    # file.close()