#!/bin/sh

BlocksURL=https://unicode.org/Public/12.1.0/ucd/Blocks-12.1.0d1.txt
UnicodeDataURL=https://unicode.org/Public/12.1.0/ucd/UnicodeData-12.1.0d2.txt

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
