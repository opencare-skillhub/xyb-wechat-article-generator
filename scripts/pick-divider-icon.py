#!/usr/bin/env python3
"""分隔线图标随机抽取器（小胰宝全站共用组件）。

规则：每篇稿件开稿前**随机抽一个**图标，整篇 8 条分隔线统一用它，中途不换；
连续两篇不要撞同一个（--no-repeat 会记住上次用的）。

用法：
    # 抽一个（默认随机），打印可直接粘贴的分隔线 HTML
    python scripts/pick-divider-icon.py
    python scripts/pick-divider-icon.py --seed 2026-10-03   # 指定日期稳定复现
    python scripts/pick-divider-icon.py --icon tree         # 指定用某个
    python scripts/pick-divider-icon.py --list              # 看图标池
    python scripts/pick-divider-icon.py --tone purple       # 紫系配色
    # 把已有稿件的分隔线图标换掉（整篇统一替换）
    python scripts/pick-divider-icon.py --apply out/xxx.html
    python scripts/pick-divider-icon.py --apply out/xxx.html --seed 2026-10-03
    python scripts/pick-divider-icon.py --apply out/xxx.html --icon leaf
"""
import argparse
import json
import os
import random
import re
import sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(SKILL, ".last_divider_icon.json")
BASE = "https://picgo-1302991947.cos.ap-guangzhou.myqcloud.com/images"

# 图标池：加新图标时在这里追加一行（SVG 放进 assets/icons/、渲染、上传后即可用）
POOL = [
    # id,       中文名,      对应 emoji,  COS 文件名,                          气质/适用
    ("sprout",  "萌芽",       "🌱", "xyb-divider-sprout-20261003.png",     "通用首选，双叶+顶芽，最稳"),
    ("leaf",    "单片叶",     "🌿", "xyb-divider-leaf-20261003.png",       "柔和，适合用药/科普长文"),
    ("clover3", "三叶草",     "☘️", "xyb-divider-clover3-20261003.png",    "完整期/希望主题，绿色系最搭"),
    ("clover4", "四叶草",     "🍀", "xyb-divider-clover4-20261003.png",    "幸运、转机类主题"),
    ("seedling","圆胖幼苗",   "🍃", "xyb-divider-seedling-20261003.png",   "圆润亲和，适合病友向"),
    ("tree",    "小树苗",     "🌲", "xyb-divider-tree-20261003.png",       "深绿沉稳，适合治疗阶段/长期"),
    ("grass",   "小草",       "🍀", "xyb-divider-grass-20261003.png",      "轻盈、章节多时用"),
    ("clover-photo", "四叶草图", "🍀", "44740431290712064.png",           "实拍四叶草（用户 2026-10-03 选定，1024 方图自动裁圆）"),
]

TONES = {
    "green":  ("#E4F2EA", "#D3EBDE", "#A8D9BF", "#7FBF9F"),
    "purple": ("#EFE9F7", "#DED4EE", "#C6B5E0", "#A48FCC"),
    "warm":   ("#F7EFE6", "#EEDCC8", "#E0C3A4", "#C99A6B"),
}

IMG_STYLE = ("flex:0 0 auto;width:36px;height:36px;border-radius:50%;"
             "object-fit:cover;margin:0 10px;display:block;")


def url_of(icon_id):
    for i in POOL:
        if i[0] == icon_id:
            return "%s/%s" % (BASE, i[3])
    sys.exit("图标池里没有 %s，看 --list" % icon_id)


def divider_html(icon_id, tone="green"):
    c1, c2, c3, c4 = TONES[tone]
    url = url_of(icon_id)
    span = lambda c: '<span style="flex:1;height:1px;background:%s;"></span>' % c
    # 左右镜像：由外到内 c1→c2→c3→c4，中间夹 36×36 圆底图标
    inner = span(c1) + span(c2) + span(c3) + span(c4)
    img = ('<img src="%s" alt="小胰宝" style="%s">' % (url, IMG_STYLE)
           ).replace('style="flex', 'style="flex')
    return ('<section style="display:flex;align-items:center;margin:0 20px 20px">'
            + inner + img + span(c4) + span(c3) + span(c2) + span(c1)
            + '</section>')


def pick(args):
    if args.icon:
        return args.icon
    ids = [i[0] for i in POOL]
    seed = args.seed or os.environ.get("DIVIDER_SEED")
    if seed:
        rnd = random.Random(seed)          # 同日期多篇稿件抽到同一枚，便于复盘
    else:
        rnd = random.Random()
    last = None
    if os.path.exists(STATE) and args.no_repeat:
        last = json.load(open(STATE, encoding="utf-8")).get("last")
    choices = [i for i in ids if i != last] or ids
    return rnd.choice(choices)


def apply_icon(path, icon_id, tone):
    if not os.path.exists(path):
        sys.exit("文件不存在：%s" % path)
    html = open(path, encoding="utf-8").read()
    # 只替换分隔线那一种 img：<img ..._width:36px;height:36px...> 或 src 含历史图标名
    pattern = re.compile(
        r'<img[^>]*?(?:width:36px;height:36px|xyb-divider-|xyb-clover-icon|xyb-plant-icon)[^>]*>',
        re.I | re.S)
    found = pattern.findall(html)
    if not found:
        sys.exit("没找到分隔线 img（既不是 36×36 也不是 xyb-divider / clover / plant 图标），跳过")
    new_img = '<img src="%s" alt="小胰宝" style="%s">' % (url_of(icon_id), IMG_STYLE)
    html, n = pattern.subn(lambda m: new_img, html)
    open(path, "w", encoding="utf-8").write(html)
    json.dump({"last": icon_id}, open(STATE, "w", encoding="utf-8"))
    print("已替换 %s 中 %d 处分隔线图标 -> %s" % (path, n, icon_id))
    return n


def main():
    ap = argparse.ArgumentParser(description="分隔线图标随机抽取")
    ap.add_argument("--list", action="store_true", help="列出图标池")
    ap.add_argument("--icon", help="指定图标 id")
    ap.add_argument("--tone", default="green", choices=list(TONES), help="分隔线配色")
    ap.add_argument("--seed", help="用固定字符串抽取（同 seed 必得同一枚）")
    ap.add_argument("--no-repeat", action="store_true", default=True,
                    help="自动避开上一篇用的图标（默认开）")
    ap.add_argument("--apply", metavar="HTML", help="把该文件的分隔线图标统一换成新抽到的")
    args = ap.parse_args()

    if args.list:
        print("  %-9s %-9s %-4s %s" % ("id", "中文名", "emoji", "说明"))
        for i in POOL:
            print("  %-9s %-9s %-4s %s" % (i[0], i[1], i[2], i[4]))
        print("\n  COS 基址：%s" % BASE)
        print("  --tone: %s" % "/".join(TONES))
        return

    icon_id = pick(args)
    if args.apply:
        apply_icon(args.apply, icon_id, args.tone)
        return
    json.dump({"last": icon_id}, open(STATE, "w", encoding="utf-8"))
    meta = next(i for i in POOL if i[0] == icon_id)
    print("# 抽中：%s（%s %s）— %s" % (icon_id, meta[1], meta[2], meta[3]))
    print("# COS：%s/%s" % (BASE, meta[3]))
    print("# tone：%s" % args.tone)
    print()
    print(divider_html(icon_id, args.tone))


if __name__ == "__main__":
    main()
