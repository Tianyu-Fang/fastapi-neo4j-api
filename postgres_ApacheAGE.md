pull the postgresql image

```
docker pull apache/age
```

run postgresql in the container

```
docker run -d \
    --name postgres-age-container \
    --network my_network \
    --platform linux/amd64 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=yourpassword \
    -e POSTGRES_DB=postgresDB \
    -p 5455:5432 \
    apache/age

```

check if the container is running

```
docker ps
```

Connect to the postgres cli running on the container

```
docker exec -it postgres-age-container bash
```

```
psql -d postgresDB -U postgres
```

load the age extension

```
LOAD 'age';
SET search_path = ag_catalog, "$user", public;
```

Then we can create the graph and run cypher queries.
