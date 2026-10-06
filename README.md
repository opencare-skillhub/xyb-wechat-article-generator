# 小胰宝公众号文章生成器

一个基于 Kiro Skill 的微信公众号文章自动排版工具，专为"小胰宝"公益科普项目设计。

## 功能

- 将 Markdown/文本素材自动转换为微信公众号兼容的 inline style HTML
- **九套版式系列**：v3.1 生机微光（默认，卡片错落 + 高对比阅读优化）、莫兰迪柔和卡片风、中国风/特展版式风、瑞慈医疗服务版、病历记录风、med 说明书解读风、review 医生点评风（前沿荟萃学术风，蓝/紫双色）、alliance 医患联合群版（紫色）、bm 前沿速递风（杂志快讯版式，橙/紫/绿三色）
- 每系列 9 套配色（8 套莫兰迪色系 + Tiffany蓝绿）
- v3.1 可读性铁律：正文用深色 token，浅色仅用于边框/装饰，杜绝"浅字叠浅底"
- 内置多种排版组件（错位标题卡、胶囊标签、大字号数据卡、气泡时间轴、CSS几何分隔线等）
- 自动附加固定底部区域（组织介绍、社交媒体、签名卡片）
- 输出可直接粘贴到135编辑器使用
- **template8 医患联合群模版**：填完占位符即出合规长文（品牌头部／三条边界／社区能力矩阵／本地志愿者招募／结尾寄语五块话术已写死，只替换医院·科室·主任·研究·二维码）
- **医生卡片「左图右简历」结构**：照片在左、姓名与职称在右，教育/擅长/任职/科研/下沉五段通栏在照片下方；含头衔多源冲突的取舍规则（官网 > 政府/学会 > 第三方平台）
- **生成后自动校验**：`verify-article.py` 十项检查（含预览污染、尾图防盗链、图片 URL 可移植性），一键 `restore-fragment.py` 还原被预览面板改写的源文件
- **分隔线图标池（全站共用组件）**：8 枚植物类图标（萌芽 / 单片叶 / 三叶草 / 四叶草 / 圆胖幼苗 / 小树苗 / 小草 / 实拍四叶草图），开稿前 `pick-divider-icon.py` 随机抽一枚、整篇统一（`--seed` 可复现、`--no-repeat` 防连续两篇撞车、`--apply` 整篇替换）；分隔线结构规范与「编辑器回写稿整条标准化重建」规则见 skill.md 组件 9
- **小胰宝头像/Logo 统一地址**：`https://picgo-1302991947.cos.ap-guangzhou.myqcloud.com/images/xyb.png`（512×512；旧的 `xyb-head-logo-20261003.png` 与更早的 Pop Mart 长文件名地址已弃用——路径含 `%20`/括号会被微信二次编码 404）
- **占位符一致性检查**：改 template8 后跑 `check-placeholders.py`，防止模版与 spec 漂移
- **临床 / 药物介绍胶囊卡片组件**（`assets/component-clinical-card/`，紫色）：一章要讲多个药物或多项在招研究时用，三种卡——标准卡（一个分子一张，7 个行组：瘤种→试验→分期→中心→剂量→机制→数据）／迷你卡（中心速查：找谁、什么状态、怎么联系）／灰底解释框（为什么还没开筛、数据口径）。标签写死只换右侧文字，19 个占位符填完即成稿；含 375px 实测的 flex 硬约束（标签 2～3 字、左列不加 `min-width:0`、右列必留）与八条内容红线（机制未披露就写未披露、注册节点≠临床结果、同靶点不同分子不可互套数据、小样本标例数等）
- **配套的两个技能**：公众号文章走本仓库（`xyb-wechat-article-generator`）；长篇白皮书 / DOCX 走 [`xyb-whitepaper-writer`](https://github.com/opencare-skillhub/xyb-whitepaper-writer)

## 目录结构

```
xyb-wechat-article-generator/
├── README.md                    # 项目说明
├── skill.md                     # Kiro Skill 定义文件
├── assets/
│   ├── template3/               # 模板系列3：生机微光 v3.1（默认，10套配色）
│   │   ├── xyb3_template.html               # 🌿 治愈翡翠绿+琥珀暖阳（默认旗舰）
│   │   ├── foot_template.html               # 📌 v3 foot 母版（深色卡片版基准）
│   │   ├── xyb3_template_morandi.html       # 🤎 莫兰迪暖棕+陶土暖阳
│   │   ├── xyb3_template_morandi_blue.html  # 🔵 雾霾蓝+琥珀暖阳
│   │   ├── xyb3_template_morandi_gray.html  # ⚪ 高级灰+琥珀暖阳
│   │   ├── xyb3_template_morandi_pink.html  # 🩷 豆沙粉+蜜桃暖阳
│   │   ├── xyb3_template_morandi_red.html   # 🔴 赭红+鎏金暖阳
│   │   ├── xyb3_template_morandi_purple.html # 🟣 烟紫+琥珀暖阳
│   │   ├── xyb3_template_morandi_green.html  # 🟢 灰绿自然+琥珀暖阳
│   │   └── xyb3_template_tiffany.html        # 💎 蒂芙尼蓝绿+珊瑚暖阳
│   ├── template1/               # 模板系列1：莫兰迪柔和卡片风（9套配色 + foot母版）
│   │   ├── foot_template.html              # 📌 foot 强调版母版（固定footer基准）
│   │   ├── xyb_template.html              # 🌿 森林绿（默认）
│   │   ├── xyb_template_morandi.html      # 🤎 莫兰迪暖棕
│   │   ├── xyb_template_morandi_blue.html # 🔵 莫兰迪蓝
│   │   ├── xyb_template_morandi_gray.html # ⚪ 莫兰迪灰
│   │   ├── xyb_template_morandi_pink.html # 🩷 莫兰迪粉
│   │   ├── xyb_template_morandi_red.html  # 🔴 莫兰迪红
│   │   ├── xyb_template_morandi_purple.html # 🟣 莫兰迪紫
│   │   ├── xyb_template_morandi_green.html  # 🟢 莫兰迪绿
│   │   └── xyb_template_tiffany.html       # 💎 Tiffany蓝绿
│   ├── template2/               # 模板系列2：中国风/特展版式风（10套配色）
│   │   ├── xyb2_template.html              # 🏮 朱砂深红（默认，中国风）
│   │   ├── xyb2_template_morandi.html      # 🤎 莫兰迪暖棕
│   │   ├── xyb2_template_morandi_blue.html # 🔵 莫兰迪蓝
│   │   ├── xyb2_template_morandi_gray.html # ⚪ 莫兰迪灰
│   │   ├── xyb2_template_morandi_pink.html # 🩷 莫兰迪粉
│   │   ├── xyb2_template_morandi_red.html  # 🔴 莫兰迪红
│   │   ├── xyb2_template_morandi_purple.html # 🟣 莫兰迪紫
│   │   ├── xyb2_template_morandi_green.html  # 🟢 莫兰迪绿
│   │   └── xyb2_template_tiffany.html       # 💎 Tiffany蓝绿
│   ├── template5-khub/          # 模板系列5：病历记录风（衬线字体+粗黑边框+暖米底）
│   │   ├── khub_template.html               # 📋 病历档案风主模板
│   │   ├── khub_components.html             # 🧩 组件库（SectionCard/Blockquote/ColorBar等）
│   │   ├── khub_foot_template.html          # 📌 病历风格 foot 母版
│   │   └── khub_template_spec.md            # 📐 视觉抽取规格
│   ├── template6-med/           # 模板系列6：med 说明模版（深蓝权威风，说明书/用药指南）
│   │   ├── med_template.html                # 🩺 说明书解读主模板
│   │   ├── med_components.html              # 🧩 组件库（对照表/警示框/风险标签/清单）
│   │   ├── med_foot_template.html           # 📌 深蓝权威版 foot 母版
│   │   └── med_template_spec.md             # 📐 视觉抽取规格
│   ├── template7-review/        # 模板系列7：医生点评风（前沿荟萃学术风）
│   │   ├── review_template.html             # 👨‍⚕️ 蓝底点评主模板
│   │   ├── review_template_purple.html      # 🟣 紫底点评主模板
│   │   ├── review_components.html           # 🧩 组件库
│   │   ├── review_foot_template.html        # 📌 通用 foot 母版
│   │   ├── review_foot_purple.html          # 📌 紫色 foot 母版（foot 逐字比对用）
│   │   ├── preview_blue.png / preview_purple.png  # 🖼️ 版式预览图
│   │   └── review_template_spec.md          # 📐 视觉抽取规格
│   ├── template8-alliance/      # 模板系列8：医患联合群（科室共建招募，紫色）
│   │   ├── alliance_template_purple.html    # 🤝 13 节骨架 + 36 个占位符
│   │   └── alliance_template_spec.md        # 📐 占位符清单与硬规则（4 战略定位 / 5 医生卡片 / 6.1 新启动研究高亮卡）
│   ├── template_bm/              # 模板系列 bm：前沿速递风（杂志快讯，橙/紫/绿三色）
│   │   ├── bm_template.html                # 📰 token 化主骨架（9 个 C_* token，三色共用）
│   │   ├── bm-template-橙色.html            # 🟠 橙色已渲染示例（母版）
│   │   ├── bm-template-紫色.html            # 🟣 紫色已渲染示例（派生）
│   │   ├── bm-template-绿色.html            # 🟢 绿色已渲染示例（派生）
│   │   ├── bm-template-spec.md              # 📐 Token/三色映射/12 组件/logo·foot·段落分隔规则
│   │   └── _derive_palettes.py              # 🔧 从橙色母版派生紫/绿，保证三色结构一致
│   ├── template_qa/             # 胶囊问答组件（医生答疑短问答）
│   │   └── qa_capsule.html                # 💬 问答胶囊卡
│   ├── component-clinical-card/ # 💊 临床/药物介绍胶囊卡组件（紫色，见功能清单）
│   │   ├── clinical_card_template.html  # ⚕️ 可填空骨架：标准卡 + 迷你卡 + 灰底解释框（19 占位符）
│   │   ├── clinical_card_spec.md        # 📐 行序 / 色板 / flex 硬约束 / 八条内容红线
│   │   └── clinical_card_specimen.html  # 🖼️ 成品样本（号码已脱敏，仅对照版式用）
│   ├── icons/                   # 🌱 分隔线图标池（8 枚植物类，规则见 skill.md 组件 9）
│   │   ├── sprout|leaf|clover3|clover4|seedling|tree|grass .svg + -384.png  # 自绘透明底
│   │   └── divider-icon-pool.md         # 📐 图标资产登记（COS 地址 / 气质 / 加新图标三步）
│   └── images/                  # 图片资源
├── examples/                    # 示例输出
│   ├── 云南白药_公众号_blue.html
│   └── 化疗贫血科学管理_公众号_purple.html
├── scripts/                     # 校验脚本
│   ├── verify-article.py        # ✅ 十项检查：预览污染 / 禁用标签 / 标签配平 / 裸 URL /
│   │                            #    foot 逐字比对 / foot 图片 / 尾图防盗链属性 / 图片 URL 可移植性 / 预览污染 /
│   │                            #    foot 五件套 / 色值
│   ├── verify-layout.py         # 📐 封面标题换行 + 整篇溢出检测
│   ├── verify-qrcode.swift      # 🔍 二维码验扫（源图与渲染截图都解码，macOS Vision）
│   ├── check-placeholders.py    # 🔢 template8 占位符与 spec 双向一致性（改模版后必跑）
│   ├── restore-fragment.py      # 🩹 把被预览面板改写成完整 HTML 的文章还原成公众号纯片段
│   ├── pick-divider-icon.py     # 🎲 分隔线图标随机抽取（--seed 可复现 / --apply 整篇替换 / --list 图标池）
│   └── render-divider-icons.py  # 🖼️ assets/icons/*.svg 批量渲 384 透明底 PNG（加新图标后跑）
└── output/                      # 生成文件输出目录
```

## 生成后校验与修复（必做）

发布前跑验证器，十项全过才算交付：

```bash
python3 scripts/verify-article.py <文章路径> --foot assets/template7-review/review_foot_purple.html
```

| # | 检查项 | 抓的是什么 |
|---|--------|-----------|
| 1 | 禁用标签/属性 | `<div>` / `<style>` / `class` 等微信不支持或样式全丢的写法 |
| 2 | 标签配平 | `<section>` 开合是否配对 |
| 3 | 裸 URL | 正文里没包 `<a>` 的裸链接（微信不识别，验证器判不合格） |
| 4 | foot 逐字比对 | 与 foot 母版逐字比对（含标点；失败会打印首个差异字符与上下文） |
| 5 | foot 图片 | 尾图路径是否与母版一致 |
| 6 | 防盗链属性 | foot 的 `mmbiz.qpic.cn` 尾图必须带 `referrerpolicy="no-referrer"` |
| 7 | 图片 URL 可移植性 | URL 路径只能含 `[A-Za-z0-9/._-]`——含 `%` 括号空格中文会被微信二次编码（`%20`→`%2520`）导致图床 404 |
| 8 | 预览污染 | 文章被 IDE / 工具的预览面板改写成完整 HTML 文档（套 `<html>` 外壳、给每个标签塞 `data-*` 属性、`&` 转义成 `&amp;`） |
| 9 | foot 五件套 | `① 关于小胰宝深卡 → ② 尾图 → ③ 关注我们 → ④ 底部寄语落款（With love and hope）→ ⑤ 免责声明`，缺件或顺序颠倒即不过。硬规则，不依赖母版文件 |
| 10 | 色值统计 | 人工核对用，可用 `--require-color` 强制要求某色值出现 |

> foot 五件套单独成项，是因为母版逐字比对查不出「整块 section 被删 / 被挪 / 顺序调换」——
> 这条漏过 2-3 次，别用人工 grep 代替。母版文件找不到时验证器现在直接报 ✗（旧版是「⚠️ 跳过」，等于这条检查悄悄失效）。

其他脚本：

```bash
python3 scripts/verify-layout.py <文章>        # 封面标题换行 + 整篇溢出
swift   scripts/verify-qrcode.swift <图>        # 二维码能否扫出（源图与渲染截图都验）
python3 scripts/check-placeholders.py                            # 改 template8 后，占位符与 spec 是否漂移
python3 scripts/check-placeholders.py assets/component-clinical-card  # 临床卡组件同理（脚本默认查 template8，可传目录）
python3 scripts/restore-fragment.py <文章>       # 还原被预览面板污染的文章（--dry-run 只看不改）
```

### 分隔线图标（全站共用，开稿先抽）

```bash
python3 scripts/pick-divider-icon.py --seed 2026-10-03 --tone green   # 随机抽一枚，打印可直贴的分隔线 HTML
python3 scripts/pick-divider-icon.py --apply <文章>                    # 整篇统一换图标（编辑器回写稿会先标准化重建）
python3 scripts/render-divider-icons.py                               # assets/icons/ 加了新 SVG 后重渲 PNG
```

- 规则：**一篇一封**——全篇 6～10 条分隔线用同一枚，`--seed` 同日期必得同一枚（可复盘），`--no-repeat` 默认避开上一篇。
- 图标池、结构规范（四段横线 + 居中 36×36 圆底图标、左右镜像）与「整条标准化重建」规则，见 skill.md「组件 9」
  和 `assets/icons/divider-icon-pool.md`。

### ⚠️ 两个高频坑

**尾图防盗链**：`mmbiz.qpic.cn` 的尾图带 Referer 请求会被换成 140×140 的「未经允许不可引用」占位图，
换域名没用（镜像 `pic.newrank.cn` 直接 403，两者都得靠 `referrerpolicy="no-referrer"`）。
渲染长图时同理——Playwright 里要在 `route` 回调里剥掉 `referer` 头再 `continue_()`，否则截图里尾图是小的。

**预览污染**：部分 IDE 与 AI 工具的预览服务会**就地改写源文件**，不是只改预览副本。
（某些预览服务还会给每个标签塞 `data-page-node-id` 之类属性、`&` 转义成 `&amp;`。）
所以预览前先把文章复制到 `/tmp`，或预览完立刻 `restore-fragment.py` 还原。
历史遗留中招文件：`PanRAS_RASi报名路径_复旦肿瘤HRS7172_公众号_purple.html` 与 `..._purple(2).html`。

## 新人快速上手：从装工具到发布（照着做 8 步）

第一次用、还没搭过环境，按这 8 步走一遍就能出稿。老手直接跳过。

**Step 0｜先分清要哪种产物**（选错要重来）

| 产物 | 用哪个技能 |
|------|-----------|
| 公众号文章（HTML，粘进 135 编辑器） | 本仓库 `xyb-wechat-article-generator` |
| 长篇白皮书、要出 DOCX | [`xyb-whitepaper-writer`](https://github.com/opencare-skillhub/xyb-whitepaper-writer) |

**Step 1｜装好 AI 编程助手**：Cursor / Claude Code / Kiro / CodeBuddy 这类助手挑一个顺手的装上登录
（到各家的官网下客户端即可，Mac / Windows 都有）。这一步是环境准备，本仓库帮不上忙。

**Step 2｜装技能**：复制下面**整段**（含 `==拷贝开始==` / `==拷贝结束==`）发给 agent，它会自己 clone 装上，
然后告诉它「后面我只要给素材，你直接出稿」。装完可以再跑一句「你现在装了哪些技能、放在哪个目录」确认一下：

```text
==拷贝开始==
我要搭一套「小胰宝」公众号文章的生成工具，请帮我装好，以后我给素材你直接出稿。

第一步，装这两个技能（用 HTTPS 地址 clone，别用 SSH）：
1. https://github.com/opencare-skillhub/xyb-wechat-article-generator.git
   —— 公众号文章：生成 HTML 纯片段，再粘进 135 编辑器
2. https://github.com/opencare-skillhub/xyb-whitepaper-writer
   —— 长篇白皮书 / 要出 DOCX 的时候用

第二步，装完后告诉我：
- 技能放在本机哪个目录（clone 到了哪）
- 以后我只要怎么说，你就能直接给我一份能粘进公众号的 HTML
- 生成后要跑哪些校验脚本、在哪跑
- 有哪几条硬规则是你必须遵守的（我会挑素材给你，不会让你编内容）

只要上面这四类信息，别让我自己去翻仓库文件。
==拷贝结束==
```

> 本仓库 README 里常见 SSH 地址（`git@github.com:...`），只有配过 GitHub key 的人才用得了；
> 上面特意写死 HTTPS，让 agent 自己 clone，省掉配 key 这一步——
> 如果你已经被要求配 SSH key，改成 `git@github.com:opencare-skillhub/xyb-wechat-article-generator.git` 也行。

**Step 3｜让 agent 生成文章**：**要求说得越细，文章越接近预期**——配色、模板、要讲哪几件事、
哪些话不要写，一次性说全。不会写就直接整段粘素材，再说一句「用紫色 template3 生成公众号文章」：

```
用紫色 template8（医患联合群版），把这段素材做成公众号文章：
<这里贴素材>
要求：医院定位与科室数据核医院官网；不要做疗效比较、不要医院排名。
```

**Step 4｜检查排版有没有套上**：打开生成的 HTML，必须以 `<section` 开头，
不能出现 `<html>` / `<style>` / `class=`。没套上就回一句
「排版错了，用 template3 生机微光重新排版一次」，让它重来。

**Step 5｜按需微调 HTML**：任意 HTML 编辑器（VS Code 最顺手），改完保存、浏览器刷新看效果；不用改就跳过。

**Step 6｜复制到 135 编辑器**：[135editor.com](https://www.135editor.com) →「导入」→「HTML 源码」→ 粘贴 →
再点顶部「HTML」切回可视化视图看前端效果 →「复制到公众号」。

**Step 7｜公众号新建文章**（后台左侧「内容与互动 → 图文素材」）。

**Step 8｜把 135 的内容全选复制进公众号后台** → 预览 → 按需微调 → 发布。
不想马上发就**存草稿**：发布前从草稿箱打开再核一遍图片（图没显示多半撞下面两条坑）。

**出问题时，先跑这三条**（都在技能目录下）

```bash
python3 scripts/restore-fragment.py <文章> --dry-run   # 是不是预览污染了
python3 scripts/verify-article.py <文章> --foot assets/template7-review/review_foot_purple.html
python3 scripts/verify-layout.py <文章>                 # 手机上有没有横向溢出
```

- **图在公众号里不显示、本地打开却正常** → 图片 URL 里混了 `%`、括号、空格、中文，
  被微信二次编码成 `%2520` 导致图床 404（校验第 7 项）。用 PicGo 重传一次干净文件名即可。
- **尾图变成一个灰块 / http 预览丢图** → 缺 `referrerpolicy="no-referrer"`（第 6 项），换域名没用。
- **粘贴后样式全丢** → 文件带了 `<html>` 外壳，跑一次 `restore-fragment.py`。

## 使用方法

### 发给 AI Agent 的使用说明（放最上面，省掉来回解释）

把下面**整段代码块**（含 `==拷贝开始==` / `==拷贝结束==` 两行）连同素材一起发给任意 AI Agent
（Claude / Codex / Cursor / Kiro 都行），它会照着走完「选版式 → 生成 → 校验 → 交付」。
用时把 `__SKILL_DIR__` 换成本机技能目录，或让 Agent 自己 clone 那个 HTTPS 地址。

> 这份说明对工具中立：不需要装特定客户端，也不需要配 SSH key，只要那个 Agent 能读文件系统、
> 能跑命令就可用。

```text
==拷贝开始==
你负责用「小胰宝公众号文章生成器」把用户给的素材排成一份能直接粘进微信公众号的 HTML 长文。
技能目录填这里：__SKILL_DIR__（没有就先
git clone https://github.com/opencare-skillhub/xyb-wechat-article-generator.git）

【第 0 步 · 先确认产物类型】
- 要公众号文章（HTML，粘进 135 编辑器）→ 用本仓库。
- 要长篇白皮书 / DOCX → 换 xyb-whitepaper-writer 技能，别用本仓库。

【第 1 步 · 选版式系列，默认 template3 生机微光】
  template3 生机微光（默认，日常科普）
  template1 莫兰迪柔和卡片（经典科普、叙事）
  template2 中国风/特展（文化历史专题）
  template4-ruici 瑞慈医疗（体检筛查、服务指南）
  template5-khub 病历记录风（个人叙事、罕见病记录）
  template6-med med 说明模版（药品/用药解读、紧急速查）
  template7-review 医生点评风（文献解读、临床研究速递、医生署名点评）
  template8-alliance 医患联合群·紫色（科室共建招募，见第 2 步）
路由关键词会自动命中：联合群 / 共建群 / 合作群 / 入群 / 科室共建 / 不用跑外地 / 家门口治疗 /
本地就医 ／ 临床介绍 / 药物介绍 / 药物卡片 / 试验卡片 / 在招研究 / 分子盘点 / 入组路径 / 中心速查。
用户没指定配色就用各系列旗舰模板（template3 治愈翡翠绿+琥珀暖阳）。

【第 2 步 · 生成】
1. 在 <技能目录>/output/ 下新建文章，命名 <主题>_公众号_<配色>.html。
2. 复制 assets/<系列>/ 下对应模板做起点；template8 直接填 alliance_template_purple.html
   的占位符，component-clinical-card 直接填 clinical_card_template.html 的占位符。
3. 素材缺哪块就留空或删掉整块，不许编内容；foot 尾巴（含尾图）逐字保留，不许改。
4. 图片一律用 COS 图床的干净 URL（路径部分只能含 [A-Za-z0-9/._-]）；本地图先用 PicGo
   （腾讯云 COS 图床）传上去，别拿本地相对路径或含中文/空格的文件名直接塞 src。
5. 正文链接必须包 <a href="..." target="_blank">，不能留裸 URL。
6. 输出必须是纯片段：文件直接以 <section 开头，禁止 <!DOCTYPE>／<html>／<head>／
   <style>／class=／内联样式以外的一切外壳。

【第 3 步 · 内容红线（违反就是返工）】
- 医院定位、科室数据、医生头衔一律核医院官网；第三方平台滞后（官网 > 政府/学会 > 第三方平台）。
- 头衔多源冲突取官网，文末加一行「职称以医院官网公示为准」。
- 不做疗效比较、不做医院排名；「家门口」只能建立在地理距离／随访连续性／并发症就近处理／
  陪护与时间成本上。
- 用户贴来的药物或临床资料不能直接照抄，逐条回一手源核对：公司名别张冠李戴、官方没写的
  机制写「未披露」、查不到来源的数字不写、注册节点（IND/首例入组）不算临床结果、
  同靶点不同分子不可互套数据、小样本要标例数。
- 私人手机号不进文章；链接 chip 附来源行（公众号名＋日期＋原标题）。
- 学科战略定位照抄原文，带「建设」字样的是目标不是成就，解读句只能用「方向是／目标是／争取」。

【第 4 步 · 交付前必跑校验（在技能目录下，全过才算完工）】
python3 scripts/verify-article.py <文章> --foot assets/template7-review/review_foot_purple.html  # 十项
python3 scripts/verify-layout.py <文章>                 # 375px 横向溢出
python3 scripts/restore-fragment.py <文章> --dry-run     # 预览污染检测
python3 scripts/check-placeholders.py                    # 只改过 template8 才需要
十项不全绿就修到全绿：漏 referrerpolicy／图片 URL 含 % 括号空格中文／带了 <html> 外壳／
标签没配平／裸 URL／foot 与母版不一致，脚本都会逐条报出来。
第 8 项报「预览污染」时先跑 python3 scripts/restore-fragment.py <文章> 还原，不要手改。

【第 5 步 · 交付】
1. 预览前先把文件复制到 /tmp 再预览——预览服务会就地改写源文件，不是只动副本。
2. 回一段「改了什么」的简报（200 字内），再给文件路径和「怎么粘进 135 编辑器」的步骤。
3. 不外发 base64，不外链本地绝对路径。
==拷贝结束==
```

### 在 Kiro 中使用

1. 在对话中通过 `#` 引用 skill
2. 提供素材内容和配色选择
3. 自动生成 HTML 文件

```
使用莫兰迪蓝模板，将 [素材] 生成公众号文章
```

### 医患联合群模版（template8）

医院科室 × 小胰宝共建病友群这类招募文已模版化，填占位符即出合规长文：

1. 把 `assets/template8-alliance/alliance_template_purple.html` 复制到文章目录
2. 按 `alliance_template_spec.md` 替换 36 个占位符（品牌头部／三条边界／社区能力矩阵／
   本地志愿者招募／结尾寄语五块话术已写死，不要改）
3. 跑 `python3 scripts/check-placeholders.py` 确认没有漏填、没有多填
4. 跑 `verify-article.py` 十项校验后发布

**这类文章的三条硬红线**：不做疗效比较、不做医院排名；「家门口」只能建立在地理距离／
随访连续性／并发症就近处理／陪护与时间成本上；医院定位、科室数据、专家头衔一律核医院官网——
第三方平台更新滞后（2026-10 实测：官网已更新为正高+博导，好大夫仍挂副高+硕导）。

### 发布到微信公众号

1. 打开 [135编辑器](https://www.135editor.com)
2. 点击"导入" → "HTML源码"
3. 粘贴生成的 HTML 代码
4. 微调后点"复制到公众号"
5. 在微信公众号后台粘贴发布

> 注意：输出必须是**纯片段**（直接以 `<section>` 开头）。带 `<html>` 外壳或 `data-*` 属性
> 的粘贴进编辑器会样式全丢，先跑 `restore-fragment.py` 还原。

## 配色方案速查

| 关键词 | 色系 | 推荐场景 |
|--------|------|---------|
| 绿色/默认 | 🌿 森林绿 | 日常科普 |
| 暖棕/莫兰迪 | 🤎 暖棕 | 人文关怀 |
| 蓝色/学术 | 🔵 雾霾蓝 | 学术报告、临床数据 |
| 灰色 | ⚪ 高级灰 | 严肃话题、纪念 |
| 粉色 | 🩷 豆沙粉 | 心理关怀、女性话题 |
| 红色 | 🔴 赭红 | 重要警示 |
| 紫色/胰腺癌 | 🟣 烟紫 | 胰腺癌宣传月（11月） |
| 灰绿/营养 | 🟢 灰绿 | 营养科普 |
| Tiffany/活动 | 💎 蒂芙尼蓝 | 活动推广、节日 |

## 版式系列速查

| 系列 | 风格 | 适用场景 |
|------|------|---------|
| template3 | 🌿 生机微光（默认） | 日常科普、治愈系长文 |
| template1 | 🎨 莫兰迪柔和卡片 | 经典科普、叙事 |
| template2 | 🏮 中国风/特展 | 文化历史向专题 |
| template4-ruici | 🩺 瑞慈医疗服务 | 医院合作、体检筛查、服务指南 |
| template5-khub | 📋 病历记录风 | 个人叙事、深度科普、罕见病记录 |
| template6-med | 💊 med 说明模版 | 药品说明书解读、用药对照、紧急速查、患教说明 |
| template7-review | 👨‍⚕️ 医生点评风（前沿荟萃学术风） | 文献解读、临床研究速递、医生署名点评文章 |
| template8-alliance | 🤝 医患联合群（紫色，可填空） | 医院科室 × 小胰宝共建病友群、本地就医与志愿者招募（路由词：联合群/共建群/入群/科室共建/不用跑外地/家门口治疗/本地就医） |
| template_bm | 📰 前沿速递风（杂志快讯，橙/紫/绿） | 新闻资讯、前沿速递、研究亮点、breaking 科普（路由词：前沿速递/快讯/breaking/研究亮点/新闻资讯/bm 模版） |

## 在其他 AI 工具中使用

### Claude (Anthropic)

在 Claude 对话中，将 `skill.md` 的内容作为 System Prompt 或对话开头粘贴，然后附上素材：

```
[粘贴 skill.md 全文]

---

请使用莫兰迪蓝配色，将以下内容生成公众号文章 HTML：

[粘贴素材内容]
```

也可以在 Claude Projects 中将 `skill.md` 和模板文件添加为 Project Knowledge，之后每次对话直接说：

```
使用蓝色模板，将以下内容生成公众号文章：[素材]
```

### OpenAI Codex / ChatGPT

**方式一：Custom Instructions**

将 `skill.md` 中的核心规则粘贴到 ChatGPT 的 "Custom Instructions" 或 GPTs 的 System Prompt 中。

**方式二：对话内使用**

```
你是一个微信公众号排版助手。请严格按照以下规则生成文章：
- 全部使用 inline style，不用 <style> 或 class
- 使用 <section> 标签
- 配色方案：主色 #4a6580，强调色 #8b5e5e，背景 #f0f4f8
- 字体：PingFangSC-light, letter-spacing:1px, line-height:2, font-size:14px

模板参考：
[粘贴 assets/template1/xyb_template_morandi_blue.html 的内容]

素材内容：
[粘贴你的素材]

请生成完整的公众号 HTML 代码。
```

**方式三：创建 GPTs**

1. 在 ChatGPT 中创建一个 GPT
2. 将 `skill.md` 作为 Instructions
3. 上传 `assets/template1/` 和 `assets/template2/` 下的模板文件作为 Knowledge
4. 用户只需说"使用蓝色模板生成文章"即可

### OpenClaw

在 OpenClaw 中创建 Agent 时：

1. **System Prompt**：粘贴 `skill.md` 全文
2. **Knowledge Base**：上传 `assets/template1/` 和 `assets/template2/` 目录下的所有模板文件
3. **使用时**：直接输入素材内容和配色选择

```yaml
# OpenClaw Agent 配置示例
name: 小胰宝公众号生成器
system_prompt: |
  [skill.md 内容]
knowledge_files:
  - assets/template1/xyb_template.html
  - assets/template1/xyb_template_morandi_blue.html
  - assets/template2/xyb2_template.html          # 中国风/特展版式
  - assets/template2/xyb2_template_morandi_purple.html
  # ... 其他模板（两个系列共 19 个文件）
```

### Hermes (Nous Research)

Hermes 模型支持 System Prompt + Tool Use。推荐配置：

```
<|im_start|>system
你是小胰宝公众号文章生成器。

[粘贴 skill.md 核心规则部分]

可用配色：绿色(#2d6a4f)、蓝色(#4a6580)、紫色(#5c4a7a)、粉色(#8c5c6c)、灰色(#5c5c5c)、红色(#7a4a4a)、Tiffany(#0abab5)

用户提供素材后，直接输出完整 inline style HTML 代码。
<|im_end|>
<|im_start|>user
使用蓝色模板，将以下内容生成公众号文章：
[素材内容]
<|im_end|>
```

### 通用提示词（适用于任何 LLM）

如果你使用的 AI 工具不在上述列表中，可以使用以下通用提示词：

```
你是一个微信公众号 HTML 排版助手。请根据我的素材生成文章，规则如下：

1. 全部使用 inline style（style=""），不用 <style> 标签
2. 使用 <section> 标签而非 <div>
3. 字体：font-family:'PingFangSC-light','PingFang SC',sans-serif
4. 正文：font-size:14px; letter-spacing:1px; line-height:2
5. 配色：主色[填入主色]，强调色[填入强调色]，背景[填入背景色]
6. 数据必须与原文一致，不得编造
7. 输出纯 HTML，不要 <!DOCTYPE> 等外壳标签

素材：
[你的内容]
```

---

## 关于小胰宝

小胰宝是一个面向胰腺肿瘤患者及家属的开源公益项目，归属小X宝社区和天工开物基金会管理。

- 官网：www.xiaoyibao.com.cn
- 社区：info.xiao-x-bao.com.cn
- 小红书：@小胰宝宝
- 公众号：@小胰宝助手
- 播客：小宇宙 @微光成炬 胰路同心
