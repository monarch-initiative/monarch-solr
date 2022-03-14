# Relation Graph / BigQuery Join 


### Create the table

172800 is 2 days for the expiration time

```bash=
bq mk --dataset --default_table_expiration 172800 --default_partition_expiration 172800 monarch-initiative:monarch_kg
```


### Set up the schema
```bash=
NODE_SCHEMA=id:STRING,name:STRING
EDGE_SCHEMA=$(gsutil cat -r 0-500 gs://monarch-ingest/202203/monarch-kg_edges.tsv | head -1 | tr '\t' '\n' | xargs -I {} echo {}:STRING | tr '\n' ',' | sed 's/.$//')
RELATION_SCHEMA=subject:STRING,predicate:STRING,object:STRING
```

### Load the data
```bash=
bq load --source_format=CSV --field_delimiter="\t" --schema=$EDGE_SCHEMA  monarch_kg.edges gs://monarch-ingest/202203/monarch-kg_edges.tsv
bq load --source_format=CSV --quote "" --field_delimiter="\t" --schema=id:STRING,name:STRING  monarch_kg.nodes gs://monarch-ingest/202203/monarch-kg_node_names.tsv
bq load --source_format=CSV --field_delimiter="\t" --schema=$RELATION_SCHEMA monarch_kg.relations gs://monarch-ingest/202203/monarch-ontology-relations-non-redundant.tsv
```


### BigQuery aggregate & join

```bash=
bq query --use_legacy_sql=false \
'SET @@dataset_id = "monarch_kg";

CREATE OR REPLACE TEMP TABLE
closure 
(
    id STRING,
    ancestors STRING
);

insert into closure (id, ancestors)
select subject, STRING_AGG(object,"|") 
from relations 
group by subject;


ALTER TABLE edges
  ADD COLUMN IF NOT EXISTS subject_closure STRING,
  ADD COLUMN IF NOT EXISTS object_closure STRING;

update edges
set subject_closure = ancestors 
from closure
where edges.subject = closure.id;

update edges
set object_closure = ancestors 
from closure
where edges.object = closure.id;'
```

### Write the edge table back to gcloud
```bash=
bq extract --destination_format CSV --field_delimiter "\t" monarch_kg.edges "gs://monarch-ingest/202203/edges_with_closure/monarch-kg_edges_*.kgx"
```




## Details & process



```bash=
time relation-graph/target/universal/stage/bin/relation-graph --ontology-file monarch-ontology-final.owl --redundant-output-file monarch-ontology-relations-redundant.tsv --non-redundant-output-file monarch-ontology-relations-non-redundant.tsv --mode tsv --reflexive-subclasses true --equivalence-as-subclass true --property "rdfs:subClassOf" 
```

16 minutes, 61M file for non-redundant, 645M for redundant 


```
kschaper@kevin-ubuntu-tmp:~$ grep ZFA:0000042 monarch-ontology-relations-non-redundant.tsv
ZFA:0000042	rdfs:subClassOf	ZFA:0000037
ZFA:0000042	rdfs:subClassOf	ZFA:0001689
ZFA:0000042	rdfs:subClassOf	UBERON:0003052
ZFA:0000042	rdfs:subClassOf	ZFA:0000042
```

```
kschaper@kevin-ubuntu-tmp:~$ grep ZFA:0000042 monarch-ontology-relations-redundant.tsv
ZFA:0000042	rdfs:subClassOf	UBERON:0000015
ZFA:0000042	rdfs:subClassOf	UBERON:0000465
ZFA:0000042	rdfs:subClassOf	ZFA:ENTITY
ZFA:0000042	rdfs:subClassOf	UBERON:0001062
ZFA:0000042	rdfs:subClassOf	ZFA:0000037
ZFA:0000042	rdfs:subClassOf	BFO:0000040
ZFA:0000042	rdfs:subClassOf	BFO:0000001
ZFA:0000042	rdfs:subClassOf	CARO:0000006
ZFA:0000042	rdfs:subClassOf	ZFA:0000042
ZFA:0000042	rdfs:subClassOf	UBERON:0000061
ZFA:0000042	rdfs:subClassOf	ZFA:0100000
ZFA:0000042	rdfs:subClassOf	GENO:0000904
ZFA:0000042	rdfs:subClassOf	BFO:0000141
ZFA:0000042	rdfs:subClassOf	UBERON:0004121
ZFA:0000042	rdfs:subClassOf	CARO:0030000
ZFA:0000042	rdfs:subClassOf	BFO:0000004
ZFA:0000042	rdfs:subClassOf	BFO:0000002
ZFA:0000042	rdfs:subClassOf	ZFA:0001689
ZFA:0000042	rdfs:subClassOf	CARO:0000000
ZFA:0000042	rdfs:subClassOf	UBERON:0006800
ZFA:0000042	rdfs:subClassOf	UBERON:0003052
ZFA:0000042	rdfs:subClassOf	UBERON:0007651
ZFA:0000042	rdfs:subClassOf	UBERON:0010314
ZFA:0000042	rdfs:subClassOf	CARO:0000003
ZFA:0000042	rdfs:subClassOf	UBERON:0000466
```

```
gsutil cp monarch-ontology-relations*.tsv gs://monarch-ingest/
```

## loading edges, nodes & relations into bigquery

### create the database with a 2 hour timeout, and try loading tsv

```bash=
bq mk --dataset --default_table_expiration 7200 --default_partition_expiration 7200 monarch-initiative:monarch_kg
```

shenanigans and tomfoolery to make a schema from the first line
```bash=

NODE_SCHEMA=$(gsutil cat -r 0-500 gs://monarch-ingest/monarch-kg_nodes.tsv | head -1 | tr '\t' '\n' | xargs -I {} echo {}:STRING | tr '\n' ',' | sed 's/.$//')
EDGE_SCHEMA=$(gsutil cat -r 0-500 gs://monarch-ingest/monarch-kg_edges.tsv | head -1 | tr '\t' '\n' | xargs -I {} echo {}:STRING | tr '\n' ',' | sed 's/.$//')
RELATION_SCHEMA=subject:STRING,predicate:STRING,object:STRING

```


Try loading 

```bash=
bq load --source_format=CSV --field_delimiter="\t" --schema=$EDGE_SCHEMA  monarch_kg.edges gs://monarch-ingest/monarch-kg_edges.tsv
```

edges load fine, but for nodes it complains about a row with 24 columns....that I can't find using awk to count tabs

### Let's try jsonlines!

no, it doesn't like the way xrefs are nested.

### Let's try cut!

We really only need node id and name, and maybe that gets us past the fields that are making the bq loader unhappy

```bash=
cut -f 1,3 monarch-kg_nodes.tsv > monarch-kg_node_names.tsv
gsutil cp monarch-kg_node_names.tsv gs://monarch-ingest/202203/
```

```bash=
bq load --source_format=CSV --quote "" --field_delimiter="\t" --schema=id:STRING,name:STRING  monarch_kg.nodes gs://monarch-ingest/202203/monarch-kg_node_names.tsv
```

After telling it that double quotes aren't for quoting fields, it worked!

### Now load relations

```bash=
bq load --source_format=CSV --field_delimiter="\t" --schema=$RELATION_SCHEMA monarch_kg.relations gs://monarch-ingest/202203/monarch-ontology-relations-redundant.tsv


```



