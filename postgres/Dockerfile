FROM postgres:11

COPY backup.sql.gz .

RUN mkdir -p /docker-entrypoint-initdb.d

COPY ./initdb.sh /docker-entrypoint-initdb.d/initdb.sh
