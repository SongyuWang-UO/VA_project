import random

import requests


# Reference: https://stackoverflow.com/questions/18834636/random-word-generator-python
from util.base_augmentation_script import read_original_dataset, get_synonyms, output_to_file

response = requests.get("https://www.mit.edu/~ecprice/wordlist.10000")
words = response.content.splitlines()


def replace_n_words(n,is_random=True):
    ori_data = read_original_dataset()
    new_dataset = {}
    for command, intent in ori_data.items():
        command_words = command.split(' ')
        length = len(command_words)
        for _ in range(n):
            pos = random.randint(0, length-1)
            new_word= random.choice(words).decode('utf-8') if is_random else random.choice(command_words)
            command_words = command_words[:pos+1] + [new_word] + command_words[pos + 1:]
        new_dataset[' '.join(command_words)] = intent
    return new_dataset


for k in range(1, 3):
    data = replace_n_words(k)
    output_to_file(data, f'./add_word_dataset/data_with_{k}_added_word_new.json')
    data = replace_n_words(k,False)
    output_to_file(data, f'./add_word_dataset/data_with_{k}_added_word_from_same_sentence.json')
