pipeline {
  agent {
    node {
      label 'worker'
    }

  }
  stages {
    stage('prepare tsv bucket') {
      steps {
        sh '''gsutil cp gs://monarch-ingest/$RELEASE/monarch-kg.tar.gz .
tar zxf monarch-kg.tar.gz
cut -f 1,3 monarch-kg_nodes.tsv > monarch-kg_node_names.tsv

gsutil cp gs://monarch-ingest/monarch-ontology-relations-non-redundant.tsv .

bq mk --dataset --default_table_expiration 172800 --default_partition_expiration 172800 monarch-initiative:monarch_kg || true

gsutil -m cp -J monarch-kg_edges.tsv  monarch-kg_node_names.tsv  monarch-kg_nodes.tsv  monarch-ontology-relations-non-redundant.tsv gs://monarch-ingest/$RELEASE/

'''
      }
    }

    stage('load the data') {
      steps {
        sh '''NODE_SCHEMA=id:STRING,name:STRING
EDGE_SCHEMA=$(gsutil cat -r 0-500 gs://monarch-ingest/$RELEASE/monarch-kg_edges.tsv | head -1 | tr \'\\t\' \'\\n\' | xargs -I {} echo {}:STRING | tr \'\\n\' \',\' | sed \'s/.$//\')
RELATION_SCHEMA=subject:STRING,predicate:STRING,object:STRING

bq load --source_format=CSV --field_delimiter="\\t" --schema=$EDGE_SCHEMA  monarch_kg.edges gs://monarch-ingest/$RELEASE/monarch-kg_edges.tsv
bq load --source_format=CSV --quote "" --field_delimiter="\\t" --schema=id:STRING,name:STRING  monarch_kg.nodes gs://monarch-ingest/$RELEASE/monarch-kg_node_names.tsv
bq load --source_format=CSV --field_delimiter="\\t" --schema=$RELATION_SCHEMA monarch_kg.relations gs://monarch-ingest/$RELEASE/monarch-ontology-relations-non-redundant.tsv

'''
      }
    }

    stage('aggregate and export') {
      steps {
        sh '''bq query --use_legacy_sql=false \\
\'SET @@dataset_id = "monarch_kg";

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
where edges.object = closure.id;\'

bq extract --destination_format CSV --field_delimiter "\\t" monarch_kg.edges "gs://monarch-ingest/$RELEASE/edges_with_closure/monarch-kg_edges_*.kgx"'''
      }
    }

    stage('start solr & index') {
      steps {
        sh '''lsolr start-server --core edges --schema edges.yaml --container monarch-solr
sleep 30
lsolr bulkload -C edges -s edges.yaml tsv/monarch-kg_edges_with_*.tsv
docker cp monarch-solr:/var/solr/data .
tar czf solr.tgz data
gsutil cp solr.tgz gs://monarch-ingest/$RELEASE/
'''
      }
    }

  }
  environment {
    RELEASE = '202203.2'
  }
}