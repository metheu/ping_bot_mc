#!/usr/bin/env bash
set -e
# check that version number is given
if [ -z $1 ]
then
    echo "No version given as argument!" && exit 1
fi

# check if Docker file exists
if [ ! -e Dockerfile ]
then
    echo "Dockerfile not is root directory! Please make sure Dockerfile is present!" && exit 1
else
    echo "Dockerfile found! Starting to build image with version: $1 "

    docker build . -t matt/ping_bot:$1 

    echo "Docker image built! Stopping old container!" 
    
    contId="$(docker inspect --format="{{.Id}}" MCL_ping_bot)"

    echo "Old Container id is: $contId"

    docker stop $contId && docker rm $contId
    
    echo "Old container stopped! Launching new!" 
    
    docker run --name MCL_ping_bot -d --restart=unless-stopped matt/ping_bot:$1

    echo "New container deployed with image matt/ping_bot:$1" 
    
    sleep 5 &&

    if [  "$(docker inspect --format="{{.State.Status}}" MCL_ping_bot)" != "running" ]
    then
        echo "Something went wrong! Container not running!"
    else
        echo "All systems go!"
    fi
fi

