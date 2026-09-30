#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公众号文章排版验证器 —— 封面标题换行 + 整篇溢出

为什么需要它：
  封面卡标题用 <br> 手动分行。但 <br> 只保证「几行之间断」，
  不保证「每行放得下」。写长了，客户端会在小屏上再折一次，
  行数翻倍。这个问题在桌面预览里完全看不出来，只有量文字真实宽度才发现。

  可用宽度**从 HTML 里读**（封面卡自身的 margin / padding），不写死——
  否则一旦调了内边距，脚本就会给出假数字，说谎的检查器比没有更糟。

用法：
  python3 verify-layout.py <文章.html>
  python3 verify-layout.py <文章.html> --widths 320,360,375,414

输出：
  1) 封面逐行宽度、各屏宽下的余量与行数（标题必须单行，副标题最多两行）
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

PROBE_WIDTH = 375  # 溢出检测用的容器宽度


def find_chrome() -> str:
    for p in CHROME_CANDIDATES:
        if pathlib.Path(p).exists():
            return p
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    sys.exit("找不到 Chrome / Chromium。请安装 Chrome，或用 --chrome 指定路径。")


# ---------------------------------------------------------------- 样式解析

def shorthand(style: str, prop: str, default=(0.0, 0.0, 0.0, 0.0)):
    """解析 margin / padding 简写，返回 (上, 右, 下, 左)。解析不出来就用默认值。"""
    m = re.search(rf"(?<![a-z-]){prop}\s*:\s*([^;\"]+)", style)
    if not m:
        return default
    parts = [p.strip() for p in m.group(1).split() if p.strip()]
    vals = []
    for p in parts:
        mm = re.fullmatch(r"(-?[0-9.]+)px", p)
        if not mm:
            return default
        vals.append(float(mm.group(1)))
    if len(vals) == 1:
        return (vals[0],) * 4
    if len(vals) == 2:
        return (vals[0], vals[1], vals[0], vals[1])
    if len(vals) == 3:
        return (vals[0], vals[1], vals[2], vals[1])
    if len(vals) >= 4:
        return tuple(vals[:4])
    return default


def px_prop(style: str, prop: str, default=0.0) -> float:
    m = re.search(rf"(?<![a-z-]){prop}\s*:\s*(-?[0-9.]+)px", style)
    return float(m.group(1)) if m else default


def enclosing_section_style(html: str, pos: int) -> str:
    """返回 pos 位置最内层包裹的 <section> 的 style。"""
    stack = []
    for m in re.finditer(r"<(/?)(section|p)\b([^>]*?)(/?)>", html[:pos]):
        closing, tag = m.group(1), m.group(2)
        if closing:
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == tag:
                    del stack[i:]
                    break
        else:
            stack.append((tag, m.group(3) or ""))
    for tag, attrs in reversed(stack):
        if tag == "section":
            return attrs
    return ""


def strip_comments(html: str) -> str:
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def paras(html: str):
    return [
        {"style": m.group(1) or "", "inner": m.group(2), "start": m.start()}
        for m in re.finditer(r"<p\b([^>]*)>(.*?)</p>", html, re.S)
    ]


def style_px(style: str, prop: str, default: float) -> float:
    return px_prop(style, prop, default)


def segments(inner: str):
    out = []
    for part in re.split(r"<br\s*/?>", inner, flags=re.I):
        text = re.sub(r"<[^>]+>", "", part)
        text = (text.replace("&nbsp;", " ").replace("&amp;", "&")
                    .replace("&lt;", "<").replace("&gt;", ">").strip())
        if text:
            out.append(text)
    return out


# ---------------------------------------------------------------- 渲染探针

def build_probe(article: str, lines: list) -> str:
    items = []
    for i, (text, size, _kind) in enumerate(lines):
        style = (f"font-size:{size:g}px;line-height:1.6;font-weight:700;"
                 "margin:0;white-space:nowrap;display:inline-block;")
        items.append(f'<div id="L{i}" style="{style}">{text}</div><br>')
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
    return ('<!DOCTYPE html><html><head><meta charset="utf-8"></head>'
            f'<body style="margin:0"><div id="phone" style="width:{PROBE_WIDTH}px">{article}</div>'
            f'{"".join(items)}{probe}</body></html>')


def run_chrome(chrome: str, page_path: str) -> dict:
    out = subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-sandbox",
         "--window-size=1200,1600", "--virtual-time-budget=4000",
         "--dump-dom", f"file://{page_path}"],
        capture_output=True, text=True, timeout=180,
    ).stdout
    m = re.search(r"<title>PROBE::(.*?)</title>", out, re.S)
    if not m:
        sys.exit("探针未返回结果。检查文章 HTML 是否可解析，或换一个 Chrome。")
    raw = m.group(1)
    for a, b in (("&quot;", '"'), ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">")):
        raw = raw.replace(a, b)
    return json.loads(raw)


# ---------------------------------------------------------------- 主流程

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("article")
    ap.add_argument("--widths", default="320,360,375,414")
    ap.add_argument("--chrome", default=None)
    args = ap.parse_args()

    chrome = args.chrome or find_chrome()
    widths = [int(x) for x in args.widths.split(",") if x.strip()]
    raw_html = pathlib.Path(args.article).read_text(encoding="utf-8")
    html = strip_comments(raw_html)

    all_p = paras(html)
    title_idx = next((i for i, p in enumerate(all_p) if "<br" in p["inner"]), None)

    lines, geo = [], {}
    if title_idx is not None:
        t = all_p[title_idx]
        card_style = enclosing_section_style(html, t["start"])
        m = shorthand(card_style, "margin", (0.0, 0.0, 0.0, 0.0))
        p = shorthand(card_style, "padding", (0.0, 0.0, 0.0, 0.0))
        geo = {"title": m[1] + m[3] + p[1] + p[3]}
        for text in segments(t["inner"]):
            lines.append((text, style_px(t["style"], "font-size", 20), "标题"))
        if title_idx + 1 < len(all_p):
            s = all_p[title_idx + 1]
            extra = (px_prop(s["style"], "padding-left", 0.0)
                     + px_prop(s["style"], "border-left-width", 0.0))
            if "border-left" in s["style"]:
                bm = re.search(r"border-left\s*:\s*([0-9.]+)px", s["style"])
                extra = px_prop(s["style"], "padding-left", 0.0) + (float(bm.group(1)) if bm else 0.0)
            geo["subtitle"] = geo["title"] + extra
            for text in segments(s["inner"]):
                lines.append((text, style_px(s["style"], "font-size", 13), "副标题"))

    with tempfile.TemporaryDirectory() as td:
        page = pathlib.Path(td) / "probe.html"
        page.write_text(build_probe(html, lines), encoding="utf-8")
        res = run_chrome(chrome, str(page))

    budget = {(w, k): w - geo.get("title" if k == "标题" else "subtitle", 0)
              for w in widths for k in ("标题", "副标题")}

    print(f"文章：{args.article}")
    print(f"屏宽档：{', '.join(str(w) + 'px' for w in widths)}")
    print(f"可用宽（从封面卡样式读出）：横向 margin+padding = {geo.get('title', 0):g}px"
          f"；副标题再扣 {geo.get('subtitle', 0) - geo.get('title', 0):g}px")
    print()
    print(f"一、封面逐行宽度（基准屏宽 {min(widths)}px；标题须单行，副标题至多两行）")

    if not lines:
        print("  （没找到带 <br> 的标题段，跳过）")
    else:
        for i, (text, size, kind) in enumerate(lines):
            measured = res["widths"].get(f"L{i}")
            if measured is None:
                continue
            cells, counts = [], []
            for w in widths:
                b = budget[(w, kind)]
                cells.append(f"{b - measured:>7}")
                counts.append(f"{(measured + b - 1) // b:>7}")
            w0 = min(widths)
            b0 = budget[(w0, kind)]
            limit = 1 if kind == "标题" else 2
            n0 = (measured + b0 - 1) // b0
            if n0 <= limit:
                flag = "✓" if b0 - measured >= 15 else "△ 偏紧"
            else:
                flag = f"✗ {w0}px 下会占 {n0} 行（上限 {limit} 行）"
            print(f"  [{kind}] {text}")
            print(f"         实际宽 {measured}px（字号 {size:g}px）")
            print(f"         {'余量':<8}| " + "".join(f"{str(w) + 'px':>9}" for w in widths))
            print(f"         {'':<8}| " + "".join(f"{c:>9}" for c in cells))
            print(f"         {'行数':<8}| " + "".join(f"{c:>9}" for c in counts) + f"   {flag}")
        print()
        print("  粗算口诀：中文 ≈ 每字 1 个字号，拉丁字符（AI / TA）≈ 每个 1.2 个字号，全角标点同中文。")

    print()
    print(f"二、整篇溢出检测（{PROBE_WIDTH}px 容器，scrollWidth 应不超过 clientWidth）")
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
