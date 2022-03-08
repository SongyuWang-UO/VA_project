from util.base_augmentation_script import read_original_dataset, output_to_file, read_oos_source, \
    read_more_intents_source


def add_OOS_to_ori_dataset(ratio):
    to_return = {}
    ori_data = read_original_dataset()
    OOS_count = int(len(ori_data.keys()) * ratio)
    oos_dataset = {**read_oos_source(), **read_more_intents_source(True)}
    for k in range(OOS_count):
        to_return[list(oos_dataset.keys())[k]] = oos_dataset[list(oos_dataset.keys())[k]]
    to_return = {**to_return, **ori_data}
    return to_return


for k in [0.25, 0.5, 1, 2]:
    data = add_OOS_to_ori_dataset(k)
    output_to_file(data, f'./OOS_dataset/data_with_ratio_{k}_OOS.json')
