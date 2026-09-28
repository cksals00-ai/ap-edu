import numpy as np, wave
SR=48000
rng=np.random.default_rng(7)
def f(n): return 440*2**((n-69)/12)
NT={'C5':72,'D5':74,'E5':76,'G5':79,'A5':81,'C6':84,'D6':86,'E6':88,'G6':91,'A6':93,'C7':96,'C4':60,'G4':67,'E4':64,'A4':69,'F4':65}
def add(sig,t,gain=1.0,pan=0.0):
    i=int(t*SR); s=sig[:max(0,N-i)]*gain
    L[i:i+len(s)]+=s*np.sqrt((1-pan)/2); R[i:i+len(s)]+=s*np.sqrt((1+pan)/2)
def env(n,a,d): t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-t/d)
def bell(fr,dur=1.2,d=.35):
    n=int(dur*SR); t=np.arange(n)/SR
    s=np.sin(2*np.pi*fr*t)+.35*np.sin(2*np.pi*fr*2.76*t)*np.exp(-t/.12)+.2*np.sin(2*np.pi*fr*5.4*t)*np.exp(-t/.05)
    return s*env(n,.002,d)
def pop(fr=900,dur=.12):
    n=int(dur*SR); t=np.arange(n)/SR; ph=2*np.pi*np.cumsum(fr*(1+2.2*np.exp(-t/.012)))/SR
    return np.sin(ph)*env(n,.001,.035)
def thump(dur=.5):
    n=int(dur*SR); t=np.arange(n)/SR; ph=2*np.pi*np.cumsum(55+140*np.exp(-t/.03))/SR
    return np.tanh(2.2*np.sin(ph)*env(n,.001,.16))+ .25*rng.standard_normal(n)*env(n,.0005,.01)
def noise_sweep(dur,f0,f1,rise=True):
    n=int(dur*SR); x=rng.standard_normal(n); X=np.fft.rfft(x); fr=np.fft.rfftfreq(n,1/SR)
    # time-varying approx: split into chunks with moving bandpass
    out=np.zeros(n); k=16; seg=n//k
    for j in range(k):
        c=f0*(f1/f0)**(j/(k-1)); xs=rng.standard_normal(seg*2); Xs=np.fft.rfft(xs); fq=np.fft.rfftfreq(seg*2,1/SR)
        Xs*=np.exp(-((np.log(fq+1)-np.log(c))**2)/.35); ys=np.fft.irfft(Xs)*np.hanning(seg*2)
        a=max(0,j*seg-seg//2); out[a:a+seg*2]+=ys[:len(out[a:a+seg*2])]
    t=np.arange(n)/dur/SR; shape=np.sin(np.pi*t**(.6 if rise else 1.4))**1.5
    return out/np.max(np.abs(out)+1e-9)*shape
def pluck(fr,dur=.6,bright=.5):
    p=int(SR/fr); buf=rng.uniform(-1,1,p); n=int(dur*SR); out=np.zeros(n)
    for i in range(n):
        out[i]=buf[i%p]; buf[i%p]=.996*(bright*buf[i%p]+(1-bright)*buf[(i+1)%p]) if False else .994*.5*(buf[i%p]+buf[(i+1)%p])
    return out*env(n,.001,dur/2.5)
def boing(f0,dur=.35):
    n=int(dur*SR); t=np.arange(n)/SR; fr=f0*(1+.5*np.exp(-t/.05)*np.sin(2*np.pi*14*t))
    ph=2*np.pi*np.cumsum(fr)/SR; return (np.sin(ph)+.3*np.sin(2*ph))*env(n,.002,.12)
def tok(fr=700):
    n=int(.12*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*fr*t)+.5*np.sin(2*np.pi*fr*2.3*t))*env(n,.0005,.018)+.3*rng.standard_normal(n)*env(n,.0003,.004)
def shaker():
    n=int(.08*SR); x=np.diff(rng.standard_normal(n+1)); return x*env(n,.004,.018)

import sys, subprocess
def new(T):
    global N,L,R; N=int(SR*T); L=np.zeros(N); R=np.zeros(N)
def add(sig,t,gain=1.0,pan=0.0):
    i=int(t*SR); s=sig[:max(0,N-i)]*gain
    L[i:i+len(s)]+=s*np.sqrt((1-pan)/2); R[i:i+len(s)]+=s*np.sqrt((1+pan)/2)
def wav(path):
    import wave as W_
    with W_.open(path) as w: sr=w.getframerate(); x=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)/32768
    if sr!=SR: x=np.interp(np.arange(int(len(x)*SR/sr))*sr/SR,np.arange(len(x)),x)
    return x
def pitch(x,semi):  # 간단 리샘플 피치업(길이도 짧아짐 — 캐릭터 목소리)
    r=2**(semi/12); return np.interp(np.arange(0,len(x)-1,r),np.arange(len(x)),x)
def verb(x):
    y=x.copy()
    for d,gn in ((1557,.62),(1617,.6),(1491,.64),(1422,.66)):
        for rep in range(1,10):
            sh=d*rep
            if sh>=len(x): break
            y[sh:]+=x[:-sh]*gn**rep*.25
    return y
def out(path,fade_out=0.0,lufs=-16):
    global L,R
    L2=L+.22*(verb(L)-L); R2=R+.22*(verb(R)-R); mix=np.stack([L2,R2],1)
    if fade_out: fo=int(fade_out*SR); mix[-fo:]*=np.linspace(1,0,fo)[:,None]**2
    mix=np.tanh(mix*1.2)/1.2; mix/=np.max(np.abs(mix))/0.89
    import wave as W_
    with W_.open(path+'.raw.wav','wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',path+'.raw.wav','-af',f'loudnorm=I={lufs}:TP=-1.5:LRA=11','-ar','48000',path],check=True)

# ── 스팅 3.0초 ──
def sting(path):
    new(3.0)
    for i,n in enumerate(('C6','D6','E6','G6')):
        t=.08+.16*i+.18; add(tok(650+80*i),t,.55,-.45+.3*i); add(bell(f(NT[n]),.8,.22),t,.2,-.45+.3*i)
    for i,n in enumerate(('C5','E5','G5','C6')): add(boing(f(NT[n])),.6+i*.06,.18,-.4+.27*i)
    add(noise_sweep(.35,900,5000),.78,.12)
    add(noise_sweep(.4,500,4000),1.45,.25)
    add(thump(.4),1.82,.45); 
    for i,n in enumerate(('C6','E6','G6','C7')): add(bell(f(NT[n]),1.6,.5),1.82+.04*i,.16,-.3+.2*i)
    add(noise_sweep(.5,300,8000),2.5,.35)
    out(path,fade_out=.12)

# ── 엔드카드 12초 ──
def outro(path,vdir):
    new(12.0)
    add(noise_sweep(.55,400,6000),0.0,.3)
    for i,n in enumerate(('C5','E5','G5','C6')): add(boing(f(NT[n])),.55+i*.08,.2,.3+.15*i)
    prog=[('C4','E4','G4','C5'),('A4','C5','E5','A5'),('F4','A4','C5','F4'),('G4','C5','E5','G5')]
    for k in range(44):
        t=.5+k*.25; ch=prog[(k//4)%4]; fd=min(1,(t-.5)/.5)*(1 if t<10.5 else max(0,(12-t)/1.5))
        add(pluck(f(NT[ch[k%4]]),.55),t,.22*fd,(-.25 if k%2 else .25))
        if k%4==0: add(pluck(f(NT[ch[0]])/2,.9),t,.15*fd)
    for k in range(88):
        t=.5+k*.125; fd=min(1,(t-.5)/.5)*(1 if t<10.5 else max(0,(12-t)/1.5)); add(shaker(),t,(.07 if k%2 else .04)*fd,.4)
    for c,n in ((1.55,'C6'),(2.45,'E6'),(3.25,'G6')): add(pop(f(NT[n])*.5),c,.5); add(bell(f(NT[n]),.9,.25),c,.22)
    for k in range(6): add(bell(f(NT['C7'])*[1,1.125,1.25,1.5,1.33][k%5],.5,.12),3.3+k*.09,.05,rng.uniform(-.7,.7))
    for v,t in (('v1',1.1),('v2',2.0),('v3',2.85),('v4',4.1)):
        x=pitch(wav(f'{vdir}/{v}.wav'),2.5); add(x,t,.9)
    out(path,fade_out=.35)

if __name__=='__main__':
    sting('sting.wav'); outro('outro.wav','voices'); print('ok')
