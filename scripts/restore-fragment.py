#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把被「预览器」污染的文章还原成可直接粘贴的公众号纯片段。

背景：用内置预览面板预览公众号文章时，预览服务会把源文件改成一个完整 HTML 文档——
  1) 套上 <!DOCTYPE><html><head><style>…</style></head><body …>…</body></html>
  2) 给每个标签塞 data-page-node-id="xxx"、data-sp-bindable="database" 之类的属性
  3) 把 img src 里的 & 转义成 &amp;
这三点对普通网页无害，但对公众号是致命的：
  - 公众号文章必须是**纯片段**（直接从 <section> 开始），带 <html><head> 会被判为整页、
    粘贴时样式全丢；
  - &amp; 若不被解码，图片地址会真的带着 &amp; 发出去 → 图裂。

本脚本做三件事：切回 <section>…</section> 片段 → 剥掉 data-* 属性 → 把 &amp; 还原成 &。

用法：
    python3 scripts/restore-fragment.py <文章>            # 原地修复
    python3 scripts/restore-fragment.py <文章> --dry-run  # 只看诊断，不写文件

退出码：0 = 干净或已修复；1 = 找不到可还原的片段。依赖：无（纯标准库）。
"""

import argparse
import pathlib
import re
import sys

# 预览服务注入的属性：data-page-node-id / data-sp-bindable / data-dm-* 等
DATA_ATTR = re.compile(r'\s+data-[a-z0-9-]+="[^"]*"', re.I)
ENTITIES = [("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&#39;", "'")]


def diagnose(text: str):
    """返回污染项列表（空列表＝干净）。"""
    issues = []
    if re.search(r'<!DOCTYPE|<html[ >]|<head[ >]|<body[ >]|<style[ >]', text, re.I):
        issues.append("被套上了完整 HTML 外壳（<!DOCTYPE>/<html>/<head>/<body>/<style>）")
    n = len(DATA_ATTR.findall(text))
    if n:
        issues.append(f"注入了 {n} 个 data-* 属性（data-page-node-id 等）")
    for ent, _ in ENTITIES:
        c = text.count(ent)
        if c:
            issues.append(f"HTML 实体未还原：{ent} × {c}")
    return issues


def restore(text: str) -> str:
    """还原成纯片段。已经是片段就不动内容，只做属性与实体的清理。"""
    if re.search(r'<html[ >]|<body[ >]', text, re.I):
        i = text.find("<section")
        j = text.rfind("</section>")
        if i < 0 or j < 0:
            raise SystemExit("✗ 找不到 <section>…</section>，无法还原")
        text = text[i:j + len("</section>")]
    text = DATA_ATTR.sub("", text)
    # 预览服务可能反复转义（& → &amp; → &amp;amp;），所以要循环到收敛
    for _ in range(5):
        before = text
        for ent, ch in ENTITIES:
            text = text.replace(ent, ch)
        if text == before:
            break
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("article")
    ap.add_argument("--dry-run", action="store_true", help="只诊断，不写文件")
    args = ap.parse_args()

    path = pathlib.Path(args.article)
    text = path.read_text(encoding="utf-8")
    issues = diagnose(text)

    print(f"文件：{path}")
    if not issues:
        print("✓ 未发现预览污染，无需还原")
        return 0

    print(f"✗ 发现 {len(issues)} 项污染：")
    for s in issues:
        print(f"    · {s}")

    if args.dry_run:
        print("\n（--dry-run：未修改文件）")
        return 0

    fixed = restore(text)
    path.write_text(fixed, encoding="utf-8")
    print(f"\n已还原：{len(text)} → {len(fixed)} 字符")
    left = diagnose(fixed)
    print("✓ 干净" if not left else "⚠️ 仍有残留：" + "；".join(left))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
