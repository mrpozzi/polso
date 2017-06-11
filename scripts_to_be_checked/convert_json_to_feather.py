import feather
import pandas as pd
import json

## Initiate file names
file_prefix = "amis_articles"
version = '27_07_2016'
input_file_name='{0}_{1}.jsonl'.format(file_prefix, version)

## Read json data
print "Reading data from '{0}' ...".format(input_file_name)
with open(input_file_name) as f:
    articles = pd.DataFrame(json.loads(line) for line in f)

## Write to file in feather format
##
## NOTE (Michael): This enables the transition between Python and R to be
## easier.
output_file_name = '{0}_{1}.feather'.format(file_prefix, version)
feather.write_dataframe(articles, output_file_name)

print "File written to '{0}'".format(output_file_name)
