
#
# import useful libraries
#
import pprint as pp

#
# user settings
#
tax_id_to_keep = [9606]

#
# read the source file
#
gene_id_to_pubmed_id = {}
unique_pubmed_ids = {}
f = open('data/gene/gene2pubmed')
for line in f:
    line = [x.strip() for x in line.split('\t') if x.strip() != '']
    if line[0] == '#tax_id':
        continue

    tax_id = int(line[0])
    if not tax_id in tax_id_to_keep:
        continue

    gene_id = int(line[1])
    pubmed_id = int(line[2])
    
    if not gene_id in gene_id_to_pubmed_id:
        gene_id_to_pubmed_id[gene_id] = {}
    gene_id_to_pubmed_id[gene_id][pubmed_id] = None

    unique_pubmed_ids[pubmed_id] = None
    
f.close()


#pp.pprint(gene_id_to_pubmed_id)
pp.pprint(unique_pubmed_ids)
