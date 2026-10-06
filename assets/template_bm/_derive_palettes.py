#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 bm-template-橙色.html 派生紫/绿两色渲染稿。
策略：先把橙色的「结构性色值」换成内部 token，再把 token 替换为目标色值。
这样保证三色结构 100% 一致，只换颜色。
"""
import re, pathlib

BASE = pathlib.Path(__file__).parent
SRC = BASE / "bm-template-橙色.html"

# 目标配色
PALETTES = {
    "紫色": {
        "GRAD_A": "#8A4FD0", "GRAD_B": "#C9A6E6",
        "ANCHOR": "#2E1F4D", "ANCHOR_DARK": "#1A1030",
        "ACCENT": "#6E4FA3",
        "banner_bg": "#f6f3fb", "banner_border": "#8A4FD0", "banner_text": "#5a3d86", "banner_b": "#6E4FA3",
    },
    "绿色": {
        "GRAD_A": "#1FAE7E", "GRAD_B": "#7FD8A8",
        "ANCHOR": "#0C3A2C", "ANCHOR_DARK": "#07251C",
        "ACCENT": "#137A57",
        "banner_bg": "#eefaf3", "banner_border": "#1FAE7E", "banner_text": "#137a57", "banner_b": "#0C3A2C",
    },
}

# 橙色 -> 内部 token 的映射（顺序敏感：先替换组合渐变，再替换单色）
def to_tokens(html: str) -> str:
    # 组合渐变：锚点 -> 渐变首段
    html = html.replace("linear-gradient(135deg, #0F3460, #E94560)", "linear-gradient(135deg, @@ANCHOR@@, @@GRAD_A@@)")
    # 组合渐变：渐变首段 -> 渐变次段
    html = html.replace("linear-gradient(135deg, #E94560, #F5A623)", "linear-gradient(135deg, @@GRAD_A@@, @@GRAD_B@@)")
    # rgba 透明度形式
    html = html.replace("rgba(233,69,96,", "rgba(@@ACCENT_RGB@@,")
    html = html.replace("rgba(15,52,96,", "rgba(@@ANCHOR_RGB@@,")
    # 单色
    html = html.replace("#0F3460", "@@ANCHOR@@")
    html = html.replace("#08101C", "@@ANCHOR_DARK@@")
    html = html.replace("#E94560", "@@ACCENT@@")   # 先把剩余的 E94560（全作强调色）标记
    html = html.replace("#F5A623", "@@GRAD_B@@")
    return html

# 注意：token 化后 @@ACCENT@@ 出现在原本 GRAD_A 的位置吗？——不会，
# 因为所有 GRAD_A 都已被上面的组合渐变替换成 @@GRAD_A@@。
# 但为保险，后续把 @@ACCENT@@ 在渐变上下文里视作强调色（橙色本就 accent=gradA 同值，派生色系分开）。

def apply_palette(html: str, pal: dict, color_name: str) -> str:
    # GRAD_A 在橙色里等于 ACCENT，派生色系不同：
    # 组合渐变里的首段用 GRAD_A，独立强调（BREAKING 胶囊/左竖条/高亮/关注我们）用 ACCENT。
    # 由于 token 化时已区分：@@GRAD_A@@ 只出现在组合渐变，@@ACCENT@@ 出现在独立强调。
    mapping = {
        "@@GRAD_A@@": pal["GRAD_A"],
        "@@GRAD_B@@": pal["GRAD_B"],
        "@@ANCHOR@@": pal["ANCHOR"],
        "@@ANCHOR_DARK@@": pal["ANCHOR_DARK"],
        "@@ACCENT@@": pal["ACCENT"],
        "@@ACCENT_RGB@@": ",".join(str(int(pal["ACCENT"].lstrip("#")[i:i+2], 16)) for i in (0, 2, 4)),
        "@@ANCHOR_RGB@@": ",".join(str(int(pal["ANCHOR"].lstrip("#")[i:i+2], 16)) for i in (0, 2, 4)),
    }
    for k, v in mapping.items():
        html = html.replace(k, v)
    # banner 换色
    html = html.replace("background:#fff7ea;border:1px dashed #f5a623", f"background:{pal['banner_bg']};border:1px dashed {pal['banner_border']}")
    html = html.replace("color:#9c5a16;", f"color:{pal['banner_text']};")
    html = html.replace(".banner b{color:#c44536;}", f".banner b{{color:{pal['banner_b']};}}")
    # banner 文案
    html = html.replace("<b>bm 系列 · 橙色 v2 · 效果预览</b>", f"<b>bm 系列 · {color_name} v2 · 效果预览</b>")
    # title
    html = html.replace("<title>bm 模版 · 橙色（效果预览 v2）</title>", f"<title>bm 模版 · {color_name}（效果预览 v2）</title>")
    return html

def main():
    src = SRC.read_text(encoding="utf-8")
    tokened = to_tokens(src)
    assert "@@ACCENT@@" in tokened, "token 化失败：未发现 ACCENT"
    for name, pal in PALETTES.items():
        out = apply_palette(tokened, pal, name)
        # 清理可能残留的 token（保险）
        leftover = re.findall(r"@@[A-Z_]+@@", out)
        if leftover:
            print(f"[warn] {name} 残留 token: {set(leftover)}")
        dst = BASE / f"bm-template-{name}.html"
        dst.write_text(out, encoding="utf-8")
        print(f"[ok] 写出 {dst.name}")
    # 校验：橙色原文件不应被改动
    print("[done] 紫/绿派生完成")

if __name__ == "__main__":
    main()
