from http.server import BaseHTTPRequestHandler, HTTPServer
import os

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
    # Split on boundary; first part is preamble, last is epilogue
    parts = body.split(delimiter)

    for part in parts:
        part = part.strip()
        if not part or part == b"--":
            continue

        # Each part: headers \r\n\r\n content \r\n
        header_end = part.find(b"\r\n\r\n")
        if header_end == -1:
            continue

        header_blob = part[:header_end].decode("utf-8", "replace")
        content = part[header_end + 4:]

        # Strip trailing CRLF that often precedes next boundary
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
            # Text fields are typically UTF-8; fall back gracefully
            fields[name] = content.decode("utf-8", "replace")

    return fields, files


class TerminalEchoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8"/>
            <title>Terminal Echo</title>
            <style>
                body { font-family: sans-serif; padding: 20px; text-align: center; }
                textarea { width: 80%; height: 150px; padding: 10px; font-size: 14px; }
                .box { width: 80%; margin: 0 auto; text-align: left; }
                button { padding: 10px 20px; font-size: 16px; margin-top: 10px; cursor: pointer; }
                input[type=file] { margin-top: 10px; }
                small { color: #666; }
            </style>
        </head>
        <body>
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
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        ct = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in ct or "boundary=" not in ct:
            self.send_response(400)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Expected multipart/form-data with boundary.\n")
            return

        # Extract boundary
        boundary = ct.split("boundary=", 1)[1].strip()
        if boundary.startswith('"') and boundary.endswith('"'):
            boundary = boundary[1:-1]
        boundary_b = boundary.encode("utf-8")

        # Read body
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0

        if length <= 0:
            self.send_response(400)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Missing or invalid Content-Length.\n")
            return

        body = self.rfile.read(length)
        fields, files = parse_multipart(body, boundary_b)

        received_text = (fields.get("text_data") or "").strip()

        saved_path = None
        file_size = None
        filename = None

        # Save uploaded file to current directory (CWD)
        up = files.get("upload_file")
        if up and up.get("filename"):
            filename = os.path.basename(up["filename"])  # prevent path tricks
            data = up.get("content", b"")

            # Avoid overwriting silently: if exists, add suffix
            base, ext = os.path.splitext(filename)
            candidate = filename
            i = 1
            while os.path.exists(candidate):
                candidate = f"{base} ({i}){ext}"
                i += 1
            filename = candidate

            with open(filename, "wb") as f:
                f.write(data)

            saved_path = os.path.abspath(filename)
            file_size = len(data)

        # TERMINAL OUTPUT
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

        # Browser response
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"<h2>Sent! File saved to current directory.</h2><a href='/'>Send more</a>"
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
