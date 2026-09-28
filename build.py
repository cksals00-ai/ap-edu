# -*- coding: utf-8 -*-
"""AP Edu — Hangeul Cubs 사이트 빌더. python3 build.py → 정적 파일 (GitHub Pages, edu.apholdings.kr)."""
import os, html
from content import CUBS, UNITS, LESSONS, EPISODES, EVENT, NEWS, STORE, YT, APP_ID
OUT = '.'; ORIGIN = 'https://edu.apholdings.kr'; V = '1'
e = html.escape
T = {
 'ko': dict(lang='ko', other='en', otherLabel='EN',
   nav=[('/ko/', '홈'), ('/ko/cubs/', '4남매'), ('/ko/episodes/', '에피소드'), ('/ko/app/', '앱'), ('/ko/event/', '체험단'), ('/ko/board/', '게시판'), ('/ko/news/', '소식')],
   heroEyebrow='AP EDU · HANGEUL CUBS', heroTitle=('호랑이 4남매와', '배우는 한글.'),
   heroLead='한 편에 글자 하나. 보고, 말하고, 쓰고, 노래한다. 한국어를 처음 만나는 아이와 어른을 위해.',
   cta='4남매 만나기', cta2='첫 레슨 보기', plat='iPhone · iPad 무료 · YouTube @hangeulcubs',
   stats=[('42', '무료 레슨', '받침 일곱 소리부터 생활 단어까지'), ('5', '유튜브 레슨', 'ㅏ ㅑ ㅓ ㅕ ㅗ — 매주 이어집니다'), ('3', '언어 힌트', '영어 · 베트남어 · 프랑스어'), ('0', '계정 · 광고', '오프라인 · 기기 내장 발음')],
   cubs='4남매', cubsLead='받침 하나씩, 네 명이 나눠 가르친다.', episodes='에피소드', episodesLead='한 편에 글자 하나. 유튜브에서.',
   app='앱', appLead='배우고 · 듣고 · 풀고. 세 화면, 한 흐름.', event='체험단', eventLead='받침 마스터를 먼저 써 보고, 후기 한 편.',
   news='소식', all='전체 보기', watch='유튜브에서 보기', words='이 편의 단어', chapters='구간', teaches='맡은 받침', hosts='앱에서 진행하는 레슨',
   look='생김새', role='역할', story='이야기', sheet='모델 시트', sheetNote='2D 턴어라운드 · 표정 시트 (제작용 원화)',
   free='무료', master='받침 마스터', masterNote='18레슨 · 108단어 — 쓰는 대로 읽지 않는 소리들. 앱 안 결제 ₩4,400 · 업데이트 심사 중',
   lessonN='과', unitLessons='레슨', store='App Store', ytch='유튜브 채널', privacy='개인정보처리방침', company='회사',
   studio='AP Edu는 A.P Holdings의 교육 레이블입니다.', footer_note='Hangeul Cubs © 2026 AP Edu / A.P Holdings. 캐릭터 · 아트 · 콘텐츠는 AP Edu의 자산입니다. 일러스트는 AI 도구로 제작했습니다.',
   applyBtn='체험단 신청', dl='앱 받기', kinds={'lesson': '글자 레슨', 'talk': '회화편', 'adult': '성인 초보', 'parent': '보호자 가이드', 'short': '쇼츠'},
   prev='이전', next='다음', backCubs='4남매 목록',
 ),
 'en': dict(lang='en', other='ko', otherLabel='KO',
   nav=[('/en/', 'Home'), ('/en/cubs/', 'The Cubs'), ('/en/episodes/', 'Episodes'), ('/en/app/', 'App'), ('/en/event/', 'Testers'), ('/en/board/', 'Community'), ('/en/news/', 'News')],
   heroEyebrow='AP EDU · HANGEUL CUBS', heroTitle=('Learn Korean with', 'four tiger cubs.'),
   heroLead='One letter per episode. See it, say it, write it, sing it. For children and adults meeting Korean for the first time.',
   cta='Meet the cubs', cta2='Watch Lesson 1', plat='Free on iPhone · iPad · YouTube @hangeulcubs',
   stats=[('42', 'free lessons', 'from the seven bottom blocks to everyday words'), ('5', 'YouTube lessons', 'ㅏ ㅑ ㅓ ㅕ ㅗ — new ones weekly'), ('3', 'hint languages', 'English · Vietnamese · French'), ('0', 'accounts · ads', 'offline · on-device Korean voice')],
   cubs='The Cubs', cubsLead='One bottom block each. Four teachers, one alphabet.', episodes='Episodes', episodesLead='One letter per episode, on YouTube.',
   app='The app', appLead='Learn · listen · quiz. Three screens, one flow.', event='Testers', eventLead='Try Batchim Master first, write one review.',
   news='News', all='See all', watch='Watch on YouTube', words='Words in this episode', chapters='Chapters', teaches='Bottom block', hosts='Lessons hosted in the app',
   look='Look', role='Role', story='Story', sheet='Model sheet', sheetNote='2D turnaround · expression sheet (production art)',
   free='Free', master='Batchim Master', masterNote='18 lessons · 108 words — where spelling and sound disagree. In-app purchase ₩4,400 · update in review',
   lessonN='', unitLessons='lessons', store='App Store', ytch='YouTube channel', privacy='Privacy policy', company='Company',
   studio='AP Edu is the education label of A.P Holdings.', footer_note='Hangeul Cubs © 2026 AP Edu / A.P Holdings. Characters, art and content are assets of AP Edu. Illustrations were made with AI tools.',
   applyBtn='Apply to test', dl='Get the app', kinds={'lesson': 'Letter lesson', 'talk': 'Conversation', 'adult': 'Adult beginner', 'parent': 'Parent guide', 'short': 'Shorts'},
   prev='Prev', next='Next', backCubs='All cubs',
 ),
}

def shell(l, title, desc, path, body, og=None, extra_head=''):
    t = T[l]; alt = f'/{t["other"]}{path[3:]}'
    nav = ''.join(f'<a href="{h}"{" class=on" if path == h or (h != f"/{l}/" and path.startswith(h)) else ""}>{e(n)}</a>' for h, n in t['nav'])
    og = og or '/assets/art/family.jpg'
    return f'''<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title>
<meta name="description" content="{e(desc, True)}"><link rel="canonical" href="{ORIGIN}{path}"><link rel="alternate" hreflang="{t['other']}" href="{ORIGIN}{alt}">
<meta property="og:title" content="{e(title, True)}"><meta property="og:description" content="{e(desc, True)}"><meta property="og:image" content="{ORIGIN}{og}"><meta property="og:url" content="{ORIGIN}{path}"><meta name="theme-color" content="#fff7ea">
<link rel="icon" href="/assets/ap_edu_mark.svg"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={V}">{extra_head}</head><body>
<header class="top"><a class="brand" href="/{l}/"><img src="/assets/ap_edu_wordmark.svg" alt="AP Edu" height="22"><img class="gicon" src="/assets/cubs_icon64.png" width="22" height="22" alt=""><span class="game">HANGEUL CUBS</span></a><nav>{nav}</nav><a class="lang" href="{alt}">{t['otherLabel']}</a></header>
<main>{body}</main>
<footer><div class="wrap"><div class="fgrid"><div><img src="/assets/ap_edu_wordmark.svg" alt="AP Edu" height="20"><p>{e(t['studio'])}</p></div>
<div><a href="{STORE[l]}" target="_blank" rel="noopener">{e(t['store'])}</a> · <a href="{YT}" target="_blank" rel="noopener">{e(t['ytch'])}</a><br><a href="https://www.apholdings.kr/{l}/">{e(t['company'])} — apholdings.kr</a> · <a href="https://www.apholdings.kr/hangeulcubs_privacy.html">{e(t['privacy'])}</a></div></div><p class="fine">{e(t['footer_note'])}</p></div></footer>
<script src="/assets/site.js?v={V}" defer></script></body></html>'''

def out(path, text):
    p = os.path.join(OUT, path.lstrip('/')); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w', encoding='utf-8').write(text)

def cub_card(l, c, big=False):
    t = T[l]
    return f'<a class="ccard" href="/{l}/cubs/{c["id"]}/" style="--c:{c["color"]}"><div class="fig"><img src="/assets/art/{c["id"]}_3d.png" alt="{e(c["name"] if l=="ko" else c["en"])}" loading="lazy" width="628" height="840"></div><div class="meta"><span class="role">{e(c["order"] if l=="ko" else c["order_en"])} · {e(c["batchim"] if l=="ko" else c["batchim_en"])}</span><h3>{e(c["name"] if l=="ko" else c["en"])}<small>{e(c["en"] if l=="ko" else c["name"])}</small></h3><p>{e(c["tag"] if l=="ko" else c["tag_en"])}</p></div></a>'

def ep_card(l, x, compact=False):
    t = T[l]; kind = t['kinds'][x['kind']]
    n = f'{"레슨" if l=="ko" else "Lesson"} {x["n"]}' if x['n'] else kind
    words = ''.join(f'<span><b>{e(k)}</b> {e(v)}</span>' for k, v in x['words'][:3])
    return f'''<article class="ecard{' short' if x['kind']=='short' else ''}" id="{x['id']}"><a class="thumb" href="https://youtu.be/{x['id']}" target="_blank" rel="noopener" data-yt="{x['id']}" aria-label="{e(x['title_en'] if l=='en' else x['title'])}"><img src="/assets/yt/{x['id']}.jpg" alt="" loading="lazy" width="1280" height="720"><span class="play" aria-hidden="true">▶</span><span class="len">{x['len']}</span></a>
<div class="meta"><span class="role">{e(n)} · <i class="letter">{e(x['letter'])}</i> {e(x['rr'])}</span><h3>{e(x['title'] if l=='ko' else x['title_en'])}</h3>{'' if compact else f'<p>{e(x["ko"] if l=="ko" else x["en"])}</p>'}{f'<div class="words">{words}</div>' if words and not compact else ''}</div></article>'''

def lesson_rows(l, host=None, unit=None):
    t = T[l]; rows = [x for x in LESSONS if (host is None or x[1] == host) and (unit is None or x[2] == unit)]
    name = {c['id']: (c['name'] if l == 'ko' else c['en']) for c in CUBS}; name['cubs'] = '4남매' if l == 'ko' else 'The Cubs'
    free_ids = [x[0] for x in LESSONS if x[2] != 'master']; master_ids = [x[0] for x in LESSONS if x[2] == 'master']
    num = lambda i: str(free_ids.index(i) + 1) if i in free_ids else 'M' + str(master_ids.index(i) + 1)
    return ''.join(f'<li{" class=master" if x[2]=="master" else ""}><i>{num(x[0])}</i><div><b>{e(x[3])}</b><span>{e(x[4])}</span></div><em>{e(name[x[1]])}</em></li>' for x in rows)

for l in ('ko', 'en'):
    t = T[l]
    cubs = ''.join(cub_card(l, c) for c in CUBS)
    eps = ''.join(ep_card(l, x, compact=True) for x in [x for x in EPISODES if x['kind'] != 'short'][:6])
    stats = ''.join(f'<article><b class="big">{a}</b><h3>{e(h_)}</h3><p>{e(d_)}</p></article>' for a, h_, d_ in t['stats'])
    news = ''.join(f'<article><time>{n[0]}</time><h3>{e(n[1] if l=="ko" else n[3])}</h3><p>{e(n[2] if l=="ko" else n[4])}</p></article>' for n in NEWS)
    ev_ko = f'받침 마스터 체험단 1기 · {EVENT["n"]}명 · {EVENT["apply"][1][5:].replace("-", "/")}까지 신청'
    ev_en = f'Batchim Master testers · {EVENT["n"]} places · apply by {EVENT["apply"][1]}'
    body = f'''<section class="hero"><img class="bg" src="/assets/art/family.jpg" alt="" width="1400" height="787"><div class="shade"></div>
<div class="wrap hero-copy"><span class="eyebrow">{e(t['heroEyebrow'])}</span><h1>{e(t['heroTitle'][0])}<br>{e(t['heroTitle'][1])}</h1><p class="lead">{e(t['heroLead'])}</p>
<div class="actions"><a class="btn" href="/{l}/cubs/">{e(t['cta'])}</a><a class="btn ghost" href="/{l}/episodes/#vpZ7JeHaz6I">{e(t['cta2'])}</a></div><p class="plat">{e(t['plat'])}</p></div></section>
<section class="feat"><div class="wrap"><div class="fgrid4">{stats}</div></div></section>
<section class="sec"><div class="wrap"><div class="sh"><h2>{e(t['cubs'])}</h2><p>{e(t['cubsLead'])}</p><a class="more" href="/{l}/cubs/">{e(t['all'])} →</a></div><div class="cgrid">{cubs}</div></div></section>
<section class="sec soft"><div class="wrap"><div class="sh"><h2>{e(t['episodes'])}</h2><p>{e(t['episodesLead'])}</p><a class="more" href="/{l}/episodes/">{e(t['all'])} →</a></div><div class="egrid">{eps}</div></div></section>
<section class="sec"><div class="wrap app-tease"><div><span class="eyebrow">APP</span><h2>{e(t['appLead'])}</h2><p class="lead">{'42레슨 무료. 받침을 색으로 나눠 보여 주고, 기기 안의 한국어 목소리로 읽어 준다. 계정도 광고도 없다.' if l=='ko' else '42 free lessons. The bottom block is shown in its own colour and read aloud by the device’s Korean voice. No account, no ads.'}</p><div class="actions"><a class="btn" href="{STORE[l]}" target="_blank" rel="noopener">{e(t['dl'])}</a><a class="btn ghost" href="/{l}/app/">{e(t['all'])}</a></div></div><img src="/assets/art/screens.jpg" alt="" loading="lazy" width="1400" height="787"></div></section>
<section class="sec event-band"><div class="wrap"><div class="eband"><div><span class="eyebrow">{e(t['event'])}</span><h2>{e(t['eventLead'])}</h2><p>{e(ev_ko if l=='ko' else ev_en)}</p></div><a class="btn" href="/{l}/event/">{e(t['applyBtn'])}</a></div></div></section>
<section class="sec"><div class="wrap"><div class="sh"><h2>{e(t['news'])}</h2><a class="more" href="/{l}/news/">{e(t['all'])} →</a></div><div class="ngrid">{news}</div></div></section>'''
    out(f'/{l}/index.html', shell(l, 'Hangeul Cubs — ' + ('호랑이 4남매와 배우는 한글 | AP Edu' if l == 'ko' else 'Learn Korean with four tiger cubs | AP Edu'), t['heroLead'], f'/{l}/', body))

    # CUBS list
    body = f'<section class="page"><div class="wrap"><span class="eyebrow">HANGEUL CUBS</span><h1>{e(t["cubs"])}</h1><p class="lead">{e(t["cubsLead"])}</p><figure class="team"><img src="/assets/art/group_3d.png" alt="" loading="lazy"><figcaption>{"다호 · 꼬비 · 아리 · 라미" if l=="ko" else "Daho · Kkobi · Aari · Rami"}</figcaption></figure><div class="cgrid big">{"".join(cub_card(l, c) for c in CUBS)}</div></div></section>'
    out(f'/{l}/cubs/index.html', shell(l, f'{t["cubs"]} — Hangeul Cubs', t['cubsLead'], f'/{l}/cubs/', body))

    # CUB pages
    for i, c in enumerate(CUBS):
        nm = c['name'] if l == 'ko' else c['en']; sub = c['en'] if l == 'ko' else c['name']
        bio = ''.join(f'<p>{e(x)}</p>' for x in (c['bio'] if l == 'ko' else c['bio_en']))
        rows = lesson_rows(l, host=c['id'])
        prev = CUBS[i - 1]; nxt = CUBS[(i + 1) % len(CUBS)]
        body = f'''<section class="cpage" style="--c:{c['color']}"><div class="wrap two"><div class="copy"><span class="eyebrow">{e(c['order'] if l=='ko' else c['order_en'])} · {e(t['role'])} · {e(c['role'] if l=='ko' else c['role_en'])}</span><h1>{e(nm)}<small>{e(sub)}</small></h1><p class="tag">{e(c['tag'] if l=='ko' else c['tag_en'])}</p>
<blockquote>“{e(c['quote'] if l=='ko' else c['quote_en'])}”</blockquote><div class="stats"><span>{e(t['teaches'])} <b>{e(c['batchim'] if l=='ko' else c['batchim_en'])}</b></span><span>{e(t['look'])} <b>{e(c['look'] if l=='ko' else c['look_en'])}</b></span></div></div><div class="art"><img src="/assets/art/{c['id']}_3d.png" alt="{e(nm)}" width="628" height="840"></div></div></section>
<section class="sec"><div class="wrap two"><div><div class="sh"><h2>{e(t['story'])}</h2></div>{bio}</div><div><div class="sh"><h2>{e(t['hosts'])}</h2></div><ul class="lessons">{rows}</ul></div></div></section>
<section class="sec soft"><div class="wrap"><div class="sh"><h2>{e(t['sheet'])}</h2><p>{e(t['sheetNote'])}</p></div><div class="sheets"><img src="/assets/art/{c['id']}_turn.jpg" alt="{e(nm)} turnaround" loading="lazy" width="1376" height="768"><img src="/assets/art/{c['id']}_face.jpg" alt="{e(nm)} expressions" loading="lazy" width="1376" height="768"></div></div></section>
<nav class="pn wrap"><a href="/{l}/cubs/{prev['id']}/">← {e(prev['name'] if l=='ko' else prev['en'])}</a><a href="/{l}/cubs/">{e(t['backCubs'])}</a><a href="/{l}/cubs/{nxt['id']}/">{e(nxt['name'] if l=='ko' else nxt['en'])} →</a></nav>'''
        out(f'/{l}/cubs/{c["id"]}/index.html', shell(l, f'{nm} — Hangeul Cubs', c['tag'] if l == 'ko' else c['tag_en'], f'/{l}/cubs/{c["id"]}/', body, og=f'/assets/art/{c["id"]}_3d.png'))

    # EPISODES
    groups = [('lesson', '글자 레슨' if l == 'ko' else 'Letter lessons', '모음 열 개부터. 한 편에 글자 하나, 단어 셋, 쓰기 한 번.' if l == 'ko' else 'Starting with the ten vowels. One letter, three words and one writing pass per episode.'),
              ('talk', '회화편' if l == 'ko' else 'Conversation', '상황 하나에 문장 서너 개.' if l == 'ko' else 'A few phrases for one situation.'),
              ('adult', '성인 초보 · 여행자' if l == 'ko' else 'Adult beginners · travellers', '1분 안에 끝나는 실전 한 컷.' if l == 'ko' else 'One practical clip, under a minute.'),
              ('parent', '보호자 가이드' if l == 'ko' else 'Parent guide', '집에서 아이와 함께 하는 법.' if l == 'ko' else 'How to practise with your child at home.'),
              ('short', '쇼츠' if l == 'ko' else 'Shorts', '30초 안에 글자 하나.' if l == 'ko' else 'One letter in thirty seconds.')]
    secs = ''
    for k, h_, d_ in groups:
        items = [x for x in EPISODES if x['kind'] == k]
        secs += f'<div class="sh"><h2>{e(h_)}</h2><p>{e(d_)}</p></div><div class="egrid{" shorts" if k=="short" else ""}">{"".join(ep_card(l, x, compact=(k=="short")) for x in items)}</div>'
    body = f'<section class="page"><div class="wrap"><span class="eyebrow">YOUTUBE @HANGEULCUBS</span><h1>{e(t["episodes"])}</h1><p class="lead">{e(t["episodesLead"])} <a href="{YT}" target="_blank" rel="noopener">{e(t["ytch"])} →</a></p>{secs}</div></section><div id="yt-modal" class="yt-modal" hidden><div class="yt-box"><button class="yt-x" type="button" aria-label="close">×</button><div class="yt-frame"></div></div></div>'
    out(f'/{l}/episodes/index.html', shell(l, f'{t["episodes"]} — Hangeul Cubs', t['episodesLead'], f'/{l}/episodes/', body, og='/assets/yt/vpZ7JeHaz6I.jpg'))

    # APP
    unit_blocks = ''
    for uid, uko, uen in UNITS:
        rows = lesson_rows(l, unit=uid); n = len([x for x in LESSONS if x[2] == uid])
        unit_blocks += f'<details class="unit{" master" if uid=="master" else ""}"{" open" if uid=="start" else ""}><summary><b>{e(uko if l=="ko" else uen)}</b><span>{n} {e(t["unitLessons"])}{" · " + e(t["master"]) if uid=="master" else ""}</span></summary><ul class="lessons">{rows}</ul></details>'
    feats_ko = [('색', '받침을 색으로', '「바」 아래 블록 하나가 「반」이 되는 순간을 색으로 나눠 보여 준다.'), ('소리', '기기 안의 목소리', '단어마다 한국어 발음. 서버 없이 기기 내장 음성으로.'), ('귀', '최소대립쌍', '반/방 · 발/밥 · 문/물 · 곰/공 — 받침 하나로 뜻이 갈리는 짝을 듣는다.'), ('퀴즈', '도전 모드', '3라운드 12문항 약 2분. 워밍업 · 미니게임 · 파이널 베팅. 끝낸 과에서만 출제.')]
    feats_en = [('Colour', 'The block in colour', 'The moment one block under 바 turns it into 반 — shown in its own colour.'), ('Voice', 'On-device Korean voice', 'Every word read aloud by the device itself. No server.'), ('Ears', 'Minimal pairs', '반/방 · 발/밥 · 문/물 · 곰/공 — pairs that change meaning with one block.'), ('Quiz', 'Challenge mode', '3 rounds, 12 questions, about 2 minutes. Warm-up · mini game · final bet. Only from lessons you finished.')]
    feats = ''.join(f'<article><b class="big">{e(a)}</b><h3>{e(h_)}</h3><p>{e(d_)}</p></article>' for a, h_, d_ in (feats_ko if l == 'ko' else feats_en))
    tags = ['42레슨 무료', 'EN · VI · FR 힌트', '기기 내장 발음', '완전 오프라인', '광고 0 · 계정 0', 'iPhone · iPad'] if l == 'ko' else ['42 free lessons', 'EN · VI · FR hints', 'on-device voice', 'fully offline', 'no ads · no account', 'iPhone · iPad']
    body = f'''<section class="page"><div class="wrap"><span class="eyebrow">HANGEUL CUBS · iOS</span><h1>{e(t['app'])}</h1><p class="lead">{e(t['appLead'])}</p><div class="tags">{''.join(f'<span>{e(x)}</span>' for x in tags)}</div>
<div class="actions"><a class="btn" href="{STORE[l]}" target="_blank" rel="noopener">{e(t['dl'])} — {e(t['store'])}</a></div>
<figure class="wide"><img src="/assets/art/screens.jpg" alt="" width="1400" height="787"></figure>
<div class="fgrid4">{feats}</div>
<figure class="wide"><img src="/assets/art/devices.jpg" alt="" loading="lazy" width="1400" height="787"></figure>
<div class="sh"><h2>{'레슨 60' if l=='ko' else '60 lessons'}</h2><p>{'무료 42 + 받침 마스터 18. 6묶음. 과마다 진행하는 남매가 다르다.' if l=='ko' else '42 free + 18 in Batchim Master. Six units. A different cub hosts each lesson.'}</p></div>
<div class="units">{unit_blocks}</div>
<div class="master-note"><span class="eyebrow">{e(t['master'])}</span><p>{e(t['masterNote'])}</p></div>
<div class="sh"><h2>{'약속' if l=='ko' else 'Promise'}</h2></div><div class="fgrid4 promise"><article><b class="big">0</b><h3>{'계정' if l=='ko' else 'accounts'}</h3><p>{'로그인 없음. 진행은 기기에만.' if l=='ko' else 'No sign-in. Progress stays on the device.'}</p></article><article><b class="big">0</b><h3>{'광고' if l=='ko' else 'ads'}</h3><p>{'광고도, 추적도 없다.' if l=='ko' else 'No ads, no tracking.'}</p></article><article><b class="big">0</b><h3>{'서버' if l=='ko' else 'servers'}</h3><p>{'완전 오프라인. 비행기에서도.' if l=='ko' else 'Fully offline. Works on a plane.'}</p></article><article><b class="big">1</b><h3>{'결제' if l=='ko' else 'purchase'}</h3><p>{'받침 마스터 팩 하나뿐. 구독 없음.' if l=='ko' else 'One Batchim Master pack. No subscription.'}</p></article></div>
</div></section>'''
    out(f'/{l}/app/index.html', shell(l, f'{t["app"]} — Hangeul Cubs', t['appLead'], f'/{l}/app/', body, og='/assets/art/screens.jpg'))

    # EVENT
    a0, a1 = EVENT['apply']; r0, r1 = EVENT['run']
    if l == 'ko':
        steps = [('신청', f'{a0[5:].replace("-", "/")} – {a1[5:].replace("-", "/")}', '아래 폼으로. 아이·어른·가족 누구나.'), ('발표', EVENT['announce'][5:].replace('-', '/'), f'{EVENT["n"]}명. 이메일로 코드를 보내 드려요.'), ('체험', f'{r0[5:].replace("-", "/")} – {r1[5:].replace("-", "/")}', '받침 마스터 18레슨을 2주 동안.'), ('후기', EVENT['review_due'][5:].replace('-', '/'), '게시판 「후기」에 한 편, 또는 App Store 리뷰.')]
        give = [('받침 마스터 무료', '₩4,400 팩을 코드로 열어 드려요. 기간이 끝나도 남아요.'), ('이름 남기기', '원하면 게시판 후기에 닉네임으로 소개해 드려요.'), ('다음 레슨 먼저', '새 레슨팩이 나오면 먼저 써 봅니다.')]
        ask = [('2주 사용', '받침 마스터 18레슨 중 절반 이상.'), ('후기 한 편', '좋았던 것 하나, 고칠 것 하나면 충분해요.'), ('짧은 설문', '3분. 이메일로 보내 드려요.')]
        note = '개인정보는 체험단 연락(코드 발송·설문)에만 쓰고, 체험이 끝나면 지웁니다. 아이 정보는 나이대만 받아요. 받침 마스터는 앱 업데이트(2.3) 승인 뒤 열리며, 코드는 승인 즉시 보내 드려요.'
        f = dict(name='이름 또는 닉네임', email='이메일', learner='누가 배우나요', learners=[('child', '아이 (보호자가 신청)'), ('adult', '어른 · 나'), ('family', '가족이 함께'), ('teacher', '선생님 · 교실')], age='아이 나이대 (선택)', ages=['', '4–6', '7–9', '10–12', '13+'], country='나라 · 지역 (선택)', device='기기', devices=[('iphone', 'iPhone'), ('ipad', 'iPad'), ('both', '둘 다')], channel='후기를 남길 곳 (선택 — 블로그·SNS 주소)', note='한 마디 (선택 — 왜 한글을 배우나요?)', consent='개인정보를 체험단 운영에만 쓰는 데 동의해요.', submit='신청하기', ok='신청을 받았어요. 10월 14일에 이메일로 알려 드릴게요.', err='보내지 못했어요. 잠시 뒤 다시 시도해 주세요.', many='같은 이메일로 이미 신청했어요.')
    else:
        steps = [('Apply', f'{a0} – {a1}', 'Use the form below. Kids, adults, families, teachers.'), ('Results', EVENT['announce'], f'{EVENT["n"]} testers. Codes go out by email.'), ('Test', f'{r0} – {r1}', 'Two weeks with the 18 Batchim Master lessons.'), ('Review', EVENT['review_due'], 'One post in the community board, or an App Store review.')]
        give = [('Batchim Master, free', 'The ₩4,400 pack unlocked by code. It stays yours afterwards.'), ('Your name on the board', 'If you like, we introduce your review by nickname.'), ('Next packs first', 'New lesson packs reach testers first.')]
        ask = [('Two weeks of use', 'At least half of the 18 lessons.'), ('One review', 'One thing you liked, one thing to fix — that’s enough.'), ('A short survey', 'Three minutes, by email.')]
        note = 'We use your details only to run the programme (sending codes, the survey) and delete them when it ends. For children we ask only an age band. Batchim Master unlocks once app update 2.3 is approved; codes are sent the moment it is.'
        f = dict(name='Name or nickname', email='Email', learner='Who is learning?', learners=[('child', 'A child (parent applies)'), ('adult', 'An adult · me'), ('family', 'The whole family'), ('teacher', 'A teacher · classroom')], age='Child’s age band (optional)', ages=['', '4–6', '7–9', '10–12', '13+'], country='Country · region (optional)', device='Device', devices=[('iphone', 'iPhone'), ('ipad', 'iPad'), ('both', 'Both')], channel='Where you’d post a review (optional — blog / social link)', note='One line (optional — why Korean?)', consent='I agree that my details are used only to run the tester programme.', submit='Apply', ok='Got it. We’ll email you on 14 October.', err='Couldn’t send. Please try again in a moment.', many='This email has already applied.')
    steps_h = ''.join(f'<li><b>{e(a)}</b><time>{e(b)}</time><p>{e(c_)}</p></li>' for a, b, c_ in steps)
    give_h = ''.join(f'<li><b>{e(a)}</b><p>{e(b)}</p></li>' for a, b in give)
    ask_h = ''.join(f'<li><b>{e(a)}</b><p>{e(b)}</p></li>' for a, b in ask)
    form = f'''<form id="apply" class="apply" data-lang="{l}" data-event="{EVENT['key']}" data-ok="{e(f['ok'], True)}" data-err="{e(f['err'], True)}" data-many="{e(f['many'], True)}">
<label>{e(f['name'])}<input name="name" required maxlength="40"></label>
<label>{e(f['email'])}<input name="email" type="email" required maxlength="120"></label>
<label>{e(f['learner'])}<select name="learner" required>{''.join(f'<option value="{v}">{e(k)}</option>' for v, k in f['learners'])}</select></label>
<label>{e(f['age'])}<select name="age_band">{''.join(f'<option value="{e(v)}">{e(v)}</option>' for v in f['ages'])}</select></label>
<label>{e(f['country'])}<input name="country" maxlength="40"></label>
<label>{e(f['device'])}<select name="device" required>{''.join(f'<option value="{v}">{e(k)}</option>' for v, k in f['devices'])}</select></label>
<label class="full">{e(f['channel'])}<input name="channel" maxlength="200"></label>
<label class="full">{e(f['note'])}<textarea name="note" maxlength="600" rows="3"></textarea></label>
<label class="full check"><input type="checkbox" name="consent" required> <span>{e(f['consent'])}</span></label>
<div class="full actions"><button class="btn" type="submit">{e(f['submit'])}</button><p class="form-msg" role="status"></p></div></form>'''
    body = f'''<section class="page event"><div class="wrap"><span class="eyebrow">{'체험단 1기' if l=='ko' else 'Tester programme · round 1'}</span><h1>{e(t['eventLead'])}</h1><p class="lead">{f'받침 마스터 — 쓰는 대로 읽지 않는 소리 18레슨. {EVENT["n"]}명이 먼저 써 보고 한 편씩 남깁니다.' if l=='ko' else f'Batchim Master — 18 lessons on sounds that don’t match the spelling. {EVENT["n"]} people try it first and each leave one review.'}</p>
<figure class="wide"><img src="/assets/art/scene_cheer.jpg" alt="" width="1600" height="893"></figure>
<ol class="steps">{steps_h}</ol>
<div class="two"><div><div class="sh"><h2>{'받는 것' if l=='ko' else 'What you get'}</h2></div><ul class="plain">{give_h}</ul></div><div><div class="sh"><h2>{'하는 것' if l=='ko' else 'What we ask'}</h2></div><ul class="plain">{ask_h}</ul></div></div>
<div class="sh" id="form"><h2>{'신청' if l=='ko' else 'Apply'}</h2><p>{a0} – {a1}</p></div>{form}<p class="note">{e(note)}</p></div></section>'''
    eh = '<script src="/assets/event-config.js?v=1"></script><script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script><script src="/assets/event.js?v=1" defer></script>'
    out(f'/{l}/event/index.html', shell(l, f'{t["event"]} — Hangeul Cubs', t['eventLead'], f'/{l}/event/', body, og='/assets/art/scene_cheer.jpg', extra_head=eh))

    # BOARD
    bt = '게시판' if l == 'ko' else 'Community'
    bl = '공지 · 자유·질문 · 후기·팬아트 · 오류·건의' if l == 'ko' else 'Notices · General & questions · Reviews & fan art · Bugs & ideas'
    body = f'<section class="page board-page"><div class="wrap"><span class="eyebrow">HANGEUL CUBS</span><h1>{e(bt)}</h1><p class="lead">{e(bl)}</p><div id="board" data-lang="{l}"><p class="b-msg">…</p></div></div></section>'
    bh = '<script src="/assets/board-config.js?v=1"></script><script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script><script src="/assets/board.js?v=1" defer></script>'
    out(f'/{l}/board/index.html', shell(l, f'{bt} — Hangeul Cubs', bl, f'/{l}/board/', body, extra_head=bh))

    # NEWS
    items = ''.join(f'<article><time>{n[0]}</time><h3>{e(n[1] if l=="ko" else n[3])}</h3><p>{e(n[2] if l=="ko" else n[4])}</p></article>' for n in NEWS)
    body = f'<section class="page"><div class="wrap"><span class="eyebrow">HANGEUL CUBS</span><h1>{e(t["news"])}</h1><div class="ngrid list">{items}</div></div></section>'
    out(f'/{l}/news/index.html', shell(l, f'{t["news"]} — Hangeul Cubs', 'AP Edu news', f'/{l}/news/', body))

out('/index.html', '<!doctype html><html><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/ko/"><link rel="canonical" href="https://edu.apholdings.kr/ko/"><script>location.replace((navigator.language||"").toLowerCase().startsWith("ko")?"/ko/":"/en/")</script></head><body></body></html>')
out('/404.html', '<!doctype html><html><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/ko/"></head><body></body></html>')
out('/CNAME', 'edu.apholdings.kr'); out('/.nojekyll', '')
urls = [f'/{l}/{s}' for l in ('ko', 'en') for s in ['', 'cubs/', 'episodes/', 'app/', 'event/', 'board/', 'news/'] + [f'cubs/{c["id"]}/' for c in CUBS]]
out('/sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{ORIGIN}{u}</loc></url>' for u in urls) + '</urlset>')
out('/robots.txt', f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')
print('built', len(urls), 'pages')
