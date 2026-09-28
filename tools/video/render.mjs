// node render.mjs "<page?query>" <fps> <dur> <outdir> <worker> <nworkers>
import { chromium } from 'playwright';
const [page, fps, dur, outdir, w, n] = process.argv.slice(2); const F=+fps, N=Math.round(+dur*F), S=8, SH=0.5/F;
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p = await b.newPage({viewport:{width:1920,height:1080}}); p.on('pageerror', e => console.log('ERR', e.message));
await p.goto('http://localhost:8792/'+page); await p.evaluate(() => window.ready);
for (let i=+w; i<N; i+=+n) { await p.evaluate(([t,S,SH]) => renderBlur(t,S,SH), [i/F,S,SH]); await p.screenshot({path:`${outdir}/f_${String(i).padStart(4,'0')}.png`}); }
await b.close();
