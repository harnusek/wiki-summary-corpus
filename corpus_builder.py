#!/usr/bin/python
import os
import wikipedia

wikipedia.set_lang("sk")
domain = 'cars'

directory = 'data/' + domain + '/'
source_file = 'data/' + domain + '.txt'

def filter_opts(filter,options):
    match = [s for s in options if filter in s]
    if match: return match[0]
    return 'adtggfbxf'

def load_page(name):
    try:
        page = wikipedia.WikipediaPage(name)
        print(name)
        return page
    except wikipedia.exceptions.DisambiguationError as e:
        return load_page(filter_opts('automobil', e.options))
    except wikipedia.exceptions.PageError as pe:
        pass
    except AssertionError as ae:
        pass
    except KeyError as ke:
        pass

def save_summary(page):
    url = page.url
    title = page.title.encode('utf-8')
    id = page.pageid
    summary = page.summary.encode('utf-8')
    with open(directory + id + '.txt', 'w') as file:
        file.write(id + '\n')
        file.write(title + '\n')
        file.write(url + '\n')
        file.write(summary)
    print('\t : success')


def process_domain(debug=False):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(source_file) as file:
        for i,name in enumerate(file.read().splitlines()):
            p = load_page(name)
            if p is not None and debug is False:
                save_summary(p)


if __name__ == "__main__":
    process_domain(not True)
