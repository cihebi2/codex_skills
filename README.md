# codex_skills

This repo contains personal Codex skills.

## Skills

- `dl-paper-code-blog/` - Write Chinese blog posts from a paper+code bundle, enforce cropped figures, upload figures to Lsky, query local journal metrics (JCR/CAS), and provide QA gates + self-review checklist.
- `lsky-uploader/` - Upload files to a self-hosted Lsky Pro instance and return URLs/Markdown snippets.

## Install (Codex)

Option A: Use the built-in `skill-installer` (downloads from GitHub):

```bash
scripts/install-skill-from-github.py --repo cihebi2/codex_skills --path dl-paper-code-blog lsky-uploader
```

Option B: Clone and copy the folders into `~/.codex/skills/`.

## Notes

- `dl-paper-code-blog/references/journal_metrics_2025.sqlite3` is generated locally from your Excel tables and is intentionally gitignored. Build it with:
  - `python dl-paper-code-blog/scripts/build_journal_metrics_db.py --overwrite` (auto-detects a JCR/CAS xlsx under `D:/game/`) or pass `--xlsx <path>`.
- After drafting a post, run:
  - `python dl-paper-code-blog/scripts/check_article_requirements.py <blog.md> --require-urls`
  - `python dl-paper-code-blog/scripts/check_article_length.py <blog.md> --min 5000 --max 7000`
  - and follow `dl-paper-code-blog/references/self_review.md` for the final human polish.
