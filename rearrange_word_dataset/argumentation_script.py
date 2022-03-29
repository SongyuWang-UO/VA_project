import random

from util.base_augmentation_script import read_original_dataset, output_to_file


def swap_n_words(n):
    ori_data = read_original_dataset()
    new_dataset = {}
    for command, intent in ori_data.items():
        command_words = command.split(' ')
        length = len(command_words)
        for _ in range(n):
            pos = random.randint(0, length-1)
            pos2 = random.randint(0, length - 1)
            while pos==pos2:
                pos2 = random.randint(0, length - 1)
            command_words[pos], command_words[pos2] = command_words[pos2], command_words[pos]
        new_dataset[' '.join(command_words)] = intent
    return new_dataset


for k in range(1, 3):
    data = swap_n_words(k)
    output_to_file(data, f'./rearrange_word_dataset/data_with_{k}_rearranged_word.json')
