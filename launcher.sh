#!/bin/bash

POS_DIR=.
BASE_PORT=2612
DEFAULT_SERVERS_NUMBER=1

function start() {
    cd $POS_DIR
    i=0
    while [ $i -lt $1 ]
    do
        port=$(( $BASE_PORT + $i ));
        echo "Starting instance in port $port"
        nohup python3 entity_service.py $port > logs/entity_service.$port.log 2>&1 &
        i=$(( $i + 1 ))
    done
}

function stop() {
    ps -ef | grep "entity_service" | grep -v grep | awk '{print $2}'| xargs kill -9
}


case "$1" in
    start)
        if [ "$2" ]
        then
            start $2
        else
            start $DEFAULT_SERVERS_NUMBER
        fi
        ;;
    stop)
        stop
        ;;
    *)
        echo "Usage: $0 (start|stop)"
        ;;
esac
exit 0
