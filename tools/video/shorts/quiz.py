import numpy as np, wave, subprocess, os, math
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1080,1920,30
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; BL='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; M='/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc'
F=lambda p,s:ImageFont.truetype(p,s,index=1)
BG=(18,28,52); INK=(255,255,255); SUB=(170,184,210); TEAL=(38,196,166); CORAL=(255,122,92); TILE=(33,47,84)
def ct(d,y,t,f,fill): d.text(((W-d.textlength(t,font=f))/2,y),t,font=f,fill=fill)
R0=2.5; RL=5.6
rounds=[('ya',['ㅏ','ㅑ'],['AH','YA'],1),('ah',['ㅏ','ㅑ'],['AH','YA'],0),('yagu',['아구','야구'],['agu','yagu'],1)]
END=R0+RL*3; TOTAL=END+3.2
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
os.makedirs('q/fr',exist_ok=True)
for i in range(int(TOTAL*FPS)):
    t=i/FPS; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.text((70,90),'HANGEUL CUBS',font=F(B,34),fill=TEAL); tt='KOREAN LISTENING QUIZ'; d.text((W-70-d.textlength(tt,font=F(B,30)),94),tt,font=F(B,30),fill=SUB)
    if t<R0:
        a=ease(t/0.5)
        ct(d,560-40*(1-a),'Can you hear it?',F(B,64),SUB)
        ct(d,700,'ㅏ  or  ㅑ ?',F(BL,190),INK)
        ct(d,1010,'3 rounds · Korean for beginners',F(M,46),SUB)
        ct(d,1090,'Guess before the answer.',F(M,46),TEAL)
    elif t<END:
        k=int((t-R0)//RL); lt=(t-R0)-k*RL; clip,ch,ro,ans=rounds[k]
        ct(d,300,f'ROUND {k+1} / 3',F(B,48),TEAL)
        ct(d,380,'Listen. Which one did you hear?',F(M,48),SUB)
        # speaker pulse
        pulse=0
        for s0 in (0.4,1.7):
            if s0<=lt<=s0+0.8: pulse=math.sin((lt-s0)/0.8*math.pi)
        r=90+30*pulse; cx,cy=W//2,600
        d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(38,196,166) if pulse>0 else (40,58,100))
        d.polygon([(cx-38,cy-22),(cx-12,cy-22),(cx+18,cy-50),(cx+18,cy+50),(cx-12,cy+22),(cx-38,cy+22)],fill=INK)
        # tiles
        rev=lt>=4.2
        for j in range(2):
            x0=100+j*460; y0=820; x1=x0+420; y1=y0+560
            col=TILE; out=None
            if rev: col=(28,120,104) if j==ans else (30,40,66)
            d.rounded_rectangle((x0,y0,x1,y1),radius=48,fill=col,outline=(TEAL if (rev and j==ans) else (60,78,120)),width=6)
            fs=250 if len(ch[j])==1 else 170
            tf=F(BL,fs); tw=d.textlength(ch[j],font=tf); d.text((x0+(420-tw)/2,y0+(80 if fs==250 else 150)),ch[j],font=tf,fill=INK if (not rev or j==ans) else (110,122,150))
            rf=F(B,56); rw=d.textlength(ro[j],font=rf); d.text((x0+(420-rw)/2,y0+430),ro[j],font=rf,fill=SUB if not rev else (INK if j==ans else (110,122,150)))
            if rev and j==ans:
                d.ellipse((x1-70,y0-30,x1+10,y0+50),fill=TEAL); d.line([(x1-48,y0+10),(x1-32,y0+28),(x1-8,y0-6)],fill=INK,width=10)
        # countdown
        if 2.3<=lt<4.2:
            n=3-int((lt-2.3)/0.633); n=max(1,n)
            ct(d,1450,str(n),F(BL,150),CORAL)
        elif rev:
            ct(d,1470,'Answer: '+ch[ans]+' ('+ro[ans]+')',F(B,60),TEAL)
        # progress bar
        d.rounded_rectangle((100,1700,980,1716),radius=8,fill=(40,58,100))
        d.rounded_rectangle((100,1700,100+880*min(1,lt/RL),1716),radius=8,fill=TEAL)
    else:
        lt=t-END; a=ease(lt/0.5)
        ct(d,620,'How many did you get?',F(B,72),INK)
        ct(d,760,'1/3 · 2/3 · 3/3',F(BL,110),TEAL)
        ct(d,940,'Tell us in the comments.',F(M,52),SUB)
        ct(d,1120,'Free lessons: Hangeul Cubs',F(B,52),INK)
        ct(d,1200,'ㅏ ㅑ ㅓ ㅕ ㅗ',F(BL,90),CORAL)
    im.save(f'q/fr/f_{i:04d}.png')
# audio
sr=48000; N=int(TOTAL*sr); mix=np.zeros(N)
def load(n):
    w=wave.open(f'q/{n}.wav'); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16)/32768.0; return a
clips={'ah':load('ah')[int(0.05*sr):int(0.65*sr)],'ya':load('ya')[int(0.2*sr):int(0.95*sr)],'yagu':load('yagu')[int(0.18*sr):int(1.3*sr)]}
def put(a,t,g=1.0):
    s=int(t*sr); e=min(N,s+len(a)); f=np.ones(len(a)); fl=int(0.01*sr); f[:fl]=np.linspace(0,1,fl); f[-fl:]=np.linspace(1,0,fl)
    mix[s:e]+=(a*f)[:e-s]*g
def tone(fr,d,g=0.25):
    tt=np.arange(int(d*sr))/sr; env=np.exp(-tt*18); return np.sin(2*np.pi*fr*tt)*env*g
put(tone(660,0.35,0.2),0.1); put(tone(880,0.35,0.2),0.25)
for k,(clip,_,_,_) in enumerate(rounds):
    T=R0+k*RL
    put(clips[clip],T+0.4,1.3); put(clips[clip],T+1.7,1.3)
    for c in range(3): put(tone(1000,0.08,0.18),T+2.3+c*0.633)
    put(tone(784,0.25,0.22),T+4.2); put(tone(1175,0.4,0.22),T+4.32)
put(tone(523,0.4,0.2),END); put(tone(659,0.4,0.2),END+0.12); put(tone(784,0.6,0.2),END+0.24)
mix=np.clip(mix,-1,1); w=wave.open('q/quiz.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((mix*32767).astype(np.int16).tobytes()); w.close()
subprocess.run(['ffmpeg','-v','error','-y','-framerate',str(FPS),'-i','q/fr/f_%04d.png','-i','q/quiz.wav','-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-af','loudnorm=I=-14:TP=-1.5:LRA=11','-c:a','aac','-b:a','192k','-ar','48000','-shortest','-movflags','+faststart','out/S5_quiz_ah_ya.mp4'],check=True)
print('done',TOTAL)
