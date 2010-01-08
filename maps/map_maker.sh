#!/bin/bash

if [ 4 -ne ${#@} ]; then
	echo "Usage: $0 [file_to_split] [floors] [width_in_px] [output_dir]"
	echo "Example: $0 default/day.jpg 110 2000 default/day"
	exit
fi

if [ ! -d $4 ]; then
	mkdir -p $4
fi

for i in $( seq 0 $(($2 - 1)) ); do
	echo "convert $1 -quality 85 -crop $3x30+0+$(($i * 30)) $4/$(($2 - $i)).jpg"
	convert $1 -quality 85 -crop $3x30+0+$(($i * 30)) $4/$(($2 - $i)).jpg
done
