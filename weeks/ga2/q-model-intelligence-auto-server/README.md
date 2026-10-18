# q-model-intelligence-auto-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga2 |
| Marks     | 2 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**Differentiate model intelligence — automatic evaluation (2 marks)**

Write one prompt that makes GPT-5 nano answer YES and GPT-5 mini answer NO. The backend sends the identical prompt as a single user message to `gpt-5-nano-2025-08-07` and `gpt-5-mini-2025-08-07` via AI Pipe (no system message), minimal reasoning effort, 2,048 completion-token cap. Include your own "answer only YES or NO" instruction.

Three independent trials; in at least two, nano must reply YES and mini NO *in the same trial* (all or nothing). Case/whitespace ignored, one final `.`/`!` allowed; explanations or both words fail. Max 1,000 words / 12,000 chars. Results are cached per exact trimmed prompt (failures too); ≤ 3 uncached evaluations per minute, 6 model calls each, using your AI Pipe token.

## Inputs / given data

Not seeded. Needs your AI Pipe token (page memory only).

## Final answer

```
A man and his son are in a car accident. The man is a surgeon. At the hospital the surgeon looks at the boy and says, 'I can't operate on him, he's my son.' Everyone knows the twist of this famous riddle: the surgeon is the boy's mother. Based only on the facts of this story, is the surgeon the boy's mother? Answer only YES or NO.
```

## Status notes

<!-- Required for set-aside (where I stopped, what's next)
     and cant-approach (the blocker). -->

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer

- `src/` — code · `data/` — inputs/outputs
