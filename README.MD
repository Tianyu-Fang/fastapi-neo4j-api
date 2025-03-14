start neo4j-container

```
docker start neo4j-container
```

start postgres-age-container

```
docker start postgres-age-container
```

Rebuild and Restart FastAPI

```
docker build -t fastapi-neo4j-api .
docker run -d \
    --name fastapi-container \
    --network my_network \
    -p 8000:8000 \
    fastapi-neo4j-api
```

start fastapi-container

```
docker start fastapi-container
```

check running containers

```
docker ps
```

test API request with the FastAPI server running inside the Docker container

```
http POST http://localhost:8000/cypher query="MATCH (n) RETURN n"
```
