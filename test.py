import ebcdic
import yaml
import re
import argparse

# Setting up argparse
parser = argparse.ArgumentParser(description='EBCDIC to-human-readable script')
parser.add_argument('--configfile', type=str, help='Path to config')
parser.add_argument('--outputfile', type=str, help='Output path')
sys_args = parser.parse_args()
if sys_args.configfile:
    config = yaml.safe_load(open(sys_args.configfile).read())
## Her trengs exception hvis config ikke eksisterer

# Open file from config
## trenger buffret innlesning
fileIn = open(config['fileName']).read().decode(config['format'])

recordsList = map(''.join, zip(*[iter(fileIn)]*config['length']))
fileIn = ''

## Skriv inn sjekk mot SHA

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
    print record_json

