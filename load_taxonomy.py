#
# import useful libraries
#
import pprint as pp
import pickle
from neo4j.v1 import GraphDatabase
import sys

#
# user settings
#
names_file = 'data/taxonomy/names.dmp'
uri = 'bolt://localhost:7687'
username = 'neo4j'
password = sys.argv[1]

#
# load names file
#
names_info = {}
f = open(names_file)
for line in f:
    line = [x.strip() for x in line.split('|')]
    tax_id = int(line[0])
    name = line[1]
    name_type = line[3]

    if name_type != 'scientific name':
        continue

    if name in ['', '-']:
        name = None

    names_info[tax_id] = name

f.close()

#
# reorganize in a format useful for bulk Neo4j load
#
names_list = []
for tax_id in sorted(names_info.keys()):
    names_list.append([tax_id, names_info[tax_id]])

#
# connect to Neo4j
#
driver = GraphDatabase.driver(uri, auth=(username, password))

#
# transaction functions
#
def add_node(list_to_use):
    with driver.session() as session:
        session.write_transaction(create_node, list_to_use)

def create_node(tx, list_to_use):
    cmd = 'UNWIND $list_to_use AS n CREATE (c:NCBI_TAXONOMY {id : n[0], name : n[1]}) RETURN c;'
    tx.run(cmd, list_to_use=list_to_use)

#
# clear the way (CRUDE)
#
cmd = 'MATCH (c:NCBI_TAXONOMY)-[r]-() DELETE r;'
with driver.session() as session:
    session.run(cmd)
cmd = 'MATCH (c:NCBI_TAXONOMY) DELETE c;'
with driver.session() as session:
    session.run(cmd)

#
# load database
#
add_node(names_list)

#
# Make indices on id and name
#
cmd = 'CREATE INDEX ON :NCBI_TAXONOMY(id);'
with driver.session() as session:
    session.run(cmd)
cmd = 'CREATE INDEX ON :NCBI_TAXONOMY(name);'
with driver.session() as session:
    session.run(cmd)

#
# close Neo4j driver
#
driver.close()

