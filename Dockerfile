FROM postgres:alpine

RUN apk update && apk add curl python3 py3-pip postgresql-dev gcc python3-dev musl-dev make libc-dev g++ git

RUN adduser -S python

ENV POSTGRES_USER python
ENV POSTGRES_PASSWORD python
ENV POSTGRES_DB python

USER postgres

RUN chmod 0700 /var/lib/postgresql/data

RUN chown postgres:postgres /run/postgresql/

RUN echo "host all  all    0.0.0.0/0  md5" >> /var/lib/postgresql/data/pg_hba.conf && echo "listen_addresses='*'" >> /var/lib/postgresql/data/postgresql.conf

RUN initdb -D /var/lib/postgresql/data && pg_ctl start -D /var/lib/postgresql/data

EXPOSE 5432
