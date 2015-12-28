import json


def save_file(f, season):
    with open(season, 'w') as outfile:
        json.dump(f, outfile)
