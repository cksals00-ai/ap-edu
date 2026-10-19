# 한글컵스 쇼츠 도구 (2026-09-29)
- `mk_lesson.py specs.json [이름…]` — 레슨 원본(16:9)에서 구간을 잘라 1080×1920 쇼츠로. layout A = 좌 캐릭터·우 카드(레슨 1형), B = 전체 화면 + 아래 단어 카드(레슨 2형). 자막 PNG를 구간별로 얹고 −14 LUFS.
- `quiz.py` — 캐릭터 없는 듣기 퀴즈(성인 초보 대상, 아동용 아님). 레슨 음성 클립 3개 + 카운트다운 + 정답 공개.
- 원본 레슨 mp4는 저장소에 두지 않는다(용량). 1주차 결과물: 맥 `~/Documents/HangeulCubs_video/shorts_w1/` + `UPLOAD_GUIDE.md`.
- 2주차(2026-10-19): layout `A2` 추가 — 레슨 6~10 v2 화면 배치용(캐릭터 900×720@100,30 → 700×560, 카드 740×900@1090,90 → 480×584). `specs_w2.json` 참조. 자막 타이밍은 faster-whisper 단어 타임스탬프(클라우드)에서 잡음. 결과물: 맥 `~/Documents/HangeulCubs_video/shorts_w2/` + `UPLOAD_GUIDE.md`, 공개 주소 https://www.apholdings.kr/media/lia/cubs/W1~W5.mp4
