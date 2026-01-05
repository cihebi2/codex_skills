# codex_skills

This repo contains personal Codex skills.

## Skills

- `dl-paper-code-blog/` - Write Chinese blog posts from a paper+code bundle, enforce cropped figures, upload figures to Lsky, and (optionally) query local journal metrics (JCR/CAS) from a generated SQLite DB.
- `lsky-uploader/` - Upload files to a self-hosted Lsky Pro instance and return URLs/Markdown snippets.

## Install (Codex)

Option A: Use the built-in `skill-installer` (downloads from GitHub):

```bash
scripts/install-skill-from-github.py --repo cihebi2/codex_skills --path dl-paper-code-blog lsky-uploader
```

Option B: Clone and copy the folders into `~/.codex/skills/`.

## Notes

- `dl-paper-code-blog/references/journal_metrics_2025.sqlite3` is generated locally from your Excel tables and is intentionally gitignored. Build it with:
  - `python dl-paper-code-blog/scripts/build_journal_metrics_db.py --xlsx "D:/game/2025科睿唯安JCR分区表+2025中科院分区表1.xlsx" --overwrite`

