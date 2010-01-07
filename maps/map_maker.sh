#!/bin/bash

if [ 4 -ne ${#@} ]; then
	echo "Usage: $0 [file_to_split] [floors] [width_in_px] [output_dir]"
	exit
fi

if [ ! -d $4 ]; then
	mkdir -p $4
fi

for i in $( seq 0 $(($2 - 1)) ); do
	echo "convert $1 -crop $3x30+0+$(($i * 30)) $4/$(($2 - $i)).png"
	convert $1 -crop $3x30+0+$(($i * 30)) $4/$(($2 - $i)).png
done
