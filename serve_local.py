"""Local server with smart upstream proxy: isolation headers, byte ranges, local overrides, and streaming proxy."""
import argparse, gzip, io, json, mimetypes, os, re, shutil, ssl, sys, urllib.request, urllib.error, webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, parse_qs

LOCAL_DIR = Path(__file__).resolve().parent
MIRROR_ROOT = LOCAL_DIR / 'mirror' / 'playgta5.com'
CACHE_DIR = LOCAL_DIR / '.cache'
CACHE_DIR.mkdir(exist_ok=True)

UPSTREAM = 'https://gta.deloskiyt.pl'

mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('text/javascript', '.js')
mimetypes.add_type('font/woff', '.woff')
mimetypes.add_type('image/webp', '.webp')

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

class HybridHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.byte_range = None
        super().__init__(*args, directory=str(LOCAL_DIR), **kwargs)

    def end_headers(self):
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        self.send_header('Cross-Origin-Resource-Policy', 'same-origin')
        self.send_header('Accept-Ranges', 'bytes')
        super().end_headers()

    def find_local_file(self, clean_path):
        if clean_path in ('', '/', '/index.html'):
            target = LOCAL_DIR / 'index.html'
            if target.is_file(): return target
            target = LOCAL_DIR / 'homepage.html'
            if target.is_file(): return target

        rel = clean_path.lstrip('/')

        # Check directly in LOCAL_DIR
        target = LOCAL_DIR / rel
        if target.is_file(): return target

        # Check prefix stripped: /b/8b0b5899ed/...
        if rel.startswith('b/8b0b5899ed/'):
            sub = rel[len('b/8b0b5899ed/'):]
            target = LOCAL_DIR / sub
            if target.is_file(): return target

        # Check MIRROR_ROOT
        target = MIRROR_ROOT / rel
        if target.is_file(): return target

        # Check CACHE_DIR
        target = CACHE_DIR / rel
        if target.is_file(): return target

        return None

    def do_HEAD(self):
        url = urlsplit(self.path)
        local = self.find_local_file(url.path)
        if local:
            self.serve_local(local, head_only=True)
        else:
            self.proxy_request(head_only=True)

    def do_GET(self):
        url = urlsplit(self.path)
        local = self.find_local_file(url.path)
        if local:
            self.serve_local(local, head_only=False)
        else:
            self.proxy_request(head_only=False)

    def serve_local(self, path: Path, head_only: bool = False):
        size = path.stat().st_size
        range_hdr = self.headers.get('Range')
        content_type = self.guess_type(str(path)) or 'application/octet-stream'

        if not range_hdr:
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(size))
            self.end_headers()
            if not head_only:
                with path.open('rb') as f:
                    shutil.copyfileobj(f, self.wfile, length=1024 * 1024)
            return

        match = re.fullmatch(r'bytes=(\d*)-(\d*)', range_hdr)
        if not match or not any(match.groups()):
            self.send_error(416)
            return

        start = int(match[1]) if match[1] else max(0, size - int(match[2]))
        end = min(size - 1, int(match[2])) if match[1] and match[2] else size - 1
        if start >= size or end < start:
            self.send_response(416)
            self.send_header('Content-Range', f'bytes */{size}')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return

        self.send_response(206)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(end - start + 1))
        self.end_headers()

        if not head_only:
            with path.open('rb') as f:
                f.seek(start)
                remaining = end - start + 1
                while remaining > 0:
                    chunk = f.read(min(1024 * 1024, remaining))
                    if not chunk: break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)

    def proxy_request(self, head_only: bool = False):
        remote_url = UPSTREAM + self.path
        req = urllib.request.Request(remote_url, method='HEAD' if head_only else 'GET')

        for h in ('Range', 'Accept', 'Accept-Encoding', 'User-Agent'):
            if h in self.headers:
                req.add_header(h, self.headers[h])
        req.add_header('Host', 'gta.deloskiyt.pl')
        req.add_header('Referer', 'https://gta.deloskiyt.pl/')

        try:
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=60) as resp:
                self.send_response(resp.status)
                for k, v in resp.getheaders():
                    if k.lower() in ('transfer-encoding', 'connection', 'access-control-allow-origin',
                                     'cross-origin-opener-policy', 'cross-origin-embedder-policy',
                                     'cross-origin-resource-policy'):
                        continue
                    self.send_header(k, v)
                self.end_headers()

                if not head_only:
                    shutil.copyfileobj(resp, self.wfile, length=1024 * 1024)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            for k, v in e.headers.items():
                if k.lower() in ('transfer-encoding', 'connection', 'access-control-allow-origin',
                                 'cross-origin-opener-policy', 'cross-origin-embedder-policy',
                                 'cross-origin-resource-policy'):
                    continue
                self.send_header(k, v)
            self.end_headers()
            if not head_only:
                self.wfile.write(e.read())
        except Exception as exc:
            self.send_error(502, f"Proxy error: {exc}")

    def do_POST(self):
        length = int(self.headers.get('Content-Length', '0'))
        body = self.rfile.read(length) if length > 0 else b''

        remote_url = UPSTREAM + self.path
        req = urllib.request.Request(remote_url, data=body, method='POST')
        for h, v in self.headers.items():
            if h.lower() not in ('host', 'content-length', 'connection'):
                req.add_header(h, v)
        req.add_header('Host', 'gta.deloskiyt.pl')
        req.add_header('Referer', 'https://gta.deloskiyt.pl/')

        try:
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=60) as resp:
                self.send_response(resp.status)
                for k, v in resp.getheaders():
                    if k.lower() in ('transfer-encoding', 'connection', 'access-control-allow-origin',
                                     'cross-origin-opener-policy', 'cross-origin-embedder-policy',
                                     'cross-origin-resource-policy'):
                        continue
                    self.send_header(k, v)
                self.end_headers()
                shutil.copyfileobj(resp, self.wfile, length=1024 * 1024)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            for k, v in e.headers.items():
                if k.lower() in ('transfer-encoding', 'connection', 'access-control-allow-origin',
                                 'cross-origin-opener-policy', 'cross-origin-embedder-policy',
                                 'cross-origin-resource-policy'):
                    continue
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as exc:
            self.send_error(502, f"Proxy POST error: {exc}")

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--port', type=int, default=8000)
    args.add_argument('--open', action='store_true', help='open the default browser after binding')
    options = args.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', options.port), HybridHandler)
    address = 'http://localhost:%d/' % server.server_port
    print('Servidor GTA V Web iniciado em: %s' % address, flush=True)
    print('Pressione Ctrl+C para parar o servidor.', flush=True)
    if options.open:
        webbrowser.open(address)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
