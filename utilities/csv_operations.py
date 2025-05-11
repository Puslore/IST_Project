import csv


def import_from_csv(paths: list) -> dict:
    '''Import data from test CSV files'''
    data = {}

    for path in paths:
        filename = path.split('/')[-1].split('.')[0]
        data[filename] = read_csv(path)

    return data


def read_csv(path):
    data = []
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data