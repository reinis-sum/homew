#!/bin/bash

function start_service(){
		echo "Starting Apache2 Service"
		service apache2 start
		echo "Apache2 Started"
		echo "Starting ssh Service"
		service ssh start
		echo "ssh Started"
}
start_service