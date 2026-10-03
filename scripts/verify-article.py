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
  6. 防盗链属性：mmbiz.qpic.cn / pic.newrank.cn 的图必须带 referrerpolicy="no-referrer"
     （不带的话带 Referer 请求会被换成 140×140 占位图，http 预览就是「尾图丢了」）
  7. 图片 URL 可移植性：URL 路径里不能有 % 括号 空格 中文等字符
     （微信编辑器抓图时会二次编码，%20 变 %2520 → 图床 404 → 复制进编辑器图不显示）
  8. 预览污染：预览面板会把文章改成完整 HTML（套 <html>/<head>/<style>，塞
     data-page-node-id，把 img src 里的 & 转义成 &amp;）。这类污染对公众号是致命的，
     发现即报错并提示 `scripts/restore-fragment.py`
  9. foot 五件套结构：关于小胰宝深卡 → 尾图 → 关注我们 → 底部寄语（With love and hope
     落款）→ 免责声明，缺件或顺序颠倒都算不过。这一条**不依赖母版文件**，
     单独成项是因为它漏过 2-3 次（母版比对只能查到「母版里那段文字在不在」，
     查不到「整块 section 被删/被挪」）。
  10. 色值统计（人工核对用；可用 --require-color 强制要求某个色值必须出现）

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

# foot 五件套（template3 / ruici 母版的固定顺序，一套都不能少、顺序也不能颠倒）
# last=True 表示取「最后一次出现」的位置：正文里可能顺带提一句「关于小胰宝」，
# 但 footer 块一定在文末，取最后一次才不会被正文里的同名文字骗过去。
FOOT_PIECES = (
    ("① 关于小胰宝深卡", "关于小胰宝", True),
    ("② 尾图", "mmbiz.qpic.cn", True),
    ("③ 关注我们", "关注我们", True),
    ("④ 底部寄语落款", "With love and hope", False),
    ("⑤ 免责声明", "本文仅供科普", False),
)

# 微信 CDN 图片域名：带 Referer 请求会被防盗链替换成占位图，
# 必须靠 referrerpolicy="no-referrer" 才能拿到原图。
HOTLINK_HOSTS = ("mmbiz.qpic.cn", "pic.newrank.cn")


def strip_comments(html: str) -> str:
    """剥掉 HTML 注释。标签配平必须在剥注释之后做，否则注释里写的
    字面标签（比如说明文字里的 <section>）会被算成未闭合。"""
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def para_texts(html: str):
    return [
        re.sub(r"\s+", "", m.group(1))
        for m in re.finditer(r"<p[^>]*>(.*?)</p>", html, re.S)
    ]


def closest_diff(target: str, candidates):
    """在候选段里找与 target 最相近的一段，返回 (候选, 首个差异字符下标)。

    用途：foot 逐字比对失败时，报错文本按 60 字符截断，肉眼分不出
    ASCII 直引号 " 与中文弯引号 “” 这类单字符差异。这里直接指出
    差在第几个字符并把两边上下文打印出来。"""
    best, best_i = None, -1
    for c in candidates:
        if not c:
            continue
        i = 0
        while i < len(c) and i < len(target) and c[i] == target[i]:
            i += 1
        if i > best_i:
            best, best_i = c, i
    return best, best_i


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


def check_img_url_portability(clean: str):
    """图片 URL 路径里是否含「微信抓图器会二次编码」的字符。
    典型翻车样本（COS 上的 Pop Mart 头像）：
      /images/Pop%20Mart%20Character%20Front%20View%20(2).png
    路径里同时有已编码的 %20 和未编码的括号 —— 微信抓图时 % 被再编码成 %25，
    请求变成 ...%2520...%282%29.png，图床直接 404，表现就是「复制到编辑器图片不显示」。
    修法是换一个路径只含 [A-Za-z0-9/._-] 的地址，不是加属性、也不是换图床。
    """
    bad = []
    for m in re.finditer(r'<img\b[^>]*src="([^"]+)"', clean, re.I):
        u = m.group(1)
        if u.startswith("data:"):
            continue
        path = u.split("?", 1)[0]          # 查询串里的 ? & = 是正常的，只看路径
        risky = sorted({c for c in path if not (c.isalnum() or c in "/._-:")})
        if risky:
            bad.append((u, "".join(risky)))
    return bad


def check_foot_pieces(clean: str):
    """foot 五件套（关于小胰宝深卡 → 尾图 → 关注我们 → 落款 → 免责）。

    返回 (缺件列表, 乱序描述列表)。检查前必须是**剥掉注释**的 html：
    母版片段里那些 `<!-- ===== 关于小胰宝（固定区域，勿删） ===== -->` 锚点注释
    本身就含关键词，否则整篇都会误判成「已有」。
    """
    missing, ordered = [], []
    idx = {}
    for name, marker, use_last in FOOT_PIECES:
        positions = [m.start() for m in re.finditer(re.escape(marker), clean, re.I)]
        if not positions:
            missing.append(name)
            continue
        idx[name] = positions[-1] if use_last else positions[0]
    # 顺序校验：只比对都存在的那几件，缺件已单独报过
    prev = None
    for name, _, _ in FOOT_PIECES:
        if name not in idx:
            continue
        if prev is not None and idx[name] < idx[prev]:
            ordered.append(f"{prev} 之后本该是 {name}，实际跑到它前面了")
        prev = name
    return missing, ordered


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
            # 母版找不到不能「跳过」——跳过就等于这条检查永远不生效，
            # foot 整块丢失这类事故就是这么漏过去的（2026-10-03 ×2）。
            print(f"4 foot 逐字比对：✗ 找不到母版 {foot_path}，无法比对（先把母版放回 assets/）")
            ok &= False
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
                c, i = closest_diff(t, have)
                # 相似度够高才提示，避免对完全无关的段落给出误导性对照
                if c is not None and i >= max(10, len(t) // 3):
                    print(f"       ↳ 最接近的一段仅差在第 {i} 字符：")
                    print(f"          母版 {t[max(0, i - 12):i + 12]!r}")
                    print(f"          文章 {c[max(0, i - 12):i + 12]!r}")
                    if i >= len(t) or i >= len(c):
                        print("          （一边已结束 → 疑似在该段里追加/删减了文字）")
            ok &= not missing

            srcs = re.findall(r'<img[^>]+src="([^"]+)"', mtext)
            miss_img = [s for s in srcs if s not in html]
            print(f"5 foot 图片：{'✓ 齐备' if not miss_img else f'✗ 缺 {len(miss_img)} 张'}")
            for s in miss_img[:3]:
                print(f"     · {s[:70]}")
            ok &= not miss_img

    hotlink = [t for t in re.findall(r"<img\b[^>]*>", clean)
               if any(h in t for h in HOTLINK_HOSTS) and "referrerpolicy" not in t]
    print(f"6 防盗链属性：{'✓ 均带 no-referrer' if not hotlink else f'✗ {len(hotlink)} 张缺 referrerpolicy'}")
    for t in hotlink[:3]:
        print(f"     · {t[:70]}")
    ok &= not hotlink

    risky_urls = check_img_url_portability(clean)
    print(f"7 图片 URL 可移植性：{'✓ 路径无特殊字符' if not risky_urls else f'✗ {len(risky_urls)} 张含风险字符'}")
    for u, chars in risky_urls[:3]:
        print(f"     · [{chars}] {u[:78]}")
    ok &= not risky_urls

    polluted = []
    if re.search(r"<!DOCTYPE|<html[ >]|<head[ >]|<body[ >]", clean, re.I):
        polluted.append("套了完整 HTML 外壳")
    n_data = len(re.findall(r"\sdata-[a-z0-9-]+=", clean, re.I))
    if n_data:
        polluted.append(f"{n_data} 个 data-* 注入属性")
    n_amp = len(re.findall(r'<img[^>]*&amp;', clean, re.I))
    if n_amp:
        polluted.append(f"{n_amp} 张图的 src 里 & 被转义成 &amp;")
    print(f"8 预览污染：{'✓ 无' if not polluted else '✗ ' + '、'.join(polluted)}")
    if polluted:
        print("     修复：python3 scripts/restore-fragment.py <文章>")
    ok &= not polluted

    # 这条刻意放在「色值统计」之前：色值只是人工核对用，不该挡在结构检查前面
    missing_p, ordered_p = check_foot_pieces(clean)
    foot_bad = bool(missing_p or ordered_p)
    print(f"9 foot 五件套：{'✓ 五件齐全且顺序正确' if not foot_bad else '✗ ' + '；'.join(missing_p + ordered_p)}")
    if missing_p:
        print("     fix：照 assets/template3/foot_template.html 补整块 section，文案逐字照抄（表情/标点别动）")
    ok &= not foot_bad

    colors = re.findall(r"#[0-9A-Fa-f]{6}", html)
    norm = [c.lower() for c in colors]
    uniq = sorted(set(norm), key=lambda c: -norm.count(c))
    print(f"10 色值统计（共 {len(uniq)} 种，按出现次数）：")
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
