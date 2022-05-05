#!/usr/bin/env python3

import json
import re
import os
import requests
import pymongo


def get_symbols_from_file(file_path):
    symbols = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            symbols.append(line)
    return symbols


def get_quote_from_yahoo(symbol, quotes_dir):
    url = f'https://finance.yahoo.com/quote/{symbol}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    with open(os.path.join(quotes_dir, symbol), 'wb') as file:
        file.write(response.content)


def parse_line(sym, line):
    if 'root.App.main = ' in line:
        result = re.search(r"root.App.main = (.+);", line)
        if result:
            data = json.loads(result.group(1))
            return data['context']['dispatcher']['stores']['StreamDataStore']['quoteData'][sym]
    elif 'FIFTY_TWO_WK_RANGE-value' in line:
        result = re.search(r'FIFTY_TWO_WK_RANGE-value">(\d?,?\d+\.\d+) - (\d?,?\d+\.\d+)<\/td', line)
        if result:
            low = float(result.group(1).replace(',', ''))
            high = float(result.group(2).replace(',', ''))
            return {"52WeekLow": low, "52WeekHigh": high}


## MAIN

symbols = get_symbols_from_file('symbols.txt')
quotes_dir = 'quotes'

if not os.path.exists(quotes_dir):
    os.makedirs(quotes_dir)

# scrape quotes from web
# for symbol in symbols:
#     get_quote_from_yahoo(symbol, quotes_dir)
#     break

# harvest data
for symbol in symbols:
    with open(os.path.join(quotes_dir, symbol)) as file:
        print(symbol)
        info = {}
        for line in file:
            res = parse_line(symbol, line)
            if res:
                info.update(res)
        print(info)
        break

# client = pymongo.MongoClient("mongodb+srv://")
# db = client["stocks"]
# col = db["yahoo"]

# for x in col.find({},{ "symbol": 0, "sector": 1, "industry": 1 }):
#   print(x)
# col.insert_one({'symbol':'test'})
# col.update_one({'symbol': 'test'}, {"$set" : {"52WeekLow": low, "52WeekHigh": high}})


# walk a dict to find a key - show path to get there
# def walk(d, root):
#     for key, val in d.items():
#         print(root, key)
#         if isinstance(val, dict):
#             walk(val, root + '/' + key)

