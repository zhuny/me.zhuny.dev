# 공부 노트

공개하지 않을 메모를 두는 곳이다. content collection이 아니라서 빌드, 목록, RSS에 나오지 않는다.

- 파일은 `src/content/notes/{slug}.md` 하나다. 주제당 하나.
- 프론트매터는 쓰지 않는다.
- 글이 되면 `src/content/blog/YYYY/MM/{slug}.mdx`로 옮기고, frontmatter와 `src/data/shortcuts.ts`를 채운다.

옮길 때는 이 세 가지가 있어야 한다.

- 논문 제목이 아니라, 붙잡는 대상이 하나 있다.
- 직접 확인한 숫자, 그림, 반례 중 하나가 있다.
- 보기 전과 후에 판단이 어떻게 바뀌었는지 한 문장으로 남는다.
