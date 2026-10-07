#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
actionlist 系列：从主骨架派生 6 套配色。
主骨架 bm_template 风格一致，用 token 替换保证 6 色结构 100% 相同。

配色逻辑（60-30-10 + WCAG）：
- INK 深墨（巨型数字/编号圆底，为标题与结构的"骨"）
- TITLE 标题色（比 INK 略浅，用于文字标题）
- TEXT 正文（WCAG ≥7:1）
- MUTED 辅助灰蓝（英文小标/说明，WCAG ≥4.5:1）
- MAIN 主色（下划线/圆点/竖条，饱和度高，只占小面积）
- TINT 浅底（看点卡底/巨型数字，浅）
- LINE 描线（分隔线，浅）
"""
import pathlib, re

BASE = pathlib.Path(__file__).parent
SRC = BASE / "actionlist_template.html"

PALETTES = {
    "蓝色": {  # 基准·医疗权威（源自原稿）
        "C_INK": "#0D2740", "C_TITLE": "#0D2740", "C_TEXT": "#2F4358",
        "C_MUTED": "#4A7398", "C_MAIN": "#0070C0", "C_MAIN_RGB": "0,112,192",
        "C_MAIN_TINT": "#A8CBEA", "C_TINT": "#DDEAF6", "C_LINE": "#CFE0F2",
        "banner_bg": "#eef4fb", "banner_border": "#0070C0", "banner_text": "#2F4358",
    },
    "紫色": {  # 品牌紫 #5c4a7a 系（胰腺癌宣传）
        "C_INK": "#2E2340", "C_TITLE": "#3A2C50", "C_TEXT": "#4A4358",
        "C_MUTED": "#6E6288", "C_MAIN": "#5C4A7A", "C_MAIN_RGB": "92,74,122",
        "C_MAIN_TINT": "#C0B2DC", "C_TINT": "#E4DEF0", "C_LINE": "#D2C9E6",
        "banner_bg": "#f5f2fa", "banner_border": "#5C4A7A", "banner_text": "#4A4358",
    },
    "绿色": {  # 生机健康（对齐品牌绿 #2d8c6e）
        "C_INK": "#0C2E22", "C_TITLE": "#124534", "C_TEXT": "#2F4A3E",
        "C_MUTED": "#4F7A66", "C_MAIN": "#2D8C6E", "C_MAIN_RGB": "45,140,110",
        "C_MAIN_TINT": "#A5D4BF", "C_TINT": "#D9EDE3", "C_LINE": "#C2E0D2",
        "banner_bg": "#eefaf4", "banner_border": "#2D8C6E", "banner_text": "#2F4A3E",
    },
    "橙色": {  # 温暖行动（对齐 bm 橙 #E94560/#F5A623 调性但更柔和）
        "C_INK": "#5A2E10", "C_TITLE": "#7A3F14", "C_TEXT": "#5C4632",
        "C_MUTED": "#8F6539", "C_MAIN": "#C96A28", "C_MAIN_RGB": "224,123,57",
        "C_MAIN_TINT": "#F2C39C", "C_TINT": "#FBE6D2", "C_LINE": "#F2D3B4",
        "banner_bg": "#fdf4ec", "banner_border": "#C96A28", "banner_text": "#5C4632",
    },
    "红色": {  # 警示重要（对齐 bm 红 #E94560 调性，更沉稳）
        "C_INK": "#5C1420", "C_TITLE": "#7A1C2C", "C_TEXT": "#5E3A40",
        "C_MUTED": "#96586A", "C_MAIN": "#C64055", "C_MAIN_RGB": "198,64,85",
        "C_MAIN_TINT": "#EAAAB4", "C_TINT": "#F7DEE2", "C_LINE": "#EDC4CB",
        "banner_bg": "#fdf0f2", "banner_border": "#C64055", "banner_text": "#5E3A40",
    },
    "青色": {  # 清新沉稳（比蓝更青绿，差异化）
        "C_INK": "#0C2E33", "C_TITLE": "#0F3D45", "C_TEXT": "#2C4A50",
        "C_MUTED": "#4C737B", "C_MAIN": "#12808F", "C_MAIN_RGB": "18,128,143",
        "C_MAIN_TINT": "#9CCBD3", "C_TINT": "#D7EBEE", "C_LINE": "#BFDDE2",
        "banner_bg": "#eef8f9", "banner_border": "#12808F", "banner_text": "#2C4A50",
    },
}

def build(pal: dict, name: str) -> str:
    s = SRC.read_text(encoding="utf-8")
    # 颜色 token 替换
    for k in ["C_INK","C_TITLE","C_TEXT","C_MUTED","C_MAIN","C_MAIN_TINT","C_MAIN_RGB","C_TINT","C_LINE"]:
        s = s.replace("{{"+k+"}}", pal[k])
    # banner 换色
    s = s.replace("background:#eef0f3;border:1px dashed #9aa3ad", f"background:{pal['banner_bg']};border:1px dashed {pal['banner_border']}")
    s = s.replace(".banner b{color:#2F4358;}", f".banner b{{color:{pal['C_TITLE']};}}")
    s = s.replace("color:#54606b;", f"color:{pal['banner_text']};")
    # 标题与文案
    s = s.replace("<title>actionlist 模版 · 主骨架（token 化，6 色共用）</title>", f"<title>actionlist 模版 · {name}（效果预览）</title>")
    s = s.replace("<b>actionlist 主骨架 · token 化</b>", f"<b>actionlist 系列 · {name} · 效果预览</b>")
    s = s.replace("actionlist 系列主骨架（行动清单 / 步骤指南风）", f"actionlist 系列 · {name}")
    # 残留 token 检查
    leftover = re.findall(r"\{\{[A-Z_]+\}\}", s)
    if leftover:
        print(f"[warn] {name} 残留 token: {set(leftover)}")
    return s

def main():
    for name, pal in PALETTES.items():
        out = build(pal, name)
        (BASE / f"actionlist-{name}.html").write_text(out, encoding="utf-8")
        print(f"[ok] actionlist-{name}.html")
    print("[done] 6 色派生完成")

if __name__ == "__main__":
    main()
