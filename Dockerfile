###############################################
# Builder Image
###############################################
FROM alpine:latest as base

WORKDIR /tmp
RUN wget https://data.monarchinitiative.org/monarch-kg-dev/latest/solr.tar.gz && \
    tar -zxf solr.tar.gz

###############################################
# Production Image
###############################################

FROM solr:8 as prod
COPY --from=0 /tmp/data /var/solr

EXPOSE 8983
ENTRYPOINT ["/opt/docker-solr/scripts/docker-entrypoint.sh"]

