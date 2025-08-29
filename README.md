# Project Chat

To run this project, you need [docker](https://docs.docker.com/get-started/get-docker/)

First, replace the path in dockerfile with where the project is located

Create a network, this application needs redis so you need to make sure this django app works with redis

```
docker network create testnet
```

Build the django application

```
docker build -t project_chat .
```

Run redis in the network

```
docker run -d --network testnet redis
```

Run the django app

```
docker run -d --network testnet -p 8000:8000 project_chat
```