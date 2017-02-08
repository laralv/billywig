#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ebcdic
import yaml
import re
import argparse
import glob
import hashlib

# Setting up argparse
parser = argparse.ArgumentParser(description='EBCDIC to-human-readable script')
parser.add_argument('--configfile', type=str, help='Path to config')
parser.add_argument('--output', type=str, help='Output path')
sys_args = parser.parse_args()
if sys_args.configfile:
    config = yaml.safe_load(open(sys_args.configfile).read())
## Her trengs exception hvis config ikke eksisterer

# Checking hashes against files in folder. 
fileList = glob.glob('*')
fileMatchList = []
for fileHash in fileList:
    if hashlib.sha256(open(fileHash, 'rb').read()).hexdigest() in config['applies_to']:
        fileMatchList.append(fileHash)
print(fileMatchList)
# Open file from config
## Trenger buffret innlesning
## Nå leser den hele filen inn i minnet før den splitter opp.
recordsList = []
for fileMatch in fileMatchList:
    fileIn = open(fileMatch, 'rb').read().decode(config['input_charset'])
    recordsList.extend(map(''.join, zip(*[iter(fileIn)]*config['post_length'])))
fileIn = ''

for record in recordsList:
    record_json = {}
    for column in config['columns']:
        if column['columnStart'] is None:
            continue
        if column['columnCondition'] is not None:
            if type(column['columnCondition']) == list:
                for condition in column['columnCondition']:
                    if record[condition['columnConditionStart']:condition['columnConditionEnd']] == condition['columnConditionCondition']:
                            record_json[column['columnName']] = record[column['columnStart']:column['columnEnd']]
            else:
                if record[column['columnCondition']['columnConditionStart']:column['columnCondition']['columnConditionEnd']] == column['columnCondition']['columnConditionCondition']:
                    record_json[column['columnName']] = record[column['columnStart']:column['columnEnd']]
            continue
        record_json[column['columnName']] = record[column['columnStart']:column['columnEnd']]
    print(record_json)

