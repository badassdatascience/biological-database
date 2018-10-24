# biological-database

This is basically where I'm collecting all my Neo4j code for making general purpose, non-proprietary biological databases.

I started with NCBI's taxonomy and gene data.

## How to run this

```
mkdir output
mkdir output/gene_lists
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

python3 load_taxonomy.py localhost "password"
python3 preprocess_gene_info.py
python3 load_gene.py localhost "password"
python3 load_and_link_synonyms.py localhost "password"
```

## Useful queries

### Boring queries

Find the taxonomy node for human:

```
MATCH (c:NCBI_TAXONOMY) WHERE c.id = 9606 RETURN c;
```

Find the taxonomy node for human, which specific attributes:
```
MATCH (c:NCBI_TAXONOMY) WHERE c.id = 9606 RETURN c.id AS NCBI_taxonomy_id, c.name AS scientific_name;
```

Find the NCBI gene synonym node 'A1B':
```
MATCH (n:NCBI_GENE_SYNONYM) WHERE n.symbol = "A1B" RETURN n;
```

### Slightly more interesting queries

```
MATCH (g:NCBI_GENE)-[r2]->(gs:NCBI_GENE_SYNONYM)-[r]->(t:NCBI_TAXONOMY) WHERE gs.symbol = "A1B" AND t.id = 9606 RETURN gs, r, t, g, r2;
```

