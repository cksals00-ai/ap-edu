#!/bin/bash
# 한글컵스 본편 포장: [스팅 3초] + [본편] + [엔드카드 12초]  (쇼츠 제외)
# ./cubs_wrap.sh <본편.mp4> <스팅.mp4> <엔드카드.mp4> <출력.mp4> [자막.srt]
# - 본편의 fps·해상도에 맞춰 스팅/엔드카드를 변환해 이어 붙인다. 음량은 -14 LUFS로 맞춘다.
# - 자막이 있으면 +3.000초 밀어서 <출력>.srt 로 저장한다. 설명란 챕터도 전부 +0:03 해야 한다(첫 챕터 0:00 Intro 추가).
set -e; L=$1; S=$2; O=$3; OUT=$4; SRT=$5
fps=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$L")
ffmpeg -y -loglevel error -i "$S" -i "$L" -i "$O" -filter_complex "\
[0:v]fps=$fps,scale=1920:1080,setsar=1,format=yuv420p[v0];[1:v]fps=$fps,scale=1920:1080,setsar=1,format=yuv420p[v1];[2:v]fps=$fps,scale=1920:1080,setsar=1,format=yuv420p[v2];\
[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];[2:a]aresample=48000,aformat=channel_layouts=stereo[a2];\
[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a0x];[a0x]loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUT"
if [ -n "$SRT" ]; then python3 - "$SRT" "${OUT%.mp4}.srt" <<'PY'
import re,sys
def sh(m):
    h,mi,s,ms=map(int,m.groups()); t=((h*60+mi)*60+s)*1000+ms+3000
    return f"{t//3600000:02d}:{t//60000%60:02d}:{t//1000%60:02d},{t%1000:03d}"
src=open(sys.argv[1],encoding='utf-8').read(); open(sys.argv[2],'w',encoding='utf-8').write(re.sub(r'(\d\d):(\d\d):(\d\d),(\d\d\d)',sh,src))
PY
fi
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
