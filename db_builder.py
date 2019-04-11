import os
import psycopg2
import re
import requests
import json

DATA_DIR = 'data'
DB_NAME = 'summaries_sk_wikipedia'

def tokenize(text):
    text = re.sub(r" ?\([^)]+\)", "", text)
    url = 'http://nlp.bednarik.top/ssplit/json'
    payload = {'input': text.encode('utf-8'), 'method': 'STAT'}
    response = requests.post(url, data=payload)
    json_str = response.content.decode('utf-8')
    tree = json.loads(json_str)
    sentences = [part['originalText'] for part in tree['sentences']]
    return sentences

def insert_domain(label):
    sql = """INSERT INTO domain(label)
             VALUES(%s) RETURNING id;"""
    id = None
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_NAME, password=DB_NAME)
        cur = conn.cursor()
        cur.execute(sql, (label,))
        id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return id

def insert_summary(title,pageid,url,domain_id):
    sql = """INSERT INTO summary(title,pageid,url,domain_id)
             VALUES(%s,%s,%s,%s) RETURNING id;"""
    id = None
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_NAME, password=DB_NAME)
        cur = conn.cursor()
        cur.execute(sql, (title,pageid,url,domain_id,))
        id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return id

def insert_sentence(rank,text,summary_id):
    sql = """INSERT INTO sentence(rank,text,summary_id)
             VALUES(%s,%s,%s);"""
    id = None
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_NAME, password=DB_NAME)
        cur = conn.cursor()
        cur.execute(sql, (rank,text,summary_id,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def build_database(DEBUG=False):
    if DEBUG: print('DEBUG on')
    domain_id, summary_id = None, None
    for directory in os.listdir(DATA_DIR):
        print(directory)
        if not DEBUG: domain_id = insert_domain(directory)
        for f_name in os.listdir(os.path.join(DATA_DIR, directory)):
            with open(os.path.join(DATA_DIR, directory,f_name), 'r', encoding="utf8") as f:
                pageid = f.readline().rstrip()
                title = f.readline().rstrip()
                url = f.readline().rstrip()
                all_sent = tokenize(f.read())
            if not DEBUG: summary_id = insert_summary(title,pageid,url,domain_id)
            print('\t' + title + '\t' + pageid + '\t' + url + '\t'+str(domain_id))
            for rank,text in enumerate(all_sent):
                print(str(rank) + '\t' + text + '\t'+str(summary_id))
                if not DEBUG: insert_sentence(rank,text,summary_id)

if __name__ == "__main__":
    build_database(DEBUG=True)

