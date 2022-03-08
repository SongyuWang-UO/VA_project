import random
import string

from util.base_augmentation_script import read_original_dataset, output_to_file


def replace_n_chars(n):
    ori_data = read_original_dataset()
    new_dataset = {}
    for command, intent in ori_data.items():
        length = len(command)
        for _ in range(n):
            pos = random.randint(0, length)
            change_to = random.choice(string.ascii_lowercase)
            command = command[:pos] + change_to + command[pos + 1:]
        new_dataset[command] = intent
    return new_dataset


for k in range(1, 10):
    data = replace_n_chars(k)
    output_to_file(data, f'./typo_dataset/data_with_{k}_typo.json')
