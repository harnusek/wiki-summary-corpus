import unittest
import requests
import json

"""
Requires running server
"""

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
    for sent, sent_POS, sent_NEG in get_triplet():
        data["sent_1"] = sent
        data["sent_2"] = sent_POS
        response = requests.post(url, data=json.dumps(data), headers=headers)
        sim_POS = float(response.content)

        data["sent_1"] = sent
        data["sent_2"] = sent_NEG
        response = requests.post(url, data=json.dumps(data), headers=headers)
        sim_NEG = float(response.content)
        print(sent[:10], method, use_lem, use_pos, use_stop, sim_POS, 1 - sim_NEG)

def get_triplet():
    return database

if __name__ == '__main__':
    all_config_testing()
