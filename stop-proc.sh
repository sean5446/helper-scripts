#!/bin/bash

ps aux | grep sqri | grep -v grep

PID=`ps aux | grep sqri | grep -v grep | awk -F" " '{print $2}'`

if [ -z "$PID" ]; then
  echo "no pid found?"
else
  echo "killing $PID ..."
  kill $PID
fi

sleep 1
ps aux | grep sqri | grep -v grep
