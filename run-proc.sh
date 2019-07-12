#!/bin/bash

# scp target/sqri-1.0.0-SNAPSHOT-uncommitted.jar lxsinttest01:~/sqri/

echo cleaning log file...
rm -f nohup.out

echo starting sqri server...
#nohup java -jar sqri-1.0.0-SNAPSHOT-uncommitted.jar server sqri.staging.yml &
nohup java -jar sqri-1.0.0-SNAPSHOT-uncommitted.jar server sqri.production.yml &

echo sleeping 1
sleep 1
rm log_IS_UNDEFINED
tailf nohup.out
