#!/usr/bin/env bash
wget -nv -r --spider -i $1 2>&1 | egrep " URL:" | awk '{ print $3 }' | sed " s@URL :@@g" >> korpus_link_liste.txt
