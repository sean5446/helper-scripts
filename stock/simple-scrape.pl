#!/usr/bin/env perl

use strict;
use warnings;

my @symbols = qw/
AAPL
BEN
/;

my $user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36";
my $dir = 'quotes';
`mkdir -p $dir`;

my $i = 0;
my $count = scalar(@symbols);
for my $sym (@symbols) {
    $i++;
    print("$sym $i/$count\n");
    `wget -P "$dir" -U "$user_agent" "https://finance.yahoo.com/quote/$sym"`;
}

