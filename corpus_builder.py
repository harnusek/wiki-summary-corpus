import os
import wikipedia

wikipedia.set_lang("sk")
domain = 'cities_sk'

directory = 'data/' + domain + '/'
source_file = 'data/' + domain + '.txt'

def load_page(name):
    page = wikipedia.WikipediaPage(name)
    return page

def save_summary(page):
    url = page.url
    title =page.title.encode('utf-8')
    id = page.pageid
    summary = page.summary.encode('utf-8')
    with open(directory + title + '.txt', 'w') as file:
        file.write(id+'\n')
        file.write(title+'\n')
        file.write(url+'\n')
        file.write(summary)
    print(title+' : succes')

def process_domain():
    if not os.path.exists(directory):
        os.makedirs(directory)
    p =load_page('Bratislava')
    save_summary(p)

if __name__ == "__main__":
    process_domain()