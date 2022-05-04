#!/bin/bash  
for x in $*; do  
  head -$COPYRIGHTLEN $x | diff copyright.txt - || ( ( cat copyright.txt; echo; cat $x) > /tmp/file;  
  mv /tmp/file $x )
done 


# example of copyright.txt:

# (Copyright) 2021 Company, Inc.
# Apache License Version 2.0 (see LICENSE for details)
