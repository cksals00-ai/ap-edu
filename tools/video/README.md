# 한글컵스 유튜브 — 오프닝 스팅 · 엔드카드 도구

**정책 (2026-09-29 대표 확정):** 앞으로 올리는 한글컵스 **본편**(쇼츠 제외)은 전부
`[스팅 3초] + [본편] + [엔드카드 12초]` 로 올린다. 이미 올린 10편은 그대로 둔다(주소·조회수 유지).
8초 풀 인트로(`trailer/`)는 **채널 예고편·새 시리즈 첫 편**에만 쓴다.

## 한 편 만드는 순서
```bash
cd tools/video && python3 -m http.server 8792 &     # 템플릿은 localhost:8792 에서 연다
python3 sfx_wrap.py                                  # sting.wav · outro.wav (엔드카드 목소리는 voices/*.wav 필요 — piper kristin)
./make.sh sting_L06 "sting.html?n=6&letter=ㅡ&rom=EU&series=FIRST%20STEPS&cub=daho" 3.0 sting.wav
./make.sh outro_L06 "outro.html?next=ㅣ&nextRom=I" 12.0 outro.wav
./cubs_wrap.sh 본편.mp4 out/sting_L06.mp4 out/outro_L06.mp4 EP06_upload.mp4 EP06_en.srt
```
- `cub` = 이번 편 진행 캐릭터 색(daho·kkobi·aari·rami). `series` = FIRST STEPS / REAL KOREAN / PARENT GUIDE.
- 자막은 스크립트가 **+3초** 밀어 준다. **설명란 챕터도 전부 +0:03** 하고 맨 앞에 `0:00 Intro` 추가.
- 음량은 합친 뒤 −14 LUFS 로 맞춘다.

## 아동용 영상은 엔드카드가 다르다 (2026-09-29 확인)
유튜브 규칙(COPPA)상 **아동용으로 설정한 영상은 댓글·알림 종·최종 화면·카드가 자동으로 꺼진다.**
글자 레슨·회화편처럼 아이 대상 영상은 아동용으로 두는 게 맞으므로(바꾸면 법 위반 소지) 구독 유도 연출이 먹히지 않는다.
- 아동용(글자 레슨·회화편): `outro.html?kids=1&next=ㅣ&nextRom=I` + `outro_kids.wav` — 다음 글자 타일 + 앱 안내만, 구독·좋아요 연출 없음
- 아동용 아님(성인 초보·부모 가이드): 기본 엔드카드(구독 → 좋아요 → 알림 + 최종 화면 자리)

## 업로드할 때 (유튜브 스튜디오)
- **최종 화면**: 엔드카드가 시작되는 순간(끝에서 12초)부터 끝까지.
  동영상 A = 다음 레슨 `x110 y300 w620 h349` · 재생목록 B = 「Hangeul Cubs — Vowels」 `x790 y300` · 구독 = 원 중심 `(1640,470)` 지름 250.
  두 번째 편부터는 「동영상에서 가져오기」로 앞 편 최종 화면을 복사한 뒤 A만 바꾼다.
- 시청자층은 **내용대로** 정한다 — 아이 대상 레슨은 아동용(최종 화면 없음), 성인·부모 영상은 아동용 아님.
- 문구 규칙: 구독·좋아요는 **부탁만** 한다. 경품·혜택과 엮지 않는다(30일 챌린지 규칙과 같음).
