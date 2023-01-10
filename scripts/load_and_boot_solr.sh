#!/bin/bash

SOLR_DUMP_FILENAME="solr.tar.gz"

[ ! -z ${DO_LOAD} ] && \
    echo "Loading Solr dump file '$SOLR_DUMP_FILENAME" 
    scripts/download_solr.sh

tini -s -g -- /opt/solr/docker-entrypoint.sh 
