# -*- coding: utf-8 -*-
"""30일 챌린지 키비주얼 v3 — 깔끔한 정보형 포스터 (Noto Sans KR · 크림 바탕 · 흰 카드 · 노란 무대 위 4남매).
언어 4종(ko·en·vi·fr) × 2비율(16:9 1600×900 / 4:5 1080×1350). 기존 3D 원화 컷아웃만 사용.
실행: python3 tools/keyvisual.py  (Playwright + Chromium, 시스템 폰트 Noto Sans CJK KR 필요)"""
import os, subprocess, json, tempfile
from PIL import Image, ImageFilter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ART = os.path.join(ROOT, 'assets', 'art')
TMP = tempfile.mkdtemp(prefix='kv_')

L = {
 'ko': dict(title='30일 챌린지', month='11월 한 달', sub='호랑이 4남매와 한글을 배우고, 게시판과 내 SNS에 후기를 남겨 주세요.',
            prizeTag='대상 1명', prize='Meta AI 글래스', prize2='+ 격려상 5명 · 참가 무료 · 나라 상관없이',
            info=[('신청', '10.13 – 10.31'), ('챌린지', '11.1 – 11.30'), ('발표', '12.12')],
            fine='주최 AP Edu (A.P Holdings) · Meta, Ray-Ban, YouTube는 이 이벤트의 후원사가 아닙니다.'),
 'en': dict(title='30-Day Challenge', month='All of November', sub='Learn Korean with four tiger cubs, then share your review on our board and your own channel.',
            prizeTag='Grand prize · 1 winner', prize='Meta AI glasses', prize2='+ 5 runner-up prizes · free entry · any country',
            info=[('Apply', '13 – 31 Oct'), ('Challenge', '1 – 30 Nov'), ('Winner', '12 Dec')],
            fine='Organised by AP Edu (A.P Holdings). Meta, Ray-Ban and YouTube are not sponsors of this event.'),
 'vi': dict(title='Thử thách 30 ngày', month='Suốt tháng 11', sub='Học tiếng Hàn cùng bốn chú hổ con, rồi chia sẻ cảm nhận trên bảng tin và trang cá nhân của bạn.',
            prizeTag='Giải nhất · 1 người', prize='Kính Meta AI', prize2='+ 5 giải khuyến khích · miễn phí · mọi quốc gia',
            info=[('Đăng ký', '13 – 31/10'), ('Thử thách', '1 – 30/11'), ('Công bố', '12/12')],
            fine='Tổ chức bởi AP Edu (A.P Holdings). Meta, Ray-Ban và YouTube không phải nhà tài trợ của sự kiện.'),
 'fr': dict(title='Défi 30 jours', month='Tout le mois de novembre', sub='Apprenez le coréen avec quatre bébés tigres, puis partagez votre avis sur notre forum et sur vos réseaux.',
            prizeTag='Grand prix · 1 gagnant', prize='Lunettes Meta AI', prize2='+ 5 prix d’encouragement · gratuit · tous pays',
            info=[('Inscription', '13 – 31 oct.'), ('Défi', '1er – 30 nov.'), ('Résultats', '12 déc.')],
            fine='Organisé par AP Edu (A.P Holdings). Meta, Ray-Ban et YouTube ne sont pas partenaires de ce jeu.'),
}

def cutouts():
    for n in ('kkobi', 'daho', 'aari', 'rami'):
        im = Image.open(os.path.join(ART, f'{n}_3d.png')).convert('RGBA')
        a = im.split()[3].filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(.6)); im.putalpha(a)
        im.crop(im.getbbox()).save(os.path.join(TMP, f'{n}.png'))

CSS = '''*{margin:0;padding:0;box-sizing:border-box}
:root{--cream:#fff8ec;--ink:#2b2118;--sub:#6e5a47;--line:#eadcc6;--honey:#e89b2a;--yel:#ffd040;--teal:#1f7f74}
html,body{width:__W__px;height:__H__px;overflow:hidden}
body{font-family:"Noto Sans CJK KR","Noto Sans KR",sans-serif;background:var(--cream);color:var(--ink);word-break:keep-all;-webkit-font-smoothing:antialiased;position:relative}
.brand{display:flex;align-items:center;gap:12px;font-weight:700;letter-spacing:.16em;font-size:20px;color:var(--sub)}
.brand img{width:34px;height:34px;border-radius:9px}.brand .sep{width:1px;height:18px;background:var(--line)}
.month{display:inline-block;font-weight:700;color:var(--teal);font-size:26px;letter-spacing:-.01em}
h1{font-weight:900;letter-spacing:-.035em;line-height:1.02}
.sub{font-weight:500;color:var(--sub);line-height:1.5}
.card{background:#fff;border-radius:28px;box-shadow:0 1px 0 rgba(43,33,24,.04),0 18px 40px -18px rgba(120,80,20,.28);position:relative;overflow:hidden}
.card:before{content:"";position:absolute;left:0;top:0;bottom:0;width:8px;background:var(--honey)}
.tag{display:inline-block;background:#fff1d6;color:#a8650c;font-weight:700;border-radius:999px;padding:6px 14px;font-size:19px}
.prize{font-weight:900;letter-spacing:-.03em;line-height:1.05}
.prize2{color:var(--sub);font-weight:500}
.info{display:flex}.info div{flex:1;padding:0 22px;border-left:1.5px solid var(--line)}.info div:first-child{padding-left:0;border-left:0}
.info small{display:block;color:var(--sub);font-weight:500;font-size:18px;margin-bottom:6px}.info b{font-weight:900;letter-spacing:-.02em}
.stage{position:absolute;background:var(--yel);overflow:hidden}
.stage:after{content:"";position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,rgba(255,255,255,.35),transparent 55%)}
.dots{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.55) 2.2px,transparent 2.6px);background-size:34px 34px;opacity:.55}
.cub{position:absolute;bottom:0;transform:translateX(-50%);filter:drop-shadow(0 14px 16px rgba(120,70,0,.28));z-index:2}
.url{font-weight:900;letter-spacing:-.01em}.fine{color:#9a8670;font-weight:500;font-size:15px;line-height:1.45}
'''

def html_tall(l, t):
    W, H = 1080, 1350
    cubs = [('kkobi', 250, 380), ('daho', 430, 400), ('aari', 650, 410), ('rami', 850, 385)]
    cub_h = ''.join(f'<img class="cub" src="{n}.png" style="left:{x}px;height:{h}px;bottom:-28px">' for n, x, h in cubs)
    tsize = 116 if len(t['title']) <= 12 else 96
    return f'''<!doctype html><html lang="{l}"><head><meta charset="utf-8"><style>{CSS.replace('__W__', str(W)).replace('__H__', str(H))}
.wrap{{position:absolute;left:84px;right:84px;top:76px}}h1{{font-size:{tsize}px;margin:14px 0 18px}}.sub{{font-size:28px;max-width:860px}}
.card{{margin-top:42px;padding:34px 40px 34px 48px}}.prize{{font-size:66px;margin:14px 0 10px}}.prize2{{font-size:22px}}
.info{{margin-top:34px}}.info b{{font-size:34px}}
.stage{{left:0;right:0;bottom:0;height:420px;border-radius:56px 56px 0 0}}
.foot{{position:absolute;left:84px;right:84px;bottom:30px;z-index:3;display:flex;justify-content:space-between;align-items:flex-end}}
.url{{font-size:28px;background:#fff;border-radius:999px;padding:10px 26px;box-shadow:0 8px 20px -10px rgba(120,70,0,.4)}}
.fine{{position:absolute;right:84px;left:84px;top:{H-420-44}px;text-align:right;font-size:14px}}</style></head><body>
<div class="wrap"><div class="brand"><img src="icon.png"><span>HANGEUL CUBS</span><span class="sep"></span><span>AP EDU</span></div>
<h1><span class="month">{t['month']}</span><br>{t['title']}</h1><p class="sub">{t['sub']}</p>
<div class="card"><span class="tag">{t['prizeTag']}</span><div class="prize">{t['prize']}</div><div class="prize2">{t['prize2']}</div></div>
<div class="info">{''.join(f'<div><small>{a}</small><b>{b}</b></div>' for a, b in t['info'])}</div></div>
<p class="fine">{t['fine']}</p>
<div class="stage"><div class="dots"></div>{cub_h}</div>
<div class="foot"><span class="url">edu.apholdings.kr</span></div></body></html>''', W, H

def html_wide(l, t):
    W, H = 1600, 900
    cubs = [('kkobi', 960, 390), ('daho', 1112, 410), ('aari', 1266, 418), ('rami', 1418, 398)]
    cub_h = ''.join(f'<img class="cub" src="{n}.png" style="left:{x-830}px;height:{h}px;bottom:-34px">' for n, x, h in cubs)
    tsize = 96 if len(t['title']) <= 12 else 80
    return f'''<!doctype html><html lang="{l}"><head><meta charset="utf-8"><style>{CSS.replace('__W__', str(W)).replace('__H__', str(H))}
.wrap{{position:absolute;left:88px;top:72px;width:830px}}h1{{font-size:{tsize}px;margin:12px 0 16px}}.sub{{font-size:24px;max-width:760px}}
.card{{margin-top:34px;padding:28px 36px 28px 44px;max-width:700px}}.prize{{font-size:56px;margin:12px 0 8px}}.prize2{{font-size:20px}}
.info{{margin-top:30px;max-width:700px}}.info b{{font-size:30px}}
.stage{{left:830px;right:48px;top:48px;bottom:48px;border-radius:44px}}.big30{{position:absolute;right:40px;top:6px;font-weight:900;font-size:340px;line-height:1;letter-spacing:-.06em;color:#fff;opacity:.5;z-index:1}}
.url{{position:absolute;left:88px;bottom:62px;font-size:26px}}.fine{{position:absolute;left:88px;bottom:32px;width:860px;font-size:13px}}
.stage .url2{{position:absolute;left:32px;top:28px;z-index:3;font-weight:900;font-size:20px;color:var(--ink);background:#fff;border-radius:999px;padding:8px 18px}}</style></head><body>
<div class="wrap"><div class="brand"><img src="icon.png"><span>HANGEUL CUBS</span><span class="sep"></span><span>AP EDU</span></div>
<h1><span class="month">{t['month']}</span><br>{t['title']}</h1><p class="sub">{t['sub']}</p>
<div class="card"><span class="tag">{t['prizeTag']}</span><div class="prize">{t['prize']}</div><div class="prize2">{t['prize2']}</div></div>
<div class="info">{''.join(f'<div><small>{a}</small><b>{b}</b></div>' for a, b in t['info'])}</div></div>
<span class="url">edu.apholdings.kr</span><p class="fine">{t['fine']}</p>
<div class="stage"><div class="dots"></div><div class="big30">30</div>{cub_h}</div></body></html>''', W, H

SHOT = r'''
import { chromium } from 'playwright';
const jobs = JSON.parse(process.argv[2]);
const b = await chromium.launch({executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium'});
for (const j of jobs) { const p = await b.newPage({viewport:{width:j.W,height:j.H}, deviceScaleFactor:1});
  await p.goto('file://' + j.src); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(150);
  await p.screenshot({path:j.png}); await p.close(); }
await b.close();'''

if __name__ == '__main__':
    cutouts(); Image.open(os.path.join(ROOT, 'assets', 'cubs_icon64.png')).save(os.path.join(TMP, 'icon.png'))
    jobs = []
    for l, t in L.items():
        for kind, fn in (('kv', html_wide), ('sq', html_tall)):
            h, W, H = fn(l, t); src = os.path.join(TMP, f'{kind}_{l}.html'); open(src, 'w', encoding='utf-8').write(h)
            jobs.append(dict(src=src, W=W, H=H, png=os.path.join(TMP, f'{kind}_{l}.png'), out=os.path.join(ART, f'challenge_{kind}_{l}.jpg')))
    js = os.path.join(os.environ.get('SHOT_DIR', TMP), '_kv_shot.mjs'); open(js, 'w').write(SHOT)
    subprocess.run(['node', js, json.dumps(jobs)], check=True, cwd=os.environ.get('NODE_CWD', ROOT))
    for j in jobs:
        Image.open(j['png']).convert('RGB').save(j['out'], quality=90, optimize=True, progressive=True); print(j['out'])
