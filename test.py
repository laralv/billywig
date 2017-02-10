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
# inputfiles are buffered into 64kb slices.
fileList = glob.glob('*')
fileMatchList = []
for fileHash in fileList:
    hashFileSha256 = hashlib.sha256()
    hashBufferSize = 65536
    with open(fileHash, 'rb') as f:
        while True:
            hashData = f.read(hashBufferSize)
            if not hashData:
                break
            hashFileSha256.update(hashData)
    if hashFileSha256.hexdigest() in config['applies_to']:
        fileMatchList.append(fileHash)
print(fileMatchList)
# Open file from config
## Trenger buffret innlesning
## Nå leser den hele filen inn i minnet før den splitter opp.
## Men kan vi buffre ebcdic når vi skal gjøre om til utf8?
recordsList = []
for fileMatch in fileMatchList:
    fileIn = open(fileMatch, 'rb').read().decode(config['input_charset'])
    recordsList.extend(map(''.join, zip(*[iter(fileIn)]*config['post_length'])))
fileIn = ''

record_jsonList = []
for record in recordsList:
    record_json = {}
    columnList = []
    columnList.extend(config['columns']['common'])
    columnList.extend(config['columns'][record[config['record_type']['start']:config['record_type']['end']]])
    for column in columnList:
        record_json[column['name']] = record[column['start']:column['end']]
    record_jsonList.append(record_json)
    
