import { chromium } from 'playwright';
const [w, n] = process.argv.slice(2).map(Number); const FPS=60, N=480, S=10, SH=1/120;
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p = await b.newPage({viewport:{width:1920,height:1080}});
p.on('pageerror', e => console.log('ERR', e.message));
await p.goto('http://localhost:8790/scene.html'); await p.evaluate(() => window.ready);
for (let i = w; i < N; i += n) { await p.evaluate(([t,S,SH]) => renderBlur(t,S,SH), [i/FPS,S,SH]); await p.screenshot({path:`frames60/f_${String(i).padStart(4,'0')}.png`}); }
await b.close();
