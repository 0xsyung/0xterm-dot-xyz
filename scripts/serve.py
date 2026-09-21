#!/usr/bin/env python3
"""Static preview server with GH Pages–like /app/* → 404.html rewrite.

GitHub Pages serves the root 404.html body for missing paths (URL stays).
Plain `python -m http.server` does not — this mirrors Pages so tunnel QA
matches production for legacy /app bookmarks.
"""
from __future__ import annotations

import argparse
import mimetypes
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parent.parent


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path != "/" and path.endswith("/"):
            path = path.rstrip("/") or "/"

        # Map URL path → filesystem under ROOT
        if path == "/":
            fs = ROOT / "index.html"
        else:
            rel = path.lstrip("/")
            fs = ROOT / rel
            if fs.is_dir():
                fs = fs / "index.html"

        if fs.is_file():
            self._send_file(fs, 200)
            return

        # GH Pages behavior: missing /app/* gets root 404.html (JS redirects).
        if path == "/app" or path.startswith("/app/"):
            not_found = ROOT / "404.html"
            if not_found.is_file():
                self._send_file(not_found, 404)
                return

        self.send_error(404, "File not found")

    def _send_file(self, fs: Path, status: int) -> None:
        data = fs.read_bytes()
        ctype, _ = mimetypes.guess_type(str(fs))
        if ctype is None:
            ctype = "application/octet-stream"
        if fs.suffix in {".html", ".htm"}:
            ctype = "text/html; charset=utf-8"
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt: str, *args) -> None:
        sys_stderr = __import__("sys").stderr
        sys_stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=4173)
    args = ap.parse_args()
    os.chdir(ROOT)
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"serving {ROOT} at http://{args.host}:{args.port}/ (Pages-like /app/*)", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
