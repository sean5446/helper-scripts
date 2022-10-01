#!/bin/bash

FLDR=garbage

mkdir $FLDR

# TODO: 101 is GB free on disk...

for i in {1..101}; do
    echo "Writing 1GB file $i of 101"
    dd if=/dev/zero of=$FLDR/zero-output$i bs=1M count=1024 &> /dev/null
done

echo "syncing"
sync
sleep 1

echo "removing files"
rm -rf $FLDR
sleep 1

sync
echo "syncing"
sleep 1

echo "done"
