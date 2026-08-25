# 블로그 글 추가

사용자는 제목만 준다. 예를 들면 다음과 같다.

> 「ChatGPT야 십자수 용 도트 그래픽 그려줘」라는 제목으로 블로그 글을 쓸려고 해

이 말은 **빈 글 뼈대를 만들라**는 뜻이다.
제목에서 slug와 날짜 같은 메타데이터는 정하되, 본문은 쓰지 않는다.
본문까지 원하면 그때 따로 말한다.

## 할 일

1. `src/content/blog/YYYY/MM/{slug}.mdx` 생성
2. frontmatter만 채운 빈 템플릿으로 둔다
3. `src/data/shortcuts.ts`에 hex → slug 매핑 추가

slug 형식은 `YYYY/MM/{filename-without-ext}`이고, content collection id와 같다.
디렉토리 `YYYY/MM`은 `pubDate` 기준이다. 확장자는 `.mdx`다.

## 제목만 있을 때 채우는 값

| 필드 | 규칙 |
| --- | --- |
| `title` | 사용자가 준 제목 그대로 |
| `description` | 비운다 (`''`) |
| `pubDate` | 오늘 날짜. 형식은 `'Aug 25 2026'` |
| 파일명 | 제목을 영어 소문자 kebab-case로 옮긴다 |
| hex | 기존과 겹치지 않는 8자리 |

`heroImage`, `updatedDate`, `youtube`는 사용자가 주거나 파일이 이미 있을 때만 넣는다.

템플릿:

```mdx
---
title: ''
description: ''
pubDate: 'Jan 1 2026'
---
```

## 파일명 규칙

파일명(slug 마지막 세그먼트)은 **영어 소문자 kebab-case**다.
한글 제목·한글 주제어를 파일명에 그대로 넣지 않는다.

- 소문자만 사용
- 단어는 하이픈(`-`)으로 구분
- 공백, 한글, 특수문자 없음
- 제목(`title`)은 한글이어도 되고, 파일명과 달라도 된다

예시:

| title | 파일명 |
| --- | --- |
| 밀집한 전력 공급기 (Spanning Tree) | `spanning-tree.mdx` |
| 이름 기반 이메일 생성 | `name-email-collision.mdx` |
| 붕어섬의 친환경 비늘 | `solar-efficiency.mdx` |
| ChatGPT야 십자수 용 도트 그래픽 그려줘 | `chatgpt-cross-stitch.mdx` |

## shortcuts

```ts
"c7e52b9d": '2026/05/spanning-tree',
```

- hex는 8자리 임의 문자열 (기존 항목과 겹치지 않게)
- slug는 파일 경로에서 `src/content/blog/`와 확장자를 뺀 값
- 숏링크: `/z/{hex}` → `/blog/{slug}`로 리다이렉트
