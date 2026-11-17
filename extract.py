import os
import struct

MAGIC = b"\x56\x34\x12\xfa"
HEADERS = (b"FWS", b"CWS", b"ZWS")


def get_projector(path):
    size = os.path.getsize(path)
    if size < 16:
        return None
    with open(path, "rb") as f:
        f.seek(-min(size, 65536), os.SEEK_END)
        tail = f.read()
        pos = tail.rfind(MAGIC)
        if pos == -1 or pos + 8 > len(tail):
            return None
        swf_size = struct.unpack("<I", tail[pos + 4 : pos + 8])[0]
        start = size - len(tail) + pos - swf_size
        if start < 0:
            return None
        f.seek(start)
        head = f.read(4)
        if len(head) == 4 and head[:3] in HEADERS:
            return (path, start, swf_size, head[3])
    return None


items = [p for f in os.listdir(".") if f.lower().endswith(".exe") and (p := get_projector(f))]

if not items:
    print("No Flash projectors found.")
    raise SystemExit

for i, (name, _, sz, ver) in enumerate(items, 1):
    print(f"[{i}] {name} (Flash {ver}, {sz // 1024} KB)")

sel = input("Extract (e.g. 1,2 or all): ").strip().lower()
chosen = items if sel == "all" else [items[int(x) - 1] for x in sel.split(",") if x.strip().isdigit() and 0 < int(x) <= len(items)]

for name, start, sz, _ in chosen:
    out = os.path.splitext(name)[0] + ".swf"
    with open(name, "rb") as src, open(out, "wb") as dst:
        src.seek(start)
        dst.write(src.read(sz))
    print(f"Saved: {out}")
