
#
# import useful libraries
#
import pprint as pp
import pickle

#
# user settings
#
gene_info_file = 'data/gene/gene_info'
output_directory = 'output'

#
# initialize data structures
#
synonyms_to_tax_id = {}

#
# iterate through each line in the gene_info file
#
f = open(gene_info_file)
for line in f:
    line = [x.strip() for x in line.split('\t')]

    tax_id = line[0]

    if tax_id == '#tax_id':
        continue

    tax_id = int(tax_id)
    gene_id = int(line[1])
    symbol = line[2]
    synonyms = line[4]
    type_of_gene = line[9]
    name = line[11]

    if symbol == '-':
        symbol = None
    if type_of_gene == '-':
        type_of_gene = None
    if name == '-':
        name = None

    cleaned_synonyms = [x for x in synonyms.split('|') if x != '-']
    for syn in cleaned_synonyms:
        if not syn in synonyms_to_tax_id:
            synonyms_to_tax_id[syn] = {}
        synonyms_to_tax_id[syn][tax_id] = None

f.close()

#
# save our newly loaded data structures
#
with open(output_directory + '/synonyms_to_tax_id.pickle', 'wb') as f:
    pickle.dump(synonyms_to_tax_id, f)



