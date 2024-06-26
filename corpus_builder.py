#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import wikipedia
import time

wikipedia.set_lang("sk")
DOMAIN = 'birds'
FILTER = 'vtak'

directory = 'data/' + DOMAIN + '/'
source_file = 'data/' + DOMAIN + '.txt'

def filter_opts(filter,options):
    match = [s for s in options if filter in s]
    if match: return match[0]
    return None

def load_page(name):
    """
    :param name:
    :return: page downloaded from wikipedia
    """
    try:
        page = wikipedia.WikipediaPage(name)
        print(name)
        return page
    except wikipedia.exceptions.DisambiguationError as e:
        redirect = filter_opts(FILTER, e.options)
        if redirect: return load_page(redirect)
    except wikipedia.exceptions.PageError as pe:
        pass
    except AssertionError as ae:
        pass
    except KeyError as ke:
        pass

def save_summary(page):
    """
    Save summary to file
    :param page:
    """
    url = page.url
    title = page.title
    id = page.pageid
    summary = page.summary
    with open(directory + id + '.txt', 'w') as file:
        file.write(id + '\n')
        file.write(title + '\n')
        file.write(url + '\n')
        file.write(summary)
    print('\t : success')

def process_domain(debug=False):
    """
    Download and save all summaries from list in file
    :param debug:
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(source_file) as file:
        for i,name in enumerate(file.read().splitlines()):
            p = load_page(name)
            if p is not None and debug is False:
                save_summary(p)
            time.sleep(1)

if __name__ == "__main__":
    process_domain()
