#!/bin/sh

COLOR_RESET='\e[0m'
COLOR_GREEN='\e[0;32m';

echo "${COLOR_GREEN}building . . . ${COLOR_RESET}"
make -B

echo

echo "${COLOR_GREEN}testing . . . ${COLOR_RESET}"
for filename in ./test/*; do
	echo "${COLOR_GREEN}file: $filename${COLOR_RESET}"
	./build/pascal_parser "$filename"
done
