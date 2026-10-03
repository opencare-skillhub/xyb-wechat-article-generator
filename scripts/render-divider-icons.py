#!/usr/bin/env python3
"""把 assets/icons/*.svg 渲染成 384px 透明底 PNG（分隔线图标池）。

用法：
    python scripts/render-divider-icons.py

产出：assets/icons/<id>-384.png（透明底，边长 384，内容居中留白）

原理：一次拼一张横向长图（每格 384×384 透明底）交给 headless Chrome 截图，
再按 alpha 通道裁到内容外框并补到正方形，只启动一次浏览器，快且不会漏。
"""
import os
import subprocess
import sys
import tempfile
from PIL import Image

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON_DIR = os.path.join(SKILL, "assets", "icons")
SIZE = 384
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def build_sheet(svgs):
    cells = "".join(
        '<div style="width:%dpx;height:%dpx;">%s</div>' % (SIZE, SIZE, s)
        for s in svgs
    )
    return (
        '<!doctype html><html><head><meta charset="utf-8"><style>'
        "html,body{margin:0;padding:0;background:transparent;}"
        "body{display:flex;}"
        "div{background:transparent;}"
        "svg{display:block;width:%dpx;height:%dpx;}"
        "</style></head><body>%s</body></html>" % (SIZE, SIZE, cells)
    )


def main():
    if not os.path.isdir(ICON_DIR):
        sys.exit("图标目录不存在：%s" % ICON_DIR)
    svgs = [
        os.path.join(ICON_DIR, f)
        for f in sorted(os.listdir(ICON_DIR))
        if f.endswith(".svg")
    ]
    if not svgs:
        sys.exit("目录里没有 svg")
    with open(svgs[0], encoding="utf-8") as fh:
        first = fh.read()
    with open(svgs[0], encoding="utf-8") as fh:
        pass
    html = build_sheet([open(p, encoding="utf-8").read() for p in svgs])
    tmpd = tempfile.mkdtemp(prefix="divider-icons-")
    html_path = os.path.join(tmpd, "sheet.html")
    shot_path = os.path.join(tmpd, "sheet.png")
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(html)
    cmd = [
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--force-device-scale-factor=1",
        "--default-background-color=00000000",
        "--window-size=%d,%d" % (SIZE * len(svgs), SIZE),
        "--screenshot=" + shot_path,
        "file://" + html_path,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(shot_path):
        sys.exit("Chrome 截图失败：\n%s\n%s" % (r.stdout, r.stderr))
    sheet = Image.open(shot_path).convert("RGBA")
    print("sheet", sheet.size)
    for i, svg in enumerate(svgs):
        tile = sheet.crop((i * SIZE, 0, (i + 1) * SIZE, SIZE))
        bbox = tile.split()[-1].getbbox()  # alpha 外框
        if not bbox:
            sys.exit("第 %d 格是空的：%s" % (i, svg))
        pad = 12
        x0 = max(0, bbox[0] - pad)
        y0 = max(0, bbox[1] - pad)
        x1 = min(SIZE, bbox[2] + pad)
        y1 = min(SIZE, bbox[3] + pad)
        content = tile.crop((x0, y0, x1, y1))
        square = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        square.paste(
            content,
            ((SIZE - content.width) // 2, (SIZE - content.height) // 2),
            content,
        )
        out = svg[:-4] + "-384.png"
        square.save(os.path.join(ICON_DIR, os.path.basename(out)))
        print("  ->", os.path.basename(out), "content", content.size)


if __name__ == "__main__":
    main()
