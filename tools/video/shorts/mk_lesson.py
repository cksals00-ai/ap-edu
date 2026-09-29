import json,subprocess,sys,os
from PIL import Image,ImageDraw,ImageFont
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; BL='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; M='/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc'
F=lambda p,s:ImageFont.truetype(p,s,index=1)
BG=(255,246,233); TEAL=(23,138,122); NAVY=(27,42,74); W,H=1080,1920
def ctext(d,y,txt,font,fill,maxw=980):
    # wrap
    words=txt.split(' '); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur)
    lh=int(font.size*1.3)
    for i,l in enumerate(lines):
        d.text(((W-d.textlength(l,font=font))/2,y+i*lh),l,font=font,fill=fill)
    return len(lines)*lh
def build(spec):
    n=spec['name']; bd=f'build/{n}'; os.makedirs(bd,exist_ok=True)
    bg=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(bg)
    d.text((60,70),'HANGEUL CUBS',font=F(B,34),fill=TEAL)
    t='LEARN KOREAN'; d.text((W-60-d.textlength(t,font=F(B,30)),74),t,font=F(B,30),fill=(120,130,150))
    ctext(d,135,spec['title'],F(BL,76),NAVY)
    ctext(d,245,spec['sub'],F(M,40),TEAL)
    # footer
    d.rounded_rectangle((170,1660,910,1740),radius=40,fill=TEAL)
    ctext(d,1675,spec['footer'],F(B,36),(255,255,255),maxw=780)
    if spec.get('layout','A')=='B':
        OR=(224,138,50)
        d.rounded_rectangle((110,1110,970,1630),radius=40,fill=(255,251,243),outline=(236,214,186),width=3)
        rows=spec['card']
        if len(rows)==1:
            ctext(d,1230,rows[0][0],F(BL,190),OR); ctext(d,1500,rows[0][1],F(M,44),(110,110,110))
        else:
            y=1160
            for k,e in rows:
                d.text((190,y),k,font=F(BL,110),fill=OR); d.text((560,y+40),e,font=F(M,50),fill=(90,90,90)); y+=155
    bg.save(f'{bd}/bg.png')
    caps=[]
    for i,(a,b,txt) in enumerate(spec['caps']):
        im=Image.new('RGBA',(W,200),(0,0,0,0)); dd=ImageDraw.Draw(im)
        font=F(B,46); 
        # measure
        tmp=Image.new('RGBA',(W,200)); h=ctext(ImageDraw.Draw(tmp),0,txt,font,NAVY,maxw=940)
        y0=(200-h)//2
        dd.rounded_rectangle((40,y0-18,W-40,y0+h+10),radius=28,fill=(255,255,255,245),outline=(23,138,122,255),width=4)
        ctext(dd,y0-4,txt,font,NAVY,maxw=940)
        p=f'{bd}/cap{i}.png'; im.save(p); caps.append((a-spec['t0'],b-spec['t0'],p))
    dur=spec['t1']-spec['t0']
    inputs=['-loop','1','-i',f'{bd}/bg.png','-ss',str(spec['t0']),'-t',str(dur),'-i',spec['src']]
    for _,_,p in caps: inputs+=['-loop','1','-i',p]
    L=spec.get("layout","A")
    if L=="A": fc=["[1:v]crop=980:550:70:248,scale=1000:561[ch]","[1:v]crop=728:832:1112:148,scale=540:617[cd]","[0:v][ch]overlay=40:320[v0]","[v0][cd]overlay=270:1030[v1]"]
    else: fc=["[1:v]scale=1080:608[ch]","[0:v][ch]overlay=0:320[v1]"]
    last='v1'
    capy=872 if L=='A' else 905
    for i,(a,b,_) in enumerate(caps):
        fc.append(f"[{last}][{i+2}:v]overlay=0:{capy}:enable='between(t,{a:.2f},{b+0.35:.2f})'[c{i}]"); last=f'c{i}'
    fc.append(f"[{last}]trim=0:{dur},setpts=PTS-STARTPTS,fps=30,format=yuv420p[vout]")
    fc.append(f"[1:a]atrim=0:{dur},asetpts=PTS-STARTPTS,afade=t=in:d=0.08,afade=t=out:st={dur-0.4:.2f}:d=0.4,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    cmd=['ffmpeg','-v','error','-y']+inputs+['-filter_complex',';'.join(fc),'-map','[vout]','-map','[aout]','-t',str(dur),'-c:v','libx264','-preset','slow','-crf','18','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',f'out/{n}.mp4']
    subprocess.run(cmd,check=True)
    print(n, subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=width,height','-of','csv=p=0',f'out/{n}.mp4'],capture_output=True,text=True).stdout.replace('\n',' '))
specs=json.load(open(sys.argv[1]))
for s in specs:
    if len(sys.argv)<3 or s['name'] in sys.argv[2:]: build(s)
