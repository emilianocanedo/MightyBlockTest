#!/bin/bash

echo "arg: $1"
case $1 in

  local)
	cd /code/ || exit
	PYTHONPATH=$PYTHONPATH:src/ python bin/run.py
  ;;

  *)
	echo "DEFAULT!"
	cd /code/ || exit
	PYTHONPATH=$PYTHONPATH:src/ python bin/run.py
  ;;

esac