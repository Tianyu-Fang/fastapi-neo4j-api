login to arbutus

```
ssh username@ipaddress
```

install docker

```
docker --version
sudo apt update && sudo apt install -y docker.io
docker --version
```

enable docker to start on boot

```
sudo systemctl enable --now docker
```

allow running docker without sudo

```
sudo usermod -aG docker $USER
```

test docker

```
docker run hello-world
```

check docker status

```
sudo systemctl status docker --no-pager
```

download latest Neo4j

```
docker pull neo4j
```

check if the image is downloaded

```
docker images
```

create folders for Neo4j

```
mkdir -p $HOME/neo4j/data
mkdir -p $HOME/neo4j/logs
mkdir -p $HOME/neo4j/conf
```

start Neo4j container

```
docker run -d \
    --name neo4j-container \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/password \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/conf:/conf \
    neo4j

```

verify if Neo4j is running

```
docker ps
```

access Neo4j from terminal

```
docker exec -it neo4j-container cypher-shell -u neo4j -p password
```

Stop the container:

```
docker stop neo4j-container
```

Restart the container:

```
docker restart neo4j-container
```

Remove the container:

```
docker rm neo4j-container
```

Delete all stored data:

```
rm -rf $HOME/neo4j
```
