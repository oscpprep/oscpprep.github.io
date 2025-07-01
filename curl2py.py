#!/usr/bin/env python3
import argparse, shlex, os
import requests

def parse_curl(curl_cmd: str):
    """
    Very basic curl parser: pulls out -X, -H headers and the URL.
    """
    tokens = shlex.split(curl_cmd)
    method = "get"
    url    = ""
    headers = {}
    it = iter(tokens)
    for tk in it:
        if tk in ("-X", "--request"):
            method = next(it).strip().lower()
        elif tk in ("-H", "--header"):
            h = next(it)
            if ":" in h:
                k,v = h.split(":",1)
                headers[k.strip()] = v.strip()
        # assume the last token starting with http is our URL
        elif tk.startswith("http://") or tk.startswith("https://"):
            url = tk
    return method, url, headers

def main():
    p = argparse.ArgumentParser(
        description="Paste a curl GET (with -H headers) → Python requests downloader"
    )
    p.add_argument(
        "--curl", required=True,
        help="Your full curl command in quotes"
    )
    p.add_argument(
        "-o","--output", help="Write to this filename (else basename of URL)"
    )
    args = p.parse_args()

    method, url, headers = parse_curl(args.curl)
    if not url:
        print("❌ Failed to find URL in your curl command."); return

    out = args.output or os.path.basename(url.split("?",1)[0]) or "output.bin"
    print(f"→ METHOD: {method.upper()}")
    print(f"→ URL:    {url}")
    print(f"→ HEADERS:")
    for k,v in headers.items():
        print(f"    {k}: {v}")
    print(f"→ SAVING TO: {out}\n")
    # sanitize headers for Latin-1
    for k, v in headers.items():
        headers[k] = v.encode("latin-1", "ignore").decode("latin-1")
    resp = requests.request(method, url, headers=headers, stream=True)
    try:
        resp.raise_for_status()
    except Exception as e:
        print("❌ HTTP error:", e)
        print("Response headers:", resp.headers)
        return

    total = resp.headers.get("Content-Length","unknown")
    print(f"Downloading {total} bytes…")
    with open(out, "wb") as f:
        for chunk in resp.iter_content(1024*1024):
            if chunk:
                f.write(chunk)
    print("✅ Download complete.")

if __name__=="__main__":
    main()
