#!/bin/bash

function start_service(){
		echo "Starting ssh Service"
		service ssh start
		echo "ssh Started"
}
start_service