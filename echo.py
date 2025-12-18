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
