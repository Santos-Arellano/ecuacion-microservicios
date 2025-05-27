#!/bin/bash
# Reemplaza con tu usuario de Docker Hub
DOCKER_REGISTRY="santosaro"

# Build and push suma
docker build -t $DOCKER_REGISTRY/suma:1.0.0 ./suma
docker push $DOCKER_REGISTRY/suma:1.0.0
docker tag $DOCKER_REGISTRY/suma:1.0.0 $DOCKER_REGISTRY/suma:latest
docker push $DOCKER_REGISTRY/suma:latest

# Build and push resta
docker build -t $DOCKER_REGISTRY/resta:1.0.0 ./resta
docker push $DOCKER_REGISTRY/resta:1.0.0
docker tag $DOCKER_REGISTRY/resta:1.0.0 $DOCKER_REGISTRY/resta:latest
docker push $DOCKER_REGISTRY/resta:latest

# Build and push ecuacion
docker build -t $DOCKER_REGISTRY/ecuacion:1.0.0 ./ecuacion
docker push $DOCKER_REGISTRY/ecuacion:1.0.0
docker tag $DOCKER_REGISTRY/ecuacion:1.0.0 $DOCKER_REGISTRY/ecuacion:latest
docker push $DOCKER_REGISTRY/ecuacion:latest

# Build and push almacena
docker build -t $DOCKER_REGISTRY/almacena:1.0.0 ./almacena
docker push $DOCKER_REGISTRY/almacena:1.0.0
docker tag $DOCKER_REGISTRY/almacena:1.0.0 $DOCKER_REGISTRY/almacena:latest
docker push $DOCKER_REGISTRY/almacena:latest