#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公众号文章排版验证器 —— 封面标题换行 + 整篇溢出

为什么需要它：
  封面卡标题用 <br> 手动分成两行。但 <br> 只保证「两行之间断」，
  不保证「每行放得下」。写长了，客户端会在小屏上再折一次，
  两行变四行。这个问题在桌面预览里完全看不出来，只有量文字真实宽度才发现。

用法：
  python3 verify-layout.py <文章.html>
  python3 verify-layout.py <文章.html> --widths 320,360,375,414

输出：
  1) 封面标题 / 副标题逐行宽度，以及各屏宽下的余量（负数为放不下）
  2) 整篇在 375px 容器内的溢出元素（应为 0）

依赖：本机 Chrome（headless）。不需要第三方 Python 包。
"""

import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]


def find_chrome() -> str:
    for p in CHROME_CANDIDATES:
        if pathlib.Path(p).exists():
            return p
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    sys.exit("找不到 Chrome / Chromium。请安装 Chrome，或用 --chrome 指定路径。")


def paras(html: str) -> list:
    """按出现顺序取出所有 <p ...>...</p>，含 style 与内部 HTML。"""
    return [
        {"style": m.group(1) or "", "inner": m.group(2)}
        for m in re.finditer(r"<p\b([^>]*)>(.*?)</p>", html, re.S)
    ]


def style_px(style: str, prop: str, default: float) -> float:
    m = re.search(rf"{prop}\s*:\s*([0-9.]+)px", style)
    return float(m.group(1)) if m else default


def segments(inner: str) -> list:
    """把一段 HTML 按 <br> 拆成多行；去标签、还原实体，只留纯文本。"""
    out = []
    for part in re.split(r"<br\s*/?>", inner, flags=re.I):
        text = re.sub(r"<[^>]+>", "", part)
        text = (
            text.replace("&nbsp;", " ")
            .replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .strip()
        )
        if text:
            out.append(text)
    return out


def build_probe(article: str, lines: list, widths: list) -> str:
    """构造探针页：nowrap 量行宽 + 固定宽容器做溢出检测。"""
    items = []
    for i, (text, size, _kind) in enumerate(lines):
        style = (
            f"font-size:{size:g}px;line-height:1.5;font-weight:700;"
            "margin:0;white-space:nowrap;display:inline-block;"
        )
        items.append(f'<div id="L{i}" style="{style}">{text}</div><br>')

    phone = f'<div id="phone" style="width:375px">{article}</div>'

    probe = """
<script>
window.addEventListener('load', function(){
  var lineWidths = {};
  document.querySelectorAll('div[id^="L"]').forEach(function(d){
    lineWidths[d.id] = Math.ceil(d.getBoundingClientRect().width);
  });
  var over = [];
  var box = document.getElementById('phone');
  box.querySelectorAll('p,section').forEach(function(el){
    if (el.clientWidth > 0 && el.scrollWidth > el.clientWidth + 1) {
      over.push(el.tagName + ' ' + Math.round(el.clientWidth) + '->' + el.scrollWidth
        + ' | ' + (el.textContent || '').replace(/\\s+/g, '').slice(0, 20));
    }
  });
  document.title = 'PROBE::' + JSON.stringify({widths: lineWidths, overflow: over.slice(0, 8)});
});
</script>
"""
    return (
        '<!DOCTYPE html><html><head><meta charset="utf-8"></head>'
        f'<body style="margin:0">{phone}{"".join(items)}{probe}</body></html>'
    )


def run_chrome(chrome: str, page_path: str) -> dict:
    out = subprocess.run(
        [
            chrome, "--headless", "--disable-gpu", "--no-sandbox",
            "--window-size=1200,1600", "--virtual-time-budget=4000",
            "--dump-dom", f"file://{page_path}",
        ],
        capture_output=True, text=True, timeout=180,
    ).stdout
    m = re.search(r"<title>PROBE::(.*?)</title>", out, re.S)
    if not m:
        sys.exit("探针未返回结果。检查文章 HTML 是否可解析，或换一个 Chrome。")
    raw = m.group(1)
    for a, b in (("&quot;", '"'), ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">")):
        raw = raw.replace(a, b)
    return json.loads(raw)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("article")
    ap.add_argument("--widths", default="320,360,375,414")
    ap.add_argument("--chrome", default=None)
    args = ap.parse_args()

    chrome = args.chrome or find_chrome()
    widths = [int(x) for x in args.widths.split(",") if x.strip()]
    html = pathlib.Path(args.article).read_text(encoding="utf-8")

    # 封面标题 = 第一个含 <br> 的 <p>；副标题 = 紧跟其后的那个 <p>
    all_p = paras(html)
    title_idx = next((i for i, p in enumerate(all_p) if "<br" in p["inner"]), None)

    lines = []  # (文本, 字号, 标签)
    if title_idx is not None:
        t = all_p[title_idx]
        for text in segments(t["inner"]):
            lines.append((text, style_px(t["style"], "font-size", 20), "标题"))
        if title_idx + 1 < len(all_p):
            s = all_p[title_idx + 1]
            for text in segments(s["inner"]):
                lines.append((text, style_px(s["style"], "font-size", 13), "副标题"))

    # 各屏宽下的可用文字宽度
    budget = {(w, kind): w - (90 if kind == "标题" else 102)
              for w in widths for kind in ("标题", "副标题")}

    with tempfile.TemporaryDirectory() as td:
        page = pathlib.Path(td) / "probe.html"
        page.write_text(build_probe(html, lines, widths), encoding="utf-8")
        res = run_chrome(chrome, str(page))

    print(f"文章：{args.article}")
    print(f"屏宽档：{', '.join(str(w) + 'px' for w in widths)}")
    print()
    print("一、封面逐行宽度（可用宽 = 屏宽 − 40 卡片外边距 − 50 卡片内边距；副标题再减 12 padding-left）")

    if not lines:
        print("  （没找到带 <br> 的标题段，跳过）")
    else:
        for i, (text, size, kind) in enumerate(lines):
            measured = res["widths"].get(f"L{i}")
            if measured is None:
                continue
            # 屏宽下的余量（正数=放得下）；标题必须单行，副标题最多折成两行
            cells, counts = [], []
            for w in widths:
                b = budget[(w, kind)]
                cells.append(f"{b - measured:>7}")
                counts.append(f"{(measured + b - 1) // b:>7}")
            w0 = min(widths)
            head0 = budget[(w0, kind)] - measured
            limit = 1 if kind == "标题" else 2
            lines0 = (measured + budget[(w0, kind)] - 1) // budget[(w0, kind)]
            if lines0 <= limit:
                flag = "✓" if head0 >= 15 else "△ 偏紧"
            else:
                flag = f"✗ {w0}px 下会占 {lines0} 行（上限 {limit} 行）"
            print(f"  [{kind}] {text}")
            print(f"         实际宽 {measured}px")
            print(f"         {'余量':<8}| " + "".join(f"{str(w) + 'px':>9}" for w in widths))
            print(f"         {'':<8}| " + "".join(f"{c:>9}" for c in cells))
            print(f"         {'行数':<8}| " + "".join(f"{c:>9}" for c in counts) + f"   {flag}")
        print()
        print("  判据：以最小屏宽为基准。标题必须单行（余量 ≥15px），副标题最多折成两行。")
        print("        中文 20px ≈ 每字 20px，拉丁字符（AI、CT 等）≈ 每个 24px，可先粗筛再实测。")

    print()
    print("二、整篇溢出检测（375px 容器，scrollWidth 应不超过 clientWidth）")
    if res["overflow"]:
        for item in res["overflow"]:
            print("  ✗", item)
        print(f"  共 {len(res['overflow'])} 处溢出")
    else:
        print("  ✓ 无溢出")

    w0 = min(widths)
    ok = (not res["overflow"]) and all(
        res["widths"].get(f"L{i}", 0) <= budget[(w0, kind)] * (1 if kind == "标题" else 2)
        for i, (_, _, kind) in enumerate(lines)
    )
    print()
    print("结果：" + ("通过" if ok else "有问题，见上"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
