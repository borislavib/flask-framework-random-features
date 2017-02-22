#!/usr/bin/env bash

# Truncate file
# This is a test file for storing the python processes

>f 


# Find all the busy python processes and ports
# Write them in a file 

(netstat -nlp | grep python | awk '{print $7}' | tr "/" " " | awk '{print $1}' >> f)


# Use the temp file with busy ports

file=./f


# Iterate through all the busy ports and kill them 
# This makes sure that it frees ports for the application

while IFS='' read -r line || [[ -n "$line" ]]; do
    kill -9 "$line"
done < "$file"

