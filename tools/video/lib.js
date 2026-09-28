const W=1920,H=1080,cv=document.getElementById('c'),g=cv.getContext('2d',{willReadFrequently:true});
const FONT='"Noto Sans CJK KR","Noto Sans KR",sans-serif';
const C={cream:'#fff7ea',cream2:'#ffe9c7',honey:'#e89b2a',honeyD:'#c97f12',ink:'#2b2118',brown:'#4a2c16',white:'#fffdf8',yel:'#ffd040',yel2:'#ffe27a',
  daho:'#2f6f7e',kkobi:'#4c9a3f',aari:'#1f9a8c',rami:'#e0678a'};
const CUBS=[{id:'daho',ko:'다호',en:'DAHO',c:C.daho},{id:'kkobi',ko:'꼬비',en:'KKOBI',c:C.kkobi},{id:'aari',ko:'아리',en:'AARI',c:C.aari},{id:'rami',ko:'라미',en:'RAMI',c:C.rami}];
const IMG={};

/* ── easing ── */
const cl=x=>x<0?0:x>1?1:x, lerp=(a,b,t)=>a+(b-a)*t, P=(t,a,b)=>cl((t-a)/(b-a));
const eOC=t=>1-Math.pow(1-t,3), eIOC=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2, eIQ=t=>t*t, eIC=t=>t*t*t;
const eOB=(t,s=1.7)=>1+(s+1)*Math.pow(t-1,3)+s*Math.pow(t-1,2);
const eIB=(t,s=1.7)=>(s+1)*t*t*t-s*t*t;
const eOQ=t=>1-Math.pow(1-t,5);
/* 감쇠 스프링: 0→1, overshoot 후 안착 */
const spring=(t,f=3.2,d=5.5)=>t<=0?0:1-Math.exp(-d*t)*Math.cos(2*Math.PI*f*t);
/* 충격 후 흔들림(0에서 시작해 0으로) */
const wobble=(t,f=5,d=7)=>t<=0?0:Math.exp(-d*t)*Math.sin(2*Math.PI*f*t);
function rnd(s){let x=Math.sin(s*9301+49297)*233280;return x-Math.floor(x)}
function mix(a,b,t){const pa=parseInt(a.slice(1),16),pb=parseInt(b.slice(1),16);const r=Math.round(lerp(pa>>16,pb>>16,t)),gg=Math.round(lerp(pa>>8&255,pb>>8&255,t)),bb=Math.round(lerp(pa&255,pb&255,t));return `rgb(${r},${gg},${bb})`}

/* ── 받침 분리: 글자를 픽셀로 그려 연결 성분을 나누고, 무게중심이 아래쪽인 성분을 받침으로 본다 ── */
const PARTS={};
function hasJong(ch){const c=ch.charCodeAt(0)-0xAC00;return c>=0&&c<11172&&c%28!==0}
function parts(ch,fs,ink,jc){
  const k=[ch,fs,ink,jc].join('|'); if(PARTS[k]) return PARTS[k];
  const S=Math.ceil(fs*1.5), o=document.createElement('canvas'); o.width=o.height=S; const x=o.getContext('2d');
  x.font=`900 ${fs}px ${FONT}`; x.textAlign='center'; x.textBaseline='middle'; x.fillStyle='#000'; x.fillText(ch,S/2,S/2);
  const id=x.getImageData(0,0,S,S), d=id.data, N=S*S, lab=new Int32Array(N).fill(-1); let n=0; const comps=[];
  for(let i=0;i<N;i++){ if(lab[i]>=0||d[i*4+3]<110) continue; const st=[i]; lab[i]=n; let sy=0,c=0,top=S;
    while(st.length){ const q=st.pop(), qy=(q/S)|0, qx=q%S; sy+=qy; c++; if(qy<top) top=qy;
      for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){ const nx=qx+dx, ny=qy+dy; if(nx<0||ny<0||nx>=S||ny>=S) continue; const j=ny*S+nx; if(lab[j]<0&&d[j*4+3]>=110){ lab[j]=n; st.push(j); } } }
    comps.push({cy:sy/c,c,top}); n++; }
  // 가장자리(알파 낮은 픽셀)는 가까운 성분으로
  for(let pass=0;pass<3;pass++) for(let i=0;i<N;i++){ if(lab[i]>=0||d[i*4+3]===0) continue; const qy=(i/S)|0,qx=i%S;
    for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]){ const nx=qx+dx,ny=qy+dy; if(nx<0||ny<0||nx>=S||ny>=S) continue; const L=lab[ny*S+nx]; if(L>=0){ lab[i]=L; break; } } }
  let gtop=S,gbot=0; for(let i=0;i<N;i++) if(d[i*4+3]>110){ const yy=(i/S)|0; if(yy<gtop) gtop=yy; if(yy>gbot) gbot=yy; }
  const cut=gtop+(gbot-gtop)*.60; const isJ=comps.map(cm=>hasJong(ch)&&cm.cy>cut);
  const hex=h=>[parseInt(h.slice(1,3),16),parseInt(h.slice(3,5),16),parseInt(h.slice(5,7),16)];
  const mk=(want,col)=>{ const c=document.createElement('canvas'); c.width=c.height=S; const cx=c.getContext('2d'); const out=cx.createImageData(S,S); const [r,gg,b]=hex(col);
    let jt=S,jb=0; for(let i=0;i<N;i++){ const L=lab[i]; if(L<0||isJ[L]!==want) continue; out.data[i*4]=r; out.data[i*4+1]=gg; out.data[i*4+2]=b; out.data[i*4+3]=d[i*4+3]; const yy=(i/S)|0; if(yy<jt) jt=yy; if(yy>jb) jb=yy; }
    cx.putImageData(out,0,0); c.mid=(jt+jb)/2; return c; };
  return PARTS[k]={S,top:mk(false,ink),jong:mk(true,jc||ink)};
}
/* ── 그리기 도구 ── */
function rr(x,y,w,h,r){g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath()}
function shadow(blur,oy,a){g.shadowColor=`rgba(110,60,0,${a})`;g.shadowBlur=blur;g.shadowOffsetY=oy;g.shadowOffsetX=0}
function noShadow(){g.shadowColor='transparent';g.shadowBlur=0;g.shadowOffsetY=0}

/* 글자 타일. o: {size, ch, border, jongColor, jongFlip(0..1 progress of flip), prevCh, sx, sy, rot, fill} */
function tile(cx,cy,o){
  const s=o.size, r=s*.2;
  g.save(); g.translate(cx,cy); g.rotate(o.rot||0); g.scale(o.sx||1,o.sy||1);
  shadow(s*.16,s*.07,.22); g.fillStyle=o.fill||C.white; rr(-s/2,-s/2,s,s,r); g.fill(); noShadow();
  if(o.bw!==0){ g.lineWidth=o.bw||s*.035; g.strokeStyle=o.border||C.honey; rr(-s/2+g.lineWidth/2,-s/2+g.lineWidth/2,s-g.lineWidth,s-g.lineWidth,r-g.lineWidth/2); g.stroke(); }
  if(o.ch) glyph(o.ch,0,s*.03,s*.64,o);
  g.restore();
}
/* 받침은 다른 색으로 — 앱의 시그니처를 그대로. o.jongFlip: 이전 받침이 접히고 새 받침이 펴진다 */
function glyph(ch,x,y,fs,o={}){
  fs=Math.round(fs); const ink=o.ink||C.ink;
  if(!hasJong(ch)||!o.jongColor){ g.font=`900 ${fs}px ${FONT}`; g.textAlign='center'; g.textBaseline='middle'; g.fillStyle=ink; g.fillText(ch,x,y); return; }
  const f=o.jongFlip===undefined?1:o.jongFlip, useOld=f<.5&&o.prevCh;
  const cur=parts(ch,fs,ink,o.jongColor), old=useOld?parts(o.prevCh,fs,ink,o.prevColor||o.jongColor):null, P0=old||cur, S=P0.S;
  g.drawImage(P0.top,x-S/2,y-S/2);
  const J=(old||cur).jong, sy=f>=1?1:Math.max(.02,Math.abs(Math.cos(Math.PI*f))), pop=o.jongPop||1, my=y-S/2+J.mid;
  g.save(); g.translate(x,my); g.scale(pop,sy*pop); g.drawImage(J,-S/2,-J.mid); g.restore();
}
function pill(cx,cy,text,sub,col,a,sc){
  g.save(); g.globalAlpha=a; g.translate(cx,cy); g.scale(sc,sc);
  g.font=`900 34px ${FONT}`; const w1=g.measureText(text).width; g.font=`700 22px ${FONT}`; const w2=g.measureText(sub).width; const w=w1+w2+72;
  shadow(18,8,.18); g.fillStyle=col; rr(-w/2,-30,w,60,30); g.fill(); noShadow();
  g.textBaseline='middle'; g.textAlign='left'; g.fillStyle='#fff'; g.font=`900 34px ${FONT}`; g.fillText(text,-w/2+28,2);
  g.globalAlpha=a*.85; g.font=`700 22px ${FONT}`; g.fillText(sub,-w/2+28+w1+16,3); g.restore();
}
function star(x,y,r,a,rot){ g.save(); g.globalAlpha=a; g.translate(x,y); g.rotate(rot); g.fillStyle='#fff'; g.beginPath();
  for(let i=0;i<8;i++){const rad=i%2?r*.28:r; const an=i*Math.PI/4; g.lineTo(Math.cos(an)*rad,Math.sin(an)*rad)} g.closePath(); g.fill(); g.restore(); }
function cub(id,cx,foot,h,sx,sy,rot,a){
  const im=IMG[id]; const w=im.width*h/im.height;
  g.save(); g.globalAlpha=a; g.translate(cx,foot); g.rotate(rot); g.scale(sx,sy);
  g.fillStyle='rgba(90,50,0,.18)'; g.beginPath(); g.ellipse(0,-6,w*.42*sx,18,0,0,Math.PI*2); g.fill();
  g.drawImage(im,-w/2,-h,w,h); g.restore();
}

/* ── 배경 ── */
const GRAIN=(()=>{const o=document.createElement('canvas');o.width=o.height=384;const x=o.getContext('2d');const d=x.createImageData(384,384);
  for(let i=0;i<d.data.length;i+=4){const v=rnd(i*.37)*255;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255}x.putImageData(d,0,0);return o})();
function background(t){
  // 크림 → 노랑: 2.75s 에 화면 아래에서 원이 퍼지며 덮는다
  let gr=g.createRadialGradient(W*.5,H*.42,80,W*.5,H*.5,W*.75); gr.addColorStop(0,C.cream); gr.addColorStop(1,C.cream2); g.fillStyle=gr; g.fillRect(0,0,W,H);
  const wp=eIOC(P(t,2.72,3.18));
  if(wp>0){ const R=lerp(0,Math.hypot(W,H)*1.05,wp); g.save(); g.beginPath(); g.arc(W/2,H+60,R,0,Math.PI*2); g.clip();
    let y=g.createRadialGradient(W*.5,H*.35,60,W*.5,H*.55,W*.8); y.addColorStop(0,C.yel2); y.addColorStop(.55,C.yel); y.addColorStop(1,'#f7b92c'); g.fillStyle=y; g.fillRect(0,0,W,H);
    // 은은한 점 무늬, 천천히 위로 흐른다
    g.fillStyle='rgba(255,236,160,.55)'; const off=(t*18)%52;
    for(let yy=-52;yy<H+52;yy+=52) for(let xx=((yy/52|0)%2)*26;xx<W;xx+=52){ g.beginPath(); g.arc(xx,yy-off,3.2,0,Math.PI*2); g.fill(); }
    g.restore();
    // 퍼지는 원의 테두리 하이라이트
    if(wp<1){ g.save(); g.globalAlpha=(1-wp)*.6; g.lineWidth=18; g.strokeStyle='#fff3c4'; g.beginPath(); g.arc(W/2,H+60,R,0,Math.PI*2); g.stroke(); g.restore(); }
  }
  // 떠다니는 부드러운 점 (시차)
  for(let i=0;i<22;i++){ const sp=6+rnd(i)*14, x=(rnd(i+3)*W + t*sp*(rnd(i+7)>.5?1:-1)+W)%W, y=(rnd(i+11)*H - t*sp*1.4 + H*2)%H, r=4+rnd(i+13)*10;
    g.fillStyle=`rgba(255,255,255,${.12+rnd(i+17)*.18})`; g.beginPath(); g.arc(x,y,r,0,Math.PI*2); g.fill(); }
}

/* ── 공통: 셔터 누적 모션블러 + 로더 ── */
let ACC=null;
function grain(t){ g.save(); g.globalAlpha=.035; g.globalCompositeOperation='overlay'; const ox=(rnd(Math.floor(t*120))*384)|0, oy=(rnd(Math.floor(t*120)+1)*384)|0;
  for(let y=-oy;y<H;y+=384) for(let x=-ox;x<W;x+=384) g.drawImage(GRAIN,x,y); g.restore(); }
window.renderBlur=(t,n,sh)=>{ if(!ACC) ACC=new Float32Array(W*H*4); ACC.fill(0);
  for(let j=0;j<n;j++){ const ts=Math.min(DUR,Math.max(0,t+(n>1?(j/(n-1)-.5)*sh:0))); render(ts); const d=g.getImageData(0,0,W,H).data; for(let k=0;k<d.length;k++) ACC[k]+=d[k]; }
  const out=g.createImageData(W,H), o=out.data, inv=1/n; for(let k=0;k<o.length;k++) o[k]=ACC[k]*inv+.5; g.putImageData(out,0,0); grain(t); };
const Q=new URLSearchParams(location.search);
window.ready=(async()=>{
  await Promise.all(CUBS.map(c=>new Promise(r=>{const i=new Image();i.onload=()=>{IMG[c.id]=i;r()};i.src=`art/${c.id}.png`})));
  await document.fonts.load(`900 100px ${FONT}`); await document.fonts.load(`700 40px ${FONT}`); await document.fonts.load(`500 40px ${FONT}`);
  render(0); return true; })();
