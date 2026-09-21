# 0xterm.xyz

Marketing apex for [0xterm](https://app.0xterm.xyz/) — GitHub Pages at `/` (`CNAME` = `0xterm.xyz`).

- Landing: static `index.html` (phosphor / scramble hero)
- Terminal: `https://app.0xterm.xyz/`
- Legacy `/app` bookmarks: silent redirect → app host

`.nojekyll` keeps Pages from treating this as a Jekyll site.

## `/app` and `/app/*` redirects

Production **GitHub Pages** serves the root [`404.html`](./404.html) body for any
missing path while keeping the browser URL. That page detects `/app` /
`/app/…` and `location.replace`s to `https://app.0xterm.xyz` with the rest of
the path, query, and hash.

Bare `/app` also has [`app/index.html`](./app/index.html) (same JS redirect).

**Ownership:** Pages’ custom-404 behavior owns nested `/app/*` in production.
Verify on the live apex after merge (`https://0xterm.xyz/app/foo?x=1`).

Plain static servers (`python -m http.server`, bare `cloudflared --url` over
them) do **not** serve `404.html` for missing paths. For local / tunnel QA that
matches Pages, use:

```bash
python3 scripts/serve.py --port 4173
# then: cloudflared tunnel --url http://127.0.0.1:4173
```
