# -*- coding: utf-8 -*-
"""30일 챌린지 키비주얼 — 기존 3D 원화 컷아웃 + 타이포 + 안경 아이콘(브랜드 로고 없음). 힉스필드 없이 PIL로 합성."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, sys
ART = os.path.join(os.path.dirname(__file__), '..', 'assets', 'art')
BLACK = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
INK = (43, 33, 24); HONEY = (232, 155, 42); TEAL = (47, 143, 131); MUTED = (138, 122, 104)

def font(path, size):
    for idx in (2, 0):  # ttc index 2 = KR in NotoSansCJK
        try: return ImageFont.truetype(path, size, index=idx)
        except Exception: pass
    return ImageFont.load_default()

def bg(w, h):
    im = Image.new('RGB', (w, h), (255, 247, 234))
    d = ImageDraw.Draw(im)
    # soft honey blobs
    glow = Image.new('RGB', (w, h), (255, 247, 234)); g = ImageDraw.Draw(glow)
    g.ellipse((w*0.45, -h*0.35, w*1.25, h*0.75), fill=(255, 224, 178))
    g.ellipse((-w*0.25, h*0.55, w*0.45, h*1.35), fill=(255, 233, 200))
    glow = glow.filter(ImageFilter.GaussianBlur(w*0.09))
    im = Image.blend(im, glow, 0.9)
    return im

def glasses(size, color=INK):
    """단순 안경 아이콘 — 둥근 렌즈 두 개, 브릿지, 다리. 특정 브랜드 형태가 아님."""
    s = size; im = Image.new('RGBA', (s*2, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    lw = max(4, s//14); r = s*0.42
    for cx in (s*0.52, s*1.48):
        d.rounded_rectangle((cx-r, s*0.22, cx+r, s*0.22+r*1.55), radius=r*0.45, outline=color, width=lw, fill=(255, 255, 255, 60))
    d.line((s*0.52+r, s*0.42, s*1.48-r, s*0.42), fill=color, width=lw)
    d.line((s*0.10, s*0.34, s*0.52-r, s*0.30), fill=color, width=lw)
    d.line((s*1.48+r, s*0.30, s*1.90, s*0.34), fill=color, width=lw)
    # small camera dot (AI glasses hint)
    d.ellipse((s*0.10, s*0.24, s*0.10+lw*1.6, s*0.24+lw*1.6), fill=TEAL)
    return im

def cutout(name, height):
    im = Image.open(os.path.join(ART, f'{name}_3d.png')).convert('RGBA')
    a = im.split()[3].filter(ImageFilter.MinFilter(5))  # 테두리 흰 띠 제거 (알파 2px 안쪽으로)
    im.putalpha(a)
    sc = height / im.height; return im.resize((int(im.width*sc), height), Image.LANCZOS)

def shadow(im, blur=18, alpha=90):
    sh = Image.new('RGBA', (im.width+blur*4, im.height+blur*4), (0, 0, 0, 0))
    a = im.split()[3]; s = Image.new('RGBA', im.size, (60, 30, 0, alpha)); s.putalpha(a)
    sh.paste(s, (blur*2, blur*2+int(blur*0.8)), s); return sh.filter(ImageFilter.GaussianBlur(blur))

def wide(lang='ko', out='challenge_kv.jpg'):
    W, H = 1600, 900; im = bg(W, H); d = ImageDraw.Draw(im)
    # cubs on the right
    names = ['daho', 'kkobi', 'aari', 'rami']; hts = [470, 430, 455, 440]; xs = [1000, 1150, 1300, 1450]
    for n, h_, x in zip(names, hts, xs):
        c = cutout(n, h_); sh = shadow(c)
        y = H - c.height - 60
        im.paste(sh, (x - c.width//2 - 36, y - 36), sh); im.paste(c, (x - c.width//2, y), c)
    d = ImageDraw.Draw(im)
    if lang == 'ko':
        eyebrow = 'HANGEUL CUBS · 30일 챌린지'; t1 = '30일, 4남매와 한글.'; t2 = '한 명에게'; t3 = 'Meta AI 글래스.'
        sub = '11월 한 달 · 앱 + 유튜브로 배우고 후기 남기기'; when = '신청 10.13 – 10.31 · edu.apholdings.kr'
    else:
        eyebrow = 'HANGEUL CUBS · 30-DAY CHALLENGE'; t1 = '30 days of Korean.'; t2 = 'Meta AI glasses'; t3 = 'for one of you.'
        sub = 'All of November · learn with the app + YouTube, post a review'; when = 'Apply 13 – 31 Oct · edu.apholdings.kr'
    d.text((90, 110), eyebrow, font=font(BOLD, 26), fill=TEAL)
    f1 = font(BLACK, 82 if lang == 'ko' else 78)
    d.text((88, 160), t1, font=f1, fill=INK)
    d.text((88, 262), t2, font=f1, fill=INK)
    d.text((88, 364), t3, font=f1, fill=HONEY)
    d.text((90, 490), sub, font=font(BOLD, 30), fill=MUTED)
    # date pill
    fp = font(BOLD, 28); tw = d.textlength(when, font=fp)
    d.rounded_rectangle((90, 560, 90+tw+52, 620), radius=30, fill=INK)
    d.text((116, 573), when, font=fp, fill=(255, 255, 255))
    # glasses icon
    g = glasses(150); im.paste(g, (92, 660), g)
    d = ImageDraw.Draw(im)
    d.text((420, 690), '1명 · Ray-Ban Meta' if lang == 'ko' else '1 winner · Ray-Ban Meta', font=font(BLACK, 36), fill=INK)
    d.text((420, 745), '+ 격려상 5명' if lang == 'ko' else '+ 5 encouragement prizes', font=font(BOLD, 26), fill=MUTED)
    d.text((90, 845), 'AP EDU · A.P HOLDINGS   Meta·Ray-Ban·YouTube는 후원사가 아닙니다' if lang == 'ko' else 'AP EDU · A.P HOLDINGS   Meta, Ray-Ban and YouTube are not sponsors', font=font(BOLD, 16), fill=MUTED)
    im.save(out, quality=88, optimize=True); return out

def square(lang='ko', out='challenge_sq.jpg'):
    W = H = 1080; im = bg(W, H)
    names = ['daho', 'kkobi', 'aari', 'rami']; hts = [400, 360, 385, 370]; xs = [190, 400, 640, 880]
    for n, h_, x in zip(names, hts, xs):
        c = cutout(n, h_); sh = shadow(c, 14, 80); y = H - c.height - 70
        im.paste(sh, (x - c.width//2 - 28, y - 28), sh); im.paste(c, (x - c.width//2, y), c)
    d = ImageDraw.Draw(im)
    if lang == 'ko':
        lines = [('HANGEUL CUBS · 30일 챌린지', BOLD, 26, TEAL, 80), ('30일, 4남매와 한글.', BLACK, 72, INK, 122), ('한 명에게 Meta AI 글래스.', BLACK, 64, HONEY, 212), ('신청 10.13 – 10.31 · edu.apholdings.kr', BOLD, 30, MUTED, 312)]
    else:
        lines = [('HANGEUL CUBS · 30-DAY CHALLENGE', BOLD, 26, TEAL, 80), ('30 days of Korean.', BLACK, 72, INK, 122), ('Meta AI glasses for one.', BLACK, 64, HONEY, 212), ('Apply 13 – 31 Oct · edu.apholdings.kr', BOLD, 30, MUTED, 312)]
    for t, fp, sz, col, y in lines:
        f = font(fp, sz); tw = d.textlength(t, font=f); d.text(((W-tw)/2, y), t, font=f, fill=col)
    g = glasses(120); im.paste(g, ((W - g.width)//2, 380), g)
    im.save(out, quality=88, optimize=True); return out

if __name__ == '__main__':
    o = sys.argv[1] if len(sys.argv) > 1 else '.'
    for l in ('ko', 'en'):
        print(wide(l, os.path.join(o, f'challenge_kv_{l}.jpg')), square(l, os.path.join(o, f'challenge_sq_{l}.jpg')))
