import os

DATA_DIR = 'data'
DB_NAME = 'summaries_sk_wikipedia'

def getInfo():
    domain_id, summary_id = None, None
    for directory in os.listdir(DATA_DIR):
        # print directory + '\t' + str(len(os.listdir(os.path.join(DATA_DIR, directory))))
        for f_name in os.listdir(os.path.join(DATA_DIR, directory)):
            with open(os.path.join(DATA_DIR, directory,f_name), 'r') as f:
                pageid = f.readline().rstrip()
                title = f.readline().rstrip().decode('utf8')
                url = f.readline().rstrip()
                all_sent = sent_tokenize(f.read().decode('utf8'))
            print title + '\t' + url
            break

if __name__ == "__main__":
    getInfo()

