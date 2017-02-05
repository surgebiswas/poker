#!/bin/bash
grep wins gamelog.txt | cut -f 1,5 -d " " | sed 's/(//g' | sed 's/)//g' | sed 's/P//g' > gamelog.txt.wins
