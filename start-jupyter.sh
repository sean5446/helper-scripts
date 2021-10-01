#!/usr/bin/env bash

source ~/vjup/bin/activate
/activate
notebook_home='/home/queso/notebooks'

nohup jupyter lab --NotebookApp.token='' --no-browser $notebook_home  > jup.log &
