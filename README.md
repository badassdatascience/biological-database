# biological-database

This is basically where I'm collecting all my Neo4j code for making general purpose, non-proprietary biological databases.

I started with NCBI's taxonomy and gene data.

## How to run this

```
mkdir output
mkdir data

cd data
mkdir taxonomy
cd taxonomy
wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
gunzip taxdump.tar.gz 
tar -xf taxdump.tar 
gzip taxdump.tar 
cd ..
cd ..

cd data
mkdir gene
cd gene
wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz
gunzip gene_info.gz
cd ..
cd ..

./packages/neo4j-community-3.3.3/bin/neo4j start

python3 load_taxonomy.py

python3 load_gene.py
```
