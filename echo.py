from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import base64

PORT = 8000

class TerminalEchoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve the HTML form (text + file upload)."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8"/>
            <title>Terminal Echo</title>
            <style>
                body {{ font-family: sans-serif; padding: 20px; text-align: center; }}
                textarea {{ width: 80%; height: 150px; padding: 10px; font-size: 14px; }}
                .box {{ width: 80%; margin: 0 auto; text-align: left; }}
                button {{ padding: 10px 20px; font-size: 16px; margin-top: 10px; cursor: pointer; }}
                input[type=file] {{ margin-top: 10px; }}
                small {{ color: #666; }}
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
        """Handle multipart form (text + optional file) and save file to CWD."""
        import os
        import cgi

        ctype, _ = cgi.parse_header(self.headers.get("content-type", ""))

        if ctype != "multipart/form-data":
            self.send_response(400)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Expected multipart/form-data.\n")
            return

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": self.headers.get("Content-Type"),
            },
        )

        received_text = form.getfirst("text_data", "").strip()

        file_item = form["upload_file"] if "upload_file" in form else None
        saved_path = None
        file_size = None

        if file_item is not None and getattr(file_item, "filename", None):
            filename = os.path.basename(file_item.filename)
            saved_path = os.path.abspath(filename)

            with open(filename, "wb") as f:
                data = file_item.file.read()
                f.write(data)
                file_size = len(data)

        # OUTPUT TO TERMINAL
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
