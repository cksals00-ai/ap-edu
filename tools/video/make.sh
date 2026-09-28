#!/bin/bash
# ./make.sh <name> "<page?query>" <dur> <audio.wav> [fps]  → ../out/<name>.mp4
set -e; name=$1; page=$2; dur=$3; aud=$4; fps=${5:-30}; d=/tmp/fr_$name; rm -rf $d; mkdir -p $d ../out
for w in 0 1 2 3 4 5; do node render.mjs "$page" $fps $dur $d $w 6 & done; wait
ffmpeg -y -loglevel error -framerate $fps -i $d/f_%04d.png -i $aud -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -r $fps -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart ../out/$name.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 ../out/$name.mp4
