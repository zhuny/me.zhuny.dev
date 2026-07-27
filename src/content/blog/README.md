# 블로그 글 추가

새 글을 만들거나 이동할 때:

1. `src/content/blog/YYYY/MM/{slug}.mdx` 생성
2. `src/data/shortcuts.ts`에 hex → slug 매핑 추가
3. slug 형식: `YYYY/MM/{filename-without-ext}` (content collection id와 동일)

## shortcuts 등록 예시

```ts
"a1d8f4e6": '2026/07/25-horses',
```

- hex는 8자리 임의 문자열 (기존 항목과 겹치지 않게)
- slug는 파일 경로에서 `src/content/blog/`와 확장자를 뺀 값
- 숏링크: `/z/{hex}` → `/blog/{slug}`로 리다이렉트
