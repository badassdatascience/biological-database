#
# import useful libraries
#
import pprint as pp
import pickle
from neo4j import GraphDatabase
import sys

#
# user settings
#
output_directory = 'output'
chunk_size = 25000

load_all_synonyms = True
load_all_synonyms_to_tax_id = True

username = 'neo4j'
hostname = sys.argv[1]
password = sys.argv[2]
uri = 'bolt://' + hostname + ':7687'

#
# connect to Neo4j
#
driver = GraphDatabase.driver(uri, auth=(username, password))

#
# load our data structures
#
with open(output_directory + '/synonyms_to_gene_id.pickle', 'rb') as f:
    synonyms_to_gene_id = pickle.load(f)
with open(output_directory + '/synonyms_to_tax_id.pickle', 'rb') as f:
    synonyms_to_tax_id = pickle.load(f)

#########################
#   load all synonyms   #
#########################

if load_all_synonyms:

    #
    # clear the way (CRUDE)
    #
    cmd = 'MATCH (c:NCBI_GENE_SYNONYM)-[r]-() DELETE r;'
    with driver.session() as session:
        session.run(cmd)
    cmd = 'MATCH (c:NCBI_GENE_SYNONYM) DELETE c;'
    with driver.session() as session:
        session.run(cmd)
    
    #
    # make sure we know all the unique synonyms
    #
    all_synonyms = {}
    for syn in synonyms_to_gene_id.keys():
        all_synonyms[syn] = None
    for syn in synonyms_to_tax_id.keys():
        all_synonyms[syn] = None
    all_synonyms_list = []
    for syn in sorted(list(all_synonyms.keys())):
        all_synonyms_list.append([syn])

    #
    # report how many synonyms we are loading
    #
    print()
    print('We are loading ' + str(len(all_synonyms_list)) + ' gene synonym nodes.')
    print()

    #
    # transaction functions
    #
    def add_synonym_node(list_to_use):
        with driver.session() as session:
            session.write_transaction(create_synonym_node, list_to_use)

    def create_synonym_node(tx, list_to_use):
        cmd = 'UNWIND $list_to_use AS n CREATE (c:NCBI_GENE_SYNONYM {symbol : n[0]}) RETURN c;'
        tx.run(cmd, list_to_use=list_to_use)

    #
    # load all synonyms
    #
    chunks = [all_synonyms_list[x:x+chunk_size] for x in range(0, len(all_synonyms_list), chunk_size)]
    for i, ch in enumerate(chunks):
        add_synonym_node(ch)
        print('Added ' + str((i + 1) * chunk_size) + ' nodes.')
    print()

    #
    # create index on symbol
    #
    cmd = 'CREATE INDEX ON :NCBI_GENE_SYNONYM(symbol);'
    with driver.session() as session:
        session.run(cmd)



#####################################
#   link synonyms to taxonomy IDs   #
#####################################

if load_all_synonyms_to_tax_id:

    #
    # clear the way (CRUDE)
    #
    cmd = 'MATCH (c:NCBI_GENE_SYNONYM)-[r:HAS_NCBI_TAXONOMY]->(t:NCBI_TAXONOMY) DELETE r;'
    with driver.session() as session:
        session.run(cmd)
    
    #
    # organize list
    #
    link_list = []
    for syn in sorted(list(synonyms_to_tax_id.keys())):
        for tax_id in sorted(list(synonyms_to_tax_id[syn].keys())):
            link_list.append([syn, tax_id])

    #
    # report how many synonym to tax ID relationships we are loading
    #
    print()
    print('We are loading ' + str(len(link_list)) + ' gene synonym to taxonomy relationships.')
    print()

            
    #
    # transaction functions
    #
    def add_synonym_to_tax_id_relationship(list_to_use):
        with driver.session() as session:
            session.write_transaction(create_synonym_to_tax_id_relationship, list_to_use)

    def create_synonym_to_tax_id_relationship(tx, list_to_use):
        cmd = 'UNWIND $list_to_use AS n MATCH (gs:NCBI_GENE_SYNONYM), (t:NCBI_TAXONOMY) WHERE gs.symbol = n[0] and t.id = n[1] CREATE (gs)-[r:HAS_NCBI_TAXONOMY]->(t) RETURN gs, r, t'
        tx.run(cmd, list_to_use=list_to_use)

    #
    # load all synonym to tax ID links
    #
    chunks = [link_list[x:x+chunk_size] for x in range(0, len(link_list), chunk_size)]
    for i, ch in enumerate(chunks):
        add_synonym_to_tax_id_relationship(ch)
        print('Added ' + str((i + 1) * chunk_size) + ' relationships.')
    print()
        
#
# close Neo4j driver
#
driver.close()
