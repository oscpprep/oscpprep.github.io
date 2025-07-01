#!/usr/bin/env python3
import argparse
import os
import requests
import sys

# Default headers mirroring the Android Drive client
DEFAULT_HEADERS = {
    "Icy-Metadata":         "1",
    "User-Agent":           "com.google.android.apps.docs/2.25.050.0.all.alldpi "
                            "(Linux;Android 7.1.2) AndroidXMedia3/1.6.0-alpha02",
    "Accept-Encoding":      "gzip, deflate, br",
    "Priority":             "u=1, i",
}

def sanitize_headers(headers: dict) -> dict:
    """
    Ensures all header values are pure Latin-1 (dropping any out-of-range chars).
    """
    clean = {}
    for k, v in headers.items():
        clean[k] = v.encode("latin-1", "ignore").decode("latin-1")
    return clean

def get_remote_size(url: str, headers: dict) -> int:
    """
    Issues a tiny ranged request (bytes=0-0) to learn the full resource size.
    """
    probe = headers.copy()
    probe["Range"] = "bytes=0-0"
    r = requests.get(url, headers=probe, stream=True)
    r.raise_for_status()
    # Content-Range: bytes 0-0/12345678
    cr = r.headers.get("Content-Range", "")
    try:
        return int(cr.split("/")[-1])
    except:
        return int(r.headers.get("Content-Length", 0))

def download_in_ranges(url: str, headers: dict, size: int,
                       out_path: str, chunk_size: int = 1<<20):
    """
    Streams the file in byte ranges of chunk_size, writing to out_path.
    """
    with open(out_path, "wb") as f:
        for start in range(0, size, chunk_size):
            end = min(size - 1, start + chunk_size - 1)
            h = headers.copy()
            h["Range"] = f"bytes={start}-{end}"
            r = requests.get(url, headers=h)
            try:
                r.raise_for_status()
            except Exception as e:
                print(f"ERROR: bytes={start}-{end} → {e}", file=sys.stderr)
                sys.exit(1)
            f.write(r.content)
            print(f"Wrote bytes {start}-{end}")
    print("✅ Download complete.")

def main():
    p = argparse.ArgumentParser(
        description="Download a restricted Drive media stream via its presigned token"
    )
    p.add_argument("--fileid", required=True,
                   help="Drive file ID (the long …files/<ID>?alt=media path segment)")
    p.add_argument("--auth", required=True,
                   help="Exact OAuth token (no wrapping “…”). E.g. ya29.m.CqwCA…")
    p.add_argument("-o", "--output",
                   help="Output filename (defaults to FILEID.mp3)")
    p.add_argument("--chunk", type=int, default=1<<20,
                   help="Chunk size in bytes (default 1 MiB)")

    args = p.parse_args()

    base_url = (
        "https://www.googleapis.com/download/drive/v2internal/"
        f"files/{args.fileid}?alt=media"
    )
    headers = DEFAULT_HEADERS.copy()
    headers["Authorization"] = f"OAuth {args.auth}"
    headers = sanitize_headers(headers)

    out_path = args.output or f"{args.fileid}.mp3"
    print(f"→ URL:     {base_url}")
    print(f"→ Output:  {out_path}")
    print(f"→ Headers:")
    for k,v in headers.items():
        print(f"    {k}: {v}")
    print()

    # determine remote file size
    size = get_remote_size(base_url, headers)
    print(f"→ Remote size: {size} bytes\n")

    download_in_ranges(base_url, headers, size, out_path, args.chunk)

if __name__ == "__main__":
    main()
