#!/bin/bash

# usage: find ~/src/trade-engine/src/com/company/webservices/rest/v2 -name "*.java" | xargs zsh test.sh

for x in $*; do
  head -n 5 $x | grep -qi "copyright";
  if [[ $? -eq 1 ]]; then
    echo "Adding copyright: $x";
    (cat copyright.txt; echo; cat $x) > /tmp/file; mv /tmp/file $x
  fi
done

# example of copyright.txt:

# (Copyright) 2021 Company, Inc.
# Apache License Version 2.0 (see LICENSE for details)
