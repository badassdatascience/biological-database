#
# import useful libraries
#
import pprint as pp
import pickle

#
# user settings
#
output_directory = 'output'

#
# load our data structures
#
with open(output_directory + '/gene_info.pickle', 'rb') as f:
    gene_info = pickle.load(f)
with open(output_directory + '/synonyms_to_tax_id.pickle', 'rb') as f:
    synonyms_to_tax_id = pickle.load(f)

    
