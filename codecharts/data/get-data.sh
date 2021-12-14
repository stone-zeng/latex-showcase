#!/bin/sh

BlocksURL=https://unicode.org/Public/14.0.0/ucd/Blocks.txt
UnicodeDataURL=https://unicode.org/Public/14.0.0/ucd/UnicodeData.txt

if [ "$1" == "-f" ]; then
    curl $BlocksURL      -o Blocks.txt
    curl $UnicodeDataURL -o UnicodeData.txt
else
    if [ ! -f Blocks.txt ]; then
        curl $BlocksURL -o Blocks.txt
    fi
    if [ ! -f UnicodeData.txt ]; then
        curl $UnicodeDataURL -o UnicodeData.txt
    fi
fi
