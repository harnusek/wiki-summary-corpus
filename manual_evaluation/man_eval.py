#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Requires running server and outputs from experiment
"""
import requests
import json
import math
import os

def all_config_testing():
    for method in ['corpusSim','knowledgeSim']:
        for use_lem in [True, False]:
            for use_pos in [True, False]:
                for use_stop in [True, False]:
                    compare_method(method, use_lem, use_pos, use_stop)

def compare_method(method, use_lem, use_pos, use_stop):
    sum_difference = 0
    number_experiments = len(EXPERIMENT)
    for row in EXPERIMENT:
        sent_1 = row["sent_1"]
        sent_2 = row["sent_2"]
        man_sim = row["sim"]

        computed_sim = get_similarity(sent_1,sent_2,method, use_lem, use_pos, use_stop)
        diff = man_sim - computed_sim
        sum_difference = sum_difference + (diff*diff)

    avg_diff = sum_difference/(number_experiments-2)
    error = round(math.sqrt(avg_diff), 4)
    file.write('AVG '+method+'\tlem:'+str(use_lem)+'\tpos:'+str(use_pos)+'\tstop:'+str(use_stop)+'\t'+str(error)+'\t=1 - '+str(1-error)+'\n')
    print('AVG '+method+'\tlem:'+str(use_lem)+'\tpos:'+str(use_pos)+'\tstop:'+str(use_stop)+'\t'+str(error)+'\t=1 - '+str(1-error)+'\n')

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

def averaged_experiments():
    names = os.listdir("experiments")
    experiments = list()
    for name in names:
        experiments.append(load_experiment(name))
    final = []
    for exp in zip(*experiments):
        sims = [line['sim'] for line in exp]
        # averaging similarity of all experiments
        avg_sim = (sum(sims)/len(sims))
        print(sims, avg_sim/4)
        final.append(({'sent_1':exp[0]['sent_1'], 'sent_2':exp[0]['sent_2'], 'sim':avg_sim}))
    return final

def load_experiment(name):
    rows = []
    sent_1, sent_2, sim = None, None, None
    with open('experiments/'+name, 'r', encoding='utf8') as file_in:
        line = file_in.readline()
        cnt, id = 0, 1
        while line:
            if(cnt%3 == 0):
                sent_1 = line.strip()
            if(cnt%3 == 1):
                sent_2 = line.strip()
            if(cnt%3 == 2):
                sim = line.strip()
                rows.append({"id":id, "sent_1":sent_1, "sent_2":sent_2, "sim":float(sim)})
                id = id+1
            line = file_in.readline()
            cnt += 1
    return rows

if __name__ == '__main__':
    EXPERIMENT = averaged_experiments()
    # fname = "reports/report-averaged-new.txt"
    # file = open(fname, "w")
    # file.write('pos tagset basic, experiment comparation\n\n')
    # all_config_testing()
    # file.close()