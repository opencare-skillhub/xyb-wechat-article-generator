# 分隔线图标池（小胰宝全站共用组件）

> 元素规则正文见技能根目录 `skill.md` 的「9. 分隔线（全站共用组件）」，那里管**怎么排版、怎么随机抽**；
> 这个文件只管**图标本体**：有哪些、各自长什么样、文件在哪、怎么加新图标。

## 1. 图标清单（7 枚，全部植物类）

| id | 中文名 | emoji | SVG 源 | PNG（384 透明底） | COS 地址 | 气质 / 什么时候用 |
|---|---|---|---|---|---|---|
| `sprout` | 萌芽 | 🌱 | `sprout.svg` | `sprout-384.png` | `https://picgo-1302991947.cos.ap-guangzhou.myqcloud.com/images/xyb-divider-sprout-20261003.png` | 通用首选，双叶＋顶芽，最稳 |
| `leaf` | 单片叶 | 🌿 | `leaf.svg` | `leaf-384.png` | `.../images/xyb-divider-leaf-20261003.png` | 柔和，用药 / 科普长文 |
| `clover3` | 三叶草 | ☘️ | `clover3.svg` | `clover3-384.png` | `.../images/xyb-divider-clover3-20261003.png` | 完整期 / 希望主题，绿色系最搭 |
| `clover4` | 四叶草 | 🍀 | `clover4.svg` | `clover4-384.png` | `.../images/xyb-divider-clover4-20261003.png` | 幸运、转机类主题 |
| `seedling` | 圆胖幼苗 | 🍃 | `seedling.svg` | `seedling-384.png` | `.../images/xyb-divider-seedling-20261003.png` | 圆润亲和，病友向 |
| `tree` | 小树苗 | 🌲 | `tree.svg` | `tree-384.png` | `.../images/xyb-divider-tree-20261003.png` | 深绿沉稳，治疗阶段 / 长期管理 |
| `grass` | 小草 | 🍀 | `grass.svg` | `grass-384.png` | `.../images/xyb-divider-grass-20261003.png` | 轻盈，章节特别多时用 |

COS 基址：`https://picgo-1302991947.cos.ap-guangzhou.myqcloud.com/images/`
（历史遗留一枚旧 `xyb-clover-icon-20261003.png` / 圆底绿苗 `xyb-plant-icon`，属于被淘汰的早期形态，
新稿不要再引用——筛过一轮，圆底绿苗用户反馈过"很怪"，现在统一用**透明底**的这 7 枚。）

## 2. 硬约束

- **一篇一封**：抽到哪枚就整篇用哪枚，通常 6～10 条分隔线，中途不换。
- **中间那枚只能是植物类**，`xyb-head-logo`（机器人吉祥物）是头像，别拿来当分隔线中间那枚。
- 图标在 HTML 里固定 `width:36px;height:36px;border-radius:50%;object-fit:cover;margin:0 10px`，`alt="小胰宝"`。
- 外挂百度 / 千图的现成素材图一律不用：版权风险 + 微信抓取外链可能被拦；自绘 SVG 改一版重渲即可。

## 3. 加一枚新图标（三步）

```bash
# 1) 手写 assets/icons/<id>.svg（viewBox 0 0 96 96，透明底，主色用绿系 /A8D9BF-#1F7A6B 四阶）

# 2) 渲成 384 透明底 PNG（只启动一次 Chrome，全目录一起出）
python scripts/render-divider-icons.py

# 3) 传图床，然后到 scripts/pick-divider-icon.py 的 POOL 里加一行
python ~/.workbuddy/skills/picgo-cos-upload/scripts/upload_to_picgo.py \
    assets/icons/<id>-384.png xyb-divider-<id>-<YYYYMMDD>.png
```

`POOL` 一行五列：`(id, 中文名, emoji, 上传的文件名, 气质说明)`。加完 `--list` 就能看到新枚。

## 4. 相关脚本

| 脚本 | 干什么 |
|---|---|
| `scripts/pick-divider-icon.py` | 随机抽一枚，打印可直贴的分隔线 HTML；`--apply 稿件.html` 整篇替换 |
| `scripts/render-divider-icons.py` | 把 `assets/icons/*.svg` 渲成 384 透明底 PNG |
| `scripts/verify-article.py` | 出稿校验（10 项），分隔线 img 属白名单标签，不影响检查 |

记账文件：技能根目录 `.last_divider_icon.json`（上次用过的 id，`--no-repeat` 靠它避重）。
