import json


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
