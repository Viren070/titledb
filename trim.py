#!/usr/bin/env python3

import sys
import json


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <json file>".format(sys.argv[0]))
        sys.exit(1)

    with open(sys.argv[1]) as f:
        data = json.load(f)

    new_data = {}
    for k, v in data.items():
        name = v.get('name')
        if not name:
            continue 
        new_data[k] = {
            'description': v['description'],
            'iconUrl': v['iconUrl'],
            'id': v['id'],
            'name': v['name'],
            'releaseDate': v['releaseDate'],
            'size': v['size'],
        }
    with open(sys.argv[1], 'w') as f:
        json.dump(new_data, f, separators=(',', ':'))