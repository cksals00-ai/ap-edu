import numpy as np, wave
SR=48000; T=8.0; N=int(SR*T); L=np.zeros(N); R=np.zeros(N)
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

# ---- events locked to picture ----
add(pop(600),0.02,.35)
add(pop(f(NT['G5'])),0.30,.5,-.2); add(bell(f(NT['G5']),.6,.15),0.30,.12,-.2)
add(noise_sweep(.3,1500,6000),0.40,.18,.3); add(bell(f(NT['A5']),.6,.15),0.52,.14,.3)
add(pluck(f(NT['E5']),.5),0.75,.25)
add(noise_sweep(.3,800,3000),0.72,.12)
add(thump(),1.0,.9); add(bell(f(NT['C6']),1.0,.3),1.0,.25)
for t,n,pn in ((1.5,'D6',-.3),(2.0,'E6',0),(2.5,'G6',.3)):
    add(pop(f(NT[n])*.5),t,.45,pn); add(bell(f(NT[n]),.9,.25),t,.2,pn)
add(noise_sweep(.55,400,7000),2.62,.35)
for i,(n,pn) in enumerate((('C5',-.45),('E5',-.15),('G5',.15),('C6',.45))):
    add(boing(f(NT[n])),3.0+.25*i,.3,pn)
# arp bed 3.0-8.0: 120bpm eighths = .25s
prog=[('C4','E4','G4','C5'),('A4','C5','E5','A5'),('F4','A4','C5','F4'),('G4','C5','E5','G5')]
arp_i=0
for k in range(20):
    t=3.0+k*.25; chord=prog[(k//4)%4]; n=chord[k%4]
    fade=min(1,(t-3)/.5)*(1 if t<7.2 else max(0,(8-t)/.8))
    add(pluck(f(NT[n])*1,.55),t,.30*fade,(-.25 if k%2 else .25))
    add(pluck(f(NT[chord[0]])/2,.9),t,.2*fade) if k%4==0 else None
for k in range(40):
    t=3.0+k*.125; fade=min(1,(t-3)/.5)*(1 if t<7.2 else max(0,(8-t)/.8))
    add(shaker(),t,(.09 if k%2 else .05)*fade,.4)
for i,(t,n) in enumerate(((4.5,'C6'),(4.75,'D6'),(5.0,'E6'),(5.25,'G6'))):
    add(tok(650+80*i),t,.5,-.3+.2*i); add(bell(f(NT[n]),1.0,.3),t,.2,-.3+.2*i)
add(noise_sweep(.5,600,5000),5.5,.22,-.2)
add(thump(.4),5.28,.35)
for i,n in enumerate(('C6','E6','G6','C7')):
    add(bell(f(NT[n]),2.2,.8),6.45+.06*i,.18,-.3+.2*i)
for k in range(10): add(bell(f(NT['C7'])*[1,1.125,1.25,1.5,1.33][k%5],.5,.12),6.6+k*.13,.04,rng.uniform(-.7,.7))
# simple reverb (feedback comb + allpass-ish, stereo decorrelated)
def verb(x,seed):
    y=np.zeros_like(x)
    for dly,g in ((1557,.78),(1617,.77),(1491,.79),(1422,.8)):
        d=dly+seed*23; b=np.zeros_like(x)
        for s in range(0,len(x),d):
            pass
        # vectorized comb via iterative blocks
        b=x.copy()
        for rep in range(1,14): 
            sh=d*rep; 
            if sh>=len(x): break
            b[sh:]+=x[:-sh]*g**rep
        y+=b
    return y/4
wetL=verb(L,0); wetR=verb(R,1)
L=L+.28*(wetL-L); R=R+.28*(wetR-R)
mix=np.stack([L,R],1)
fade=np.ones(N); fo=int(.35*SR); fade[-fo:]=np.linspace(1,0,fo)**2; mix*=fade[:,None]
mix=np.tanh(mix*1.2)/1.2
mix/=np.max(np.abs(mix))/0.89
with wave.open('audio_raw.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype('<i2').tobytes())
print('ok')
