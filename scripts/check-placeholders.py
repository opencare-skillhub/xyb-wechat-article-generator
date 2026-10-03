#!/usr/bin/env python3
"""模版占位符一致性检查：模版 HTML 用的占位符，必须在填写规范里都有说明。

用途：改模版（加/删 __XXX__）时，防止文档漂移——模版里冒出一个新占位符、
规范里却查不到，下次填的人不知道该往里放什么。

用法：
    python3 scripts/check-placeholders.py [模版目录]
    默认目录：assets/template8-alliance
"""
import pathlib
import re
import sys


def placeholders(text: str) -> set:
    """去掉 HTML 注释后再取占位符——注释里的说明性提及不算。"""
    body = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return set(re.findall(r"__([A-Z0-9_]+)__", body))


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent.parent
    target = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root / "assets/template8-alliance"
    target = target if target.is_absolute() else (root / target)

    tpls = sorted(target.glob("*.html"))
    specs = sorted(target.glob("*_spec.md"))
    if not tpls:
        print(f"✗ {target} 下没有 .html 模版")
        return 1
    if not specs:
        print(f"⚠️ {target} 下没有 *_spec.md，跳过比对")
        return 0

    # 所有模版的占位符并集；所有 spec 的声明并集
    in_tpl = set()
    for t in tpls:
        in_tpl |= placeholders(t.read_text(encoding="utf-8"))
    declared = set()
    for s in specs:
        declared |= set(re.findall(r"`__([A-Z0-9_]+)__`", s.read_text(encoding="utf-8")))

    print(f"模版：{', '.join(t.name for t in tpls)}")
    print(f"规范：{', '.join(s.name for s in specs)}")
    print(f"模版占位符 {len(in_tpl)} 个，规范声明 {len(declared)} 个\n")

    undocumented = sorted(in_tpl - declared)
    unused = sorted(declared - in_tpl)

    ok = True
    if undocumented:
        ok = False
        print("✗ 模版用了但规范没写（必须补进规范表格）：")
        for p in undocumented:
            print(f"    __{p}__")
    else:
        print("✓ 模版里每个占位符都能在规范里查到")

    if unused:
        print("\n⚠️ 规范声明了但模版没用到（正常可能：可选项 / 已改名的残留）：")
        for p in unused:
            print(f"    __{p}__")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
