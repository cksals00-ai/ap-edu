// node shot.mjs <page?query> <t1,t2,...>  → /tmp/sp_<t>.png (단일 샘플 미리보기)
import { chromium } from 'playwright';
const [page, ts] = process.argv.slice(2);
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p = await b.newPage({viewport:{width:1920,height:1080}}); p.on('pageerror', e => console.log('ERR', e.message));
await p.goto('http://localhost:8792/'+page); await p.evaluate(() => window.ready);
for (const t of ts.split(',').map(Number)) { await p.evaluate(t => render(t), t); await p.screenshot({path:`/tmp/sp_${t.toFixed(2)}.png`}); }
await b.close();
