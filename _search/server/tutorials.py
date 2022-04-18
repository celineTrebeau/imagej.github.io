#!/bin/env python

# Parse ImageJ tutorials into documents for
# use with their own searchable collection.

import logging, traceback, re
import json
from parseutil import first_sentence
from pathlib import Path


logger = logging.getLogger(__name__)


def is_imagej_tutorials(root):
    java = Path(root) / 'java'
    notebooks = Path(root) / 'notebooks'
    return java.isdir() and notebooks.isdir()


def parse_java_source(path):
    logger.debug(f'Parsing Java source file {path}...')

    with open(path) as f:
        lines = json.load(f)

    # This is dumb -- do we want to do better?
    doc = {}
    doc['content'] = ''.join(lines)

    return doc


def parse_notebook(path):
    logger.debug(f'Parsing notebook {path}...')

    with open(path) as f:
        data = json.load(f)

    doc = {}
    doc['content'] = ''
    for cell in data['cells']:
        # TODO: implement process_cell: extract source and output(s) if present
        doc['content'] += process_cell(cell)

    return doc

# type of cell is dict
def process_cell(cell):
    result = ''

    if 'source' in cell:
        result += filter_data("".join(cell['source']))
    
    # case 1: code cell
    if 'outputs' in cell:
        for o in cell['outputs']:
            #vals = o.values()
            if 'text' in o:
                result += filter_data("".join(o['text']))
            if 'data' in o:
                # if has_good_key(o['data']):
                if 'text/html' in o['data']:
                    result += filter_data("".join(o['data']['text/html']))
                if 'text/plain' in o['data']:
                    result += filter_data("".join(o['data']['text/plain']))
            # vals = [v for k, v in o.items() if is_good_key(k)]
            # result += filter_data("".join(vals))

    return result

# takes input of string; filters html and other data 
def filter_data(data):
    # if len(data) > 5000:
    filtered = re.sub('<[^>]*>', '', data)
    return filtered # this string will have markup with it 
    # TODO: remove markup from data

def has_good_key(k):
    keys = "".join(list(k.keys()))
    return 'text/plain' in keys or 'text/html' in keys

def load_imagej_tutorials(root):
    """
    Loads the content from the given imagej/tutorials folder.
    See: https://github.com/imagej/tutorials
    """
    java = Path(root) / 'java'
    notebooks = Path(root) / 'notebooks'
    if not java.isdir() or not notebooks.isdir():
        raise ValueError(f'The path {root} does not appear to be a Jekyll site.')

    logger.info('Loading content...')
    documents = []

    for javafile in java.rglob("**/*.java"):
        try:
            doc = parse_java_source(javafile)
            if doc:
                documents.append(doc)
        except:
            logger.error(f'Failed to parse {Path}:')
            traceback.print_exc()
    logger.info(f'Loaded {len(documents)} documents from Java source files')

    for nbfile in notebooks.rglob("**/*.ipynb"):
        try:
            doc = parse_notebook(nbfile)
            if doc:
                documents.append(doc)
        except:
            logger.error(f'Failed to parse {Path}:')
            traceback.print_exc()
    logger.info(f'Loaded {len(documents)} documents from Jupyter notebooks')

    return documents
