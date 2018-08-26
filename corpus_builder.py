import os
import wikipedia

wikipedia.set_lang("sk")
domain = 'cities_sk'

directory = 'data/' + domain + '/'
source_file = 'data/' + domain + '.txt'


def load_page(name):
    try:
        page = wikipedia.WikipediaPage(name)
        return page
    except wikipedia.exceptions.DisambiguationError as e:
        print(name + ' : fail')
        for o in e.options:
            print '\t\t' + o

def save_summary(page):
    url = page.url
    title = page.title.encode('utf-8')
    id = page.pageid
    summary = page.summary.encode('utf-8')
    with open(directory + page.title + '.txt', 'w') as file:
        file.write(id + '\n')
        file.write(title + '\n')
        file.write(url + '\n')
        file.write(summary)
    print(title + ' : success')


def process_domain(debug=False):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(source_file) as file:
        for name in file.read().splitlines():
            p = load_page(name)
            if p is not None and debug is False:
                save_summary(p)


if __name__ == "__main__":
    process_domain(True)
