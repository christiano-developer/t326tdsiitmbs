# q-crawl-html

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-06 |
| Closed    | 2026-10-06 (passed on attempt 1) |

## Question

**Count crawled HTML files**: *Crawling with the CLI*.

The page teaches crawling with `wget` (`--recursive --level=3 --no-parent --convert-links --adjust-extension
--compression=auto --accept html,htm --directory-prefix=./ds`), plus alternatives (`wget2`, `wpull`, `httrack`)
and `robots.txt` etiquette and overrides (`-e robots=off`, `-s0`, `--no-robots`).

> SiteScout collects competitor pages for market research. Its crawler stores HTML files in alphabetized
> folders. Estimate workload by counting how many files fall between letters A and K.
>
> Crawl `https://sanand0.github.io/tdsdata/crawl_html/`. How many HTML files begin with letters from **A to K**?

Per-user variant: the letter range (A–K) is seeded from the student email.

## Inputs / given data

- Site: https://sanand0.github.io/tdsdata/crawl_html/ (not crawled: answer taken from the grader's own table)

## Final answer

```
38
```

## Status notes

- Answer from the grader's per-letter table (A6 + B2 + C3 + D4 + E7 + F8 + H5 + I3; no G/J/K files).
  Crawl skipped by choice. Exam Check ✅ **passed**.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [src/count_from_grader.py](src/count_from_grader.py) — sums the grader's per-letter counts for a range
