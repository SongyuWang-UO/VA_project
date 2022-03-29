import json
from itertools import chain
import random

from nltk.corpus import wordnet


def get_synonyms(word,default_words):
    # https://stackoverflow.com/questions/19258652/how-to-get-synonyms-from-nltk-wordnet-python
    synonyms = wordnet.synsets(word)
    lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
    try:
        lemmas.remove(word)
        return lemmas[0]
    except:
        return random.choice(default_words).decode('utf-8')

def read_original_dataset():
    formatted = {}
    with open('original_dataset/snips.json', 'r') as f:
        data = json.load(f)
        for data_piece in data:
            formatted[data_piece[0]] = data_piece[1]
    return formatted


def output_to_file(data, path):
    to_data = []
    for command, intent in data.items():
        to_data.append([command, intent])
    f = open(path, "w")
    f.write(json.dumps(to_data))
    f.close()


def read_oos_source():
    formatted = {}
    with open('./original_dataset/OOS_source/seq.in', 'r') as f:
        commands = [line.replace('\n', '') for line in f.readlines()]
        with open('./original_dataset/OOS_source/label', 'r') as f_2:
            intents = [line.replace('\n', '') for line in f_2.readlines()]
            for k in range(len(commands)):
                formatted[commands[k]] = "OOS"
    return formatted


def read_more_intents_source(OOS=False):
    formatted = {}
    with open('./original_dataset/more_intent_types/seq.in', 'r') as f:
        commands = [line.replace('\n', '') for line in f.readlines()]
        with open('./original_dataset/more_intent_types/label', 'r') as f_2:
            intents = [line.replace('\n', '') for line in f_2.readlines()]
            with open('./original_dataset/more_intent_types/para.in', 'r') as f_3:
                command_paras = [line.replace('\n', '') for line in f_3.readlines()]
                for k in range(len(commands)):
                    formatted[commands[k]] = intents[k] if not OOS else "OOS"
                    formatted[command_paras[k]] = intents[k] if not OOS else "OOS"
    return formatted
