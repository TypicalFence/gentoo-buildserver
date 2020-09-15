#!/bin/bash

dir=$(dirname "$0")

while read -r line
do
    emerge --sync "$line"
done <<< $(./$dir/get_repos.py /etc/portage/repos.conf)
