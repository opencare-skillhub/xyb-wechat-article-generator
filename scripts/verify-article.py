#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公众号文章格式验证器 —— 一次跑完发布前的全部格式检查

检查项（顺序即报告顺序）：
  1. 禁用标签/属性：div / table / style / html / head / body / script / svg / ul / li / class
  2. 标签配平（**先剥掉 HTML 注释**——注释里写字面标签会被朴素正则在误判）
  3. 裸 URL（必须包在 a 标签里）
  4. foot 逐字比对：母版里的每段文案都应出现在文章里
     （允许替换的只有「参考文献：请在此处列出引用来源」这类占位行）
  5. 母版里的图片 src 是否都在文章里
  6. 色值统计（人工核对用；可用 --require-color 强制要求某个色值必须出现）

用法：
  python3 verify-article.py output/xxx.html
  python3 verify-article.py output/xxx.html --foot assets/template4-ruici/med_foot_template.html
  python3 verify-article.py output/xxx.html --require-color "#403358" --require-color "#5c4a7a"

退出码非 0 即不通过。依赖：无（纯标准库）。
"""

import argparse
import pathlib
import re
import sys

# 允许替换的占位文案（母版里有、成文后应该没有）
REPLACEABLE = ("参考文献：请在此处列出引用来源",)

BANNED = [
    (r"<div[ >]", "<div>"),
    (r"<table[ >]", "<table>"),
    (r"<style[ >]", "<style>"),
    (r"<html", "<html>"),
    (r"<head", "<head>"),
    (r"<body", "<body>"),
    (r"<script", "<script>"),
    (r"<svg", "<svg>"),
    (r"<ul[ >]", "<ul>"),
    (r"<li[ >]", "<li>"),
    (r'class="', "class 属性"),
]

VOID = {"img", "br", "hr", "input", "meta", "link"}


def strip_comments(html: str) -> str:
    """剥掉 HTML 注释。标签配平必须在剥注释之后做，否则注释里写的
    字面标签（比如说明文字里的 <section>）会被算成未闭合。"""
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def para_texts(html: str):
    return [
        re.sub(r"\s+", "", m.group(1))
        for m in re.finditer(r"<p[^>]*>(.*?)</p>", html, re.S)
    ]


def check_banned(clean: str):
    hits = []
    for pat, name in BANNED:
        n = len(re.findall(pat, clean, re.I))
        if n:
            hits.append(f"{name} × {n}")
    return hits


def check_balance(clean: str):
    stack, extra = [], []
    for m in re.finditer(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*?)(/?)>", clean):
        closing, tag, _attrs, selfclose = (
            m.group(1), m.group(2).lower(), m.group(3), m.group(4),
        )
        if tag in VOID or selfclose:
            continue
        if closing:
            if stack and stack[-1] == tag:
                stack.pop()
            else:
                extra.append(tag)
        else:
            stack.append(tag)
    return stack, extra


def check_bare_urls(clean: str):
    body = re.sub(r"<a\b[^>]*>.*?</a>", "", clean, flags=re.S | re.I)
    body = re.sub(r'(?:src|href)="[^"]*"', "", body, flags=re.I)
    return re.findall(r"https?://[^\s\"'<>)]+", body)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("article")
    ap.add_argument("--foot", default=None, help="foot 母版路径，默认 template3")
    ap.add_argument("--require-color", action="append", default=[])
    ap.add_argument("--no-foot", action="store_true", help="跳过 foot 比对")
    args = ap.parse_args()

    skill_root = pathlib.Path(__file__).resolve().parent.parent
    foot_path = pathlib.Path(
        args.foot or skill_root / "assets/template3/foot_template.html"
    )
    art = pathlib.Path(args.article)
    html = art.read_text(encoding="utf-8")
    clean = strip_comments(html)
    ok = True

    print(f"文章：{art}")
    print()

    hits = check_banned(clean)
    print(f"1 禁用标签/属性：{'✓ 0 命中' if not hits else '✗ ' + '、'.join(hits)}")
    ok &= not hits

    stack, extra = check_balance(clean)
    good = not stack and not extra
    print(f"2 标签配平：{'✓' if good else f'✗ 未闭合 {stack} 多余闭合 {extra}'}")
    ok &= good

    bare = check_bare_urls(clean)
    print(f"3 裸 URL：{'✓ 无' if not bare else '✗ ' + str(bare[:3])}")
    ok &= not bare

    if not args.no_foot:
        if not foot_path.exists():
            print(f"4 foot 比对：⚠️ 找不到母版 {foot_path}，已跳过")
        else:
            mtext = foot_path.read_text(encoding="utf-8")
            have = set(para_texts(html))
            missing = [
                t for t in para_texts(mtext)
                if t and t not in have and not any(r in t for r in REPLACEABLE)
            ]
            print(f"4 foot 逐字比对（母版 {foot_path.name}）："
                  f"{'✓ 全部一致' if not missing else f'✗ 缺 {len(missing)} 段'}")
            for t in missing[:5]:
                print(f"     · {t[:60]}")
            ok &= not missing

            srcs = re.findall(r'<img[^>]+src="([^"]+)"', mtext)
            miss_img = [s for s in srcs if s not in html]
            print(f"5 foot 图片：{'✓ 齐备' if not miss_img else f'✗ 缺 {len(miss_img)} 张'}")
            for s in miss_img[:3]:
                print(f"     · {s[:70]}")
            ok &= not miss_img

    colors = re.findall(r"#[0-9A-Fa-f]{6}", html)
    norm = [c.lower() for c in colors]
    uniq = sorted(set(norm), key=lambda c: -norm.count(c))
    print(f"6 色值统计（共 {len(uniq)} 种，按出现次数）：")
    print("     " + "  ".join(f"{c}×{norm.count(c)}" for c in uniq[:10]))
    for want in args.require_color:
        found = want.lower() in uniq
        print(f"     必含 {want}：{'✓' if found else '✗ 未出现'}")
        ok &= found

    print()
    print(f"规模：{len(html)} 字符 / {len(html.splitlines())} 行")
    print("结果：" + ("全部通过" if ok else "有问题，见上"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
