# AP Edu — Hangeul Cubs 공식 사이트 (edu.apholdings.kr)

AP Games(games.apholdings.kr)와 같은 구조의 정적 사이트. `python3 build.py` 로 `ko/` `en/` 를 다시 만든다.

- `content.py` — 4남매 · 앱 레슨(무료 42 + 받침 마스터 18) · 유튜브 에피소드 · 체험단 일정 · 소식
- `build.py` — KO/EN 페이지 생성 (홈 · 4남매 · 캐릭터 4 · 에피소드 · 앱 · 체험단 · 게시판 · 소식)
- `assets/board.js` — AP Games 게시판과 같은 Supabase `board` 스키마, `game = hangeulcubs` (설정 `board-config.js`)
- `assets/event.js` — 체험단 신청 → A.P Holdings Supabase `edu_event_applications` (insert 전용, 설정 `event-config.js`)
- 공개(publishable) 키만 둔다. secret / service_role 키는 절대 넣지 않는다.
- 캐릭터 3D 원화·2D 모델 시트·유튜브 썸네일은 `assets/art` `assets/yt`. 새 그림은 대표 원화 우선.
