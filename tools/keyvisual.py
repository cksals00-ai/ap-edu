# -*- coding: utf-8 -*-
"""30일 챌린지 키비주얼 v2 — 이벤트 포스터 구성(노란 바탕 · 큰 제목 · 말풍선 · 폰 목업 · 아래에서 고개 내민 4남매).
기존 3D 원화 컷아웃과 앱 화면만 사용, 힉스필드 생성 없음. python3 tools/keyvisual.py assets/art"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os, sys
ART = os.path.join(os.path.dirname(__file__), '..', 'assets', 'art')
BLACK = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
YEL = (255, 208, 64); YEL2 = (255, 224, 120); INK = (43, 33, 24); BROWN = (74, 44, 22); TEAL = (35, 125, 115); WHITE = (255, 255, 255)

def font(path, size):
    for idx in (2, 0):
        try: return ImageFont.truetype(path, size, index=idx)
        except Exception: pass
    return ImageFont.load_default()

def cutout(name, height):
    im = Image.open(os.path.join(ART, f'{name}_3d.png')).convert('RGBA')
    a = im.split()[3].filter(ImageFilter.MinFilter(5)); im.putalpha(a)
    # 살짝 따뜻하게 — 노란 바탕과 톤 맞추기
    rgb = ImageEnhance.Color(im.convert('RGB')).enhance(1.08); im = Image.merge('RGBA', (*rgb.split(), a))
    sc = height / im.height; return im.resize((int(im.width*sc), height), Image.LANCZOS)

def shadow_of(im, blur=16, alpha=110, dy=10):
    sh = Image.new('RGBA', (im.width+blur*4, im.height+blur*4), (0, 0, 0, 0))
    s = Image.new('RGBA', im.size, (90, 50, 0, alpha)); s.putalpha(im.split()[3])
    sh.paste(s, (blur*2, blur*2+dy), s); return sh.filter(ImageFilter.GaussianBlur(blur))

def paste_shadowed(base, im, x, y, blur=16, alpha=110, dy=10):
    sh = shadow_of(im, blur, alpha, dy); base.paste(sh, (x-blur*2, y-blur*2), sh); base.paste(im, (x, y), im)

def background(W, H):
    im = Image.new('RGB', (W, H), YEL); d = ImageDraw.Draw(im)
    # 은은한 점 무늬
    for y in range(0, H, 46):
        for x in range((y//46 % 2)*23, W, 46):
            d.ellipse((x-3, y-3, x+3, y+3), fill=(255, 216, 92))
    # 위쪽 밝은 빛
    glow = Image.new('RGB', (W, H), YEL); g = ImageDraw.Draw(glow); g.ellipse((-W*0.2, -H*0.5, W*0.9, H*0.5), fill=YEL2)
    im = Image.blend(im, glow.filter(ImageFilter.GaussianBlur(W*0.12)), 0.55)
    return im

def outlined(d, xy, text, f, fill, outline, w):
    x, y = xy
    for dx in range(-w, w+1):
        for dy in range(-w, w+1):
            if dx*dx+dy*dy <= w*w: d.text((x+dx, y+dy), text, font=f, fill=outline)
    d.text((x, y), text, font=f, fill=fill)

def bubble(d, box, radius, fill, tail=('b', 0.5)):
    x0, y0, x1, y1 = box; d.rounded_rectangle(box, radius=radius, fill=fill)
    side, t = tail; w = 26
    if side == 'b':
        cx = x0 + (x1-x0)*t; d.polygon([(cx-w, y1-2), (cx+w, y1-2), (cx+6, y1+34)], fill=fill)
    else:
        cy = y0 + (y1-y0)*t; d.polygon([(x1-2, cy-w), (x1-2, cy+w), (x1+34, cy+6)], fill=fill)

def phone(screen_h):
    """앱 「배우고 듣고」 화면을 넣은 폰 목업"""
    src = Image.open(os.path.join(ART, 'screens.jpg')).convert('RGB').crop((579, 160, 820, 738))
    sw = int(src.width * screen_h / src.height); scr = src.resize((sw, screen_h), Image.LANCZOS)
    bz = int(screen_h * 0.028); W, H = sw + bz*2, screen_h + bz*2
    ph = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ph)
    d.rounded_rectangle((0, 0, W-1, H-1), radius=int(W*0.16), fill=(28, 24, 22))
    mask = Image.new('L', scr.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw-1, screen_h-1), radius=int(W*0.12), fill=255)
    ph.paste(scr, (bz, bz), mask)
    d.rounded_rectangle((W*0.35, bz+6, W*0.65, bz+6+int(H*0.022)), radius=20, fill=(28, 24, 22))  # 노치
    return ph

def poster(lang, W, H, out):
    im = background(W, H); d = ImageDraw.Draw(im)
    tall = H > W  # 4:5 vs 16:9
    if lang == 'ko':
        top = 'HANGEUL CUBS'; t1 = '한글컵스'; t2 = '30일 챌린지'; sub = '11월 한 달, 4남매와 한글 · 후기 남기면'; prize1 = '한 명에게'; prize2 = 'Meta AI 글래스'; when = '신청 10.13 – 10.31'; site = 'edu.apholdings.kr'
        small = '+ 격려상 5명 · 나라 상관없이 · 참가 무료'; fine = 'AP EDU · A.P HOLDINGS   Meta·Ray-Ban·YouTube는 후원사가 아닙니다'
    else:
        top = 'HANGEUL CUBS'; t1 = '30-Day'; t2 = 'Challenge'; sub = 'All of November · learn, then review'; prize1 = 'One learner wins'; prize2 = 'Meta AI glasses'; when = 'Apply 13 – 31 Oct'; site = 'edu.apholdings.kr'
        small = '+ 5 prizes · any country · free entry'; fine = 'AP EDU · A.P HOLDINGS   Meta, Ray-Ban and YouTube are not sponsors'
    s = W / 1080  # 스케일 기준 1080폭
    if tall:
        # ── 4:5 세로 (인스타) ──
        d.text((W/2 - d.textlength(top, font=font(BOLD, int(30*s)))/2, int(70*s)), top, font=font(BOLD, int(30*s)), fill=BROWN)
        f1 = font(BLACK, int(118*s)); f2 = font(BLACK, int(132*s))
        for t, f, y, col in ((t1, f1, int(118*s), TEAL), (t2, f2, int(240*s), INK)):
            tw = d.textlength(t, font=f); outlined(d, ((W-tw)/2, y), t, f, col, WHITE, int(8*s))
        fs = font(BOLD, int(34*s)); tw = d.textlength(sub, font=fs); d.text(((W-tw)/2, int(408*s)), sub, font=fs, fill=BROWN)
        # 말풍선 (경품)
        bw, bh = int(600*s), int(170*s); bx, by = int(60*s), int(480*s)
        bubble(d, (bx, by, bx+bw, by+bh), int(40*s), BROWN, ('r', 0.5))
        d.text((bx+int(36*s), by+int(26*s)), prize1, font=font(BOLD, int(30*s)), fill=(255, 226, 150))
        d.text((bx+int(36*s), by+int(68*s)), prize2, font=font(BLACK, int(58*s)), fill=YEL)
        # 날짜 배지 + 사이트
        fw = font(BLACK, int(34*s)); tw = d.textlength(when, font=fw); d.rounded_rectangle((bx, int(690*s), bx+tw+int(60*s), int(752*s)), radius=int(31*s), fill=INK)
        d.text((bx+int(30*s), int(700*s)), when, font=fw, fill=YEL)
        d.text((bx, int(772*s)), site, font=font(BLACK, int(30*s)), fill=BROWN)
        d.text((bx, int(820*s)), small, font=font(BOLD, int(25*s)), fill=BROWN)
        # 폰
        ph = phone(int(520*s)); paste_shadowed(im, ph, int(720*s), int(450*s), blur=int(22*s), alpha=120, dy=int(16*s)); d = ImageDraw.Draw(im)
        # 4남매 — 아래에서 고개 내밀기
        floor = int(1215*s)
        for n, h_, x in (('kkobi', 470, 150), ('daho', 520, 400), ('aari', 500, 690), ('rami', 480, 930)):
            c = cutout(n, int(h_*s)); paste_shadowed(im, c, int(x*s) - c.width//2, floor - int(h_*s) + int(110*s), blur=int(18*s), alpha=100)
        d = ImageDraw.Draw(im); d.rectangle((0, floor, W, H), fill=BROWN)
        for x in range(0, W, int(90*s)): d.line((x, floor, x, H), fill=(92, 58, 30), width=2)
        d.line((0, floor+int(38*s), W, floor+int(38*s)), fill=(92, 58, 30), width=2)
        ff = font(BOLD, int(17*s)); tw = d.textlength(fine, font=ff); d.text(((W-tw)/2, floor + int(80*s)), fine, font=ff, fill=(210, 180, 140))
    else:
        # ── 16:9 가로 (사이트·유튜브) ──
        s = H / 900
        d.text((int(90*s), int(70*s)), top, font=font(BOLD, int(28*s)), fill=BROWN)
        f1 = font(BLACK, int(96*s if lang=='ko' else 84*s)); f2 = font(BLACK, int(112*s if lang=='ko' else 96*s))
        outlined(d, (int(86*s), int(110*s)), t1, f1, TEAL, WHITE, int(7*s)); outlined(d, (int(86*s), int(215*s)), t2, f2, INK, WHITE, int(7*s))
        d.text((int(90*s), int(365*s)), sub, font=font(BOLD, int(30*s)), fill=BROWN)
        bw, bh = int(560*s), int(160*s); bx, by = int(86*s), int(440*s)
        bubble(d, (bx, by, bx+bw, by+bh), int(36*s), BROWN, ('b', 0.28))
        d.text((bx+int(32*s), by+int(22*s)), prize1, font=font(BOLD, int(28*s)), fill=(255, 226, 150))
        d.text((bx+int(32*s), by+int(62*s)), prize2, font=font(BLACK, int(58*s)), fill=YEL)
        fw = font(BLACK, int(30*s)); tw = d.textlength(when, font=fw); d.rounded_rectangle((bx, int(660*s), bx+tw+int(56*s), int(716*s)), radius=int(28*s), fill=INK)
        d.text((bx+int(28*s), int(669*s)), when, font=fw, fill=YEL)
        d.text((bx+tw+int(80*s), int(676*s)), site, font=font(BOLD, int(26*s)), fill=BROWN)
        d.text((int(90*s), int(738*s)), small, font=font(BOLD, int(24*s)), fill=BROWN)
        ph = phone(int(470*s)); paste_shadowed(im, ph, int(660*s if lang=='ko' else 720*s), int(90*s), blur=int(22*s), alpha=120, dy=int(16*s)); d = ImageDraw.Draw(im)
        floor = int(820*s)
        for n, h_, x in (('kkobi', 470, 940), ('daho', 520, 1105), ('aari', 500, 1260), ('rami', 480, 1410)):
            c = cutout(n, int(h_*s)); paste_shadowed(im, c, int(x*s) - c.width//2, floor - int(h_*s) + int(100*s), blur=int(16*s), alpha=100)
        d = ImageDraw.Draw(im); d.rectangle((0, floor, W, H), fill=BROWN)
        for x in range(0, W, int(90*s)): d.line((x, floor, x, H), fill=(92, 58, 30), width=2)
        ff = font(BOLD, int(16*s)); d.text((int(90*s), floor + int(30*s)), fine, font=ff, fill=(210, 180, 140))
    im.save(out, quality=90, optimize=True); return out

if __name__ == '__main__':
    o = sys.argv[1] if len(sys.argv) > 1 else '.'
    for l in ('ko', 'en'):
        print(poster(l, 1600, 900, os.path.join(o, f'challenge_kv_{l}.jpg')), poster(l, 1080, 1350, os.path.join(o, f'challenge_sq_{l}.jpg')))
