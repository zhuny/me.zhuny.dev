# 블로그 글 추가

새 글을 만들거나 이동할 때:

1. `src/content/blog/YYYY/MM/{slug}.mdx` 생성
2. `src/data/shortcuts.ts`에 hex → slug 매핑 추가
3. slug 형식: `YYYY/MM/{filename-without-ext}` (content collection id와 동일)

## 새 글 작성 규칙

새 글을 추가할 때는 **frontmatter만 있는 빈 템플릿**으로 시작한다.
본문 내용은 작성자가 직접 채운다. 자동으로 초안이나 본문을 생성하지 않는다.
템플릿은 다음을 복사해 사용한다.

```mdx
---
title: ''
description: ''
pubDate: 'Jan 1 2026'
---
```

필요하면 `heroImage`, `updatedDate`, `youtube` 등을 frontmatter에 추가한다.

## shortcuts 등록 예시

```ts
"c7e52b9d": '2026/05/spanning-tree',
```

- hex는 8자리 임의 문자열 (기존 항목과 겹치지 않게)
- slug는 파일 경로에서 `src/content/blog/`와 확장자를 뺀 값
- 숏링크: `/z/{hex}` → `/blog/{slug}`로 리다이렉트
