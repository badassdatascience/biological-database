#
# useful libraries
#
import numpy as np
import pandas as pd
import pprint as pp

#
# user settings
#
number_of_papers_file = 'data/kevin/TestSetToTryGraphDatabase/NumberPapersPerCaGeneCombo-Table-1.csv'

throw_out = ['', 'LYNCH|GENE', 'multiple', 'MUTYH-Biallelic', 'MUTYH-Monoallelic', 'TGFBR1()6A']


#
# load data
#
df = pd.read_csv(number_of_papers_file)

#
# remove duplicate entries (based on disease capitalization, presense of whitespace)
#
data = {}
unique_diseases = {}
for gene_set, disease, count in zip(df['Gene'], df['BetterName'], df['CountOfBetterName']):
    if str(gene_set).lower() == 'nan':
        gene_set = ''

    gene_set = gene_set.strip()
    disease = disease.strip()
    disease = disease.lower()
    unique_diseases[disease] = {}

    if not gene_set in data:
        data[gene_set] = {}
    if not disease in data[gene_set]:
        data[gene_set][disease] = 0
    data[gene_set][disease] += count


#
# clean up gene set entries
#
cleaned_data = {}
unique_gene_symbols = {}
for gene_set in data.keys():

    if gene_set.strip() in throw_out:
        continue

    new_gene_set = gene_set.replace(' ', '|')
    new_gene_set = new_gene_set.replace(',', '|')
    new_gene_set = new_gene_set.replace('+', '|')
    new_gene_set = new_gene_set.replace('&', '|')
    new_gene_set = new_gene_set.replace('-', '|')
    new_gene_set = new_gene_set.replace('*', '')

    if new_gene_set == 'RAD51B|C|D':
        new_gene_set = 'RAD51B|RAD51C|RAD51D'

    new_gene_set_as_list = [x.strip() for x in new_gene_set.split('|') if x.strip() not in throw_out]
    new_gene_set_as_list = sorted(new_gene_set_as_list)
    if len(new_gene_set_as_list) == 0:
        continue

    for g in new_gene_set_as_list:
        unique_gene_symbols[g] = None

    key = ', '.join(new_gene_set_as_list)

    if not key in cleaned_data:
        cleaned_data[key] = {'diseases' : {}}
    for disease in data[gene_set].keys():
        if not disease in cleaned_data[key]['diseases']:
            cleaned_data[key]['diseases'][disease] = 0
        cleaned_data[key]['diseases'][disease] += data[gene_set][disease]

pp.pprint(cleaned_data)
#pp.pprint(unique_gene_symbols)




# EPCAM-MSH2 left alone


