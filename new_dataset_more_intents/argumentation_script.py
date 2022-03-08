from util.base_augmentation_script import output_to_file, read_more_intents_source

data = read_more_intents_source(False)
output_to_file(data, f'./new_dataset_more_intents/dataset.json')
